"""
MARS — Machine-Agent Revenue Science

Experiment 016

Cost-Aware Information Gain Engine

Author: Kamran Khan

Purpose:
Select black-box buyer experiments according to both
their expected information value and their estimated
commercial cost.

The engine extends active policy discovery from pure
information acquisition toward economically rational
commercial experimentation.

The buyer's private procurement-policy variables are
never accessed by this engine.
"""

from dataclasses import asdict, replace
import math


class CostAwareInformationEngine:

    def __init__(
        self,
        buyer,
        reference_proposal,
        cost_weight=0.25,
        risk_weight=0.10
    ):

        self.buyer = buyer

        self.reference_proposal = (
            reference_proposal
        )

        self.cost_weight = cost_weight

        self.risk_weight = risk_weight

        self.query_count = 0

        self.experiment_history = []

        self.selection_history = []


        # ====================================================
        # POLICY SEARCH SPACE
        # ====================================================

        self.search_space = {

            "annual_price": {
                "lower": 50000,
                "upper": 150000,
                "direction": "maximum",
                "tolerance": 1
            },

            "contract_months": {
                "lower": 12,
                "upper": 60,
                "direction": "maximum",
                "tolerance": 1
            },

            "service_availability": {
                "lower": 90.0,
                "upper": 100.0,
                "direction": "minimum",
                "tolerance": 0.001
            },

            "payment_days": {
                "lower": 7,
                "upper": 90,
                "direction": "minimum",
                "tolerance": 1
            },

            "supplier_reliability": {
                "lower": 60.0,
                "upper": 100.0,
                "direction": "minimum",
                "tolerance": 0.001
            }

        }


        # ====================================================
        # POLICY BELIEFS
        # ====================================================

        self.policy_beliefs = {}


        for variable, configuration in (
            self.search_space.items()
        ):

            self.policy_beliefs[variable] = {

                "lower":
                    configuration["lower"],

                "upper":
                    configuration["upper"],

                "direction":
                    configuration["direction"],

                "tolerance":
                    configuration["tolerance"],

                "resolved":
                    False,

                "estimated_threshold":
                    None

            }


    # ========================================================
    # NORMALISED POLICY UNCERTAINTY
    # ========================================================

    def normalised_uncertainty(
        self,
        variable
    ):

        belief = self.policy_beliefs[
            variable
        ]

        current_width = (

            belief["upper"]
            -
            belief["lower"]

        )


        original = self.search_space[
            variable
        ]


        original_width = (

            original["upper"]
            -
            original["lower"]

        )


        if original_width <= 0:

            return 0.0


        return max(

            0.0,

            current_width
            /
            original_width

        )


    # ========================================================
    # GENERATE CANDIDATE VALUES
    # ========================================================

    def generate_candidate_values(
        self,
        variable
    ):

        belief = self.policy_beliefs[
            variable
        ]


        lower = belief["lower"]

        upper = belief["upper"]

        width = upper - lower


        if width <= belief["tolerance"]:

            return []


        candidates = []


        for fraction in [

            0.25,

            0.50,

            0.75

        ]:

            value = (

                lower
                +
                width * fraction

            )


            if variable in [

                "contract_months",

                "payment_days"

            ]:

                value = int(
                    round(value)
                )


            if (
                value <= lower
                or
                value >= upper
            ):

                continue


            if value not in candidates:

                candidates.append(
                    value
                )


        return candidates


    # ========================================================
    # ACCEPTANCE PROBABILITY
    # ========================================================

    def estimate_acceptance_probability(
        self,
        variable,
        candidate_value
    ):

        belief = self.policy_beliefs[
            variable
        ]


        lower = belief["lower"]

        upper = belief["upper"]

        width = upper - lower


        if width <= 0:

            return 1.0


        if belief["direction"] == "maximum":

            probability = (

                upper
                -
                candidate_value

            ) / width


        elif belief["direction"] == "minimum":

            probability = (

                candidate_value
                -
                lower

            ) / width


        else:

            raise ValueError(

                "Unknown policy direction."

            )


        return max(

            0.0,

            min(
                1.0,
                probability
            )

        )


    # ========================================================
    # BINARY ENTROPY
    # ========================================================

    def binary_entropy(
        self,
        probability
    ):

        if (
            probability <= 0
            or
            probability >= 1
        ):

            return 0.0


        return -(

            probability
            *
            math.log2(probability)

            +

            (1 - probability)
            *
            math.log2(
                1 - probability
            )

        )


    # ========================================================
    # EXPECTED INFORMATION VALUE
    # ========================================================

    def expected_information_value(
        self,
        variable,
        candidate_value
    ):

        probability = (
            self.estimate_acceptance_probability(

                variable,

                candidate_value

            )
        )


        entropy = (
            self.binary_entropy(
                probability
            )
        )


        uncertainty = (
            self.normalised_uncertainty(
                variable
            )
        )


        return {

            "acceptance_probability":
                probability,

            "decision_entropy":
                entropy,

            "information_value":
                entropy * uncertainty

        }


    # ========================================================
    # COMMERCIAL COST MODEL
    # ========================================================

    def commercial_probe_cost(
        self,
        variable,
        candidate_value
    ):

        reference = self.reference_proposal


        # ----------------------------------------------------
        # PRICE CONCESSION
        # ----------------------------------------------------

        if variable == "annual_price":

            cost = max(

                0,

                reference.annual_price
                -
                candidate_value

            )


        # ----------------------------------------------------
        # SHORTER CONTRACT
        #
        # Opportunity cost proxy:
        # £250 per month removed.
        # ----------------------------------------------------

        elif variable == "contract_months":

            cost = max(

                0,

                reference.contract_months
                -
                candidate_value

            ) * 250


        # ----------------------------------------------------
        # SERVICE AVAILABILITY
        #
        # Operational cost proxy:
        # £1,500 per percentage-point improvement.
        # ----------------------------------------------------

        elif variable == "service_availability":

            cost = max(

                0,

                candidate_value
                -
                reference.service_availability

            ) * 1500


        # ----------------------------------------------------
        # PAYMENT TERMS
        #
        # Working-capital proxy:
        # £100 per additional payment day.
        # ----------------------------------------------------

        elif variable == "payment_days":

            cost = max(

                0,

                candidate_value
                -
                reference.payment_days

            ) * 100


        # ----------------------------------------------------
        # SUPPLIER RELIABILITY
        #
        # Capability investment proxy:
        # £1,000 per reliability point.
        # ----------------------------------------------------

        elif variable == "supplier_reliability":

            cost = max(

                0,

                candidate_value
                -
                reference.supplier_reliability

            ) * 1000


        else:

            raise ValueError(

                f"Unknown commercial variable: "
                f"{variable}"

            )


        return float(cost)


    # ========================================================
    # NORMALISE COMMERCIAL COST
    # ========================================================

    def normalise_cost(
        self,
        costs
    ):

        if not costs:

            return {}


        maximum_cost = max(
            costs.values()
        )


        if maximum_cost <= 0:

            return {

                key: 0.0

                for key in costs

            }


        return {

            key:
                value / maximum_cost

            for key, value in (
                costs.items()
            )

        }


    # ========================================================
    # COMMERCIAL RISK
    # ========================================================

    def estimate_commercial_risk(
        self,
        variable,
        candidate_value
    ):

        reference_value = getattr(

            self.reference_proposal,

            variable

        )


        configuration = (
            self.search_space[
                variable
            ]
        )


        total_range = (

            configuration["upper"]
            -
            configuration["lower"]

        )


        if total_range <= 0:

            return 0.0


        deviation = abs(

            candidate_value
            -
            reference_value

        )


        risk = (

            deviation
            /
            total_range

        )


        return max(

            0.0,

            min(
                1.0,
                risk
            )

        )


    # ========================================================
    # SCORE CANDIDATE EXPERIMENTS
    # ========================================================

    def score_candidate_experiments(
        self
    ):

        raw_candidates = []

        cost_map = {}


        candidate_id = 0


        for variable, belief in (

            self.policy_beliefs.items()

        ):

            if belief["resolved"]:

                continue


            values = (
                self.generate_candidate_values(
                    variable
                )
            )


            for value in values:

                candidate_id += 1


                information = (
                    self.expected_information_value(

                        variable,

                        value

                    )
                )


                commercial_cost = (
                    self.commercial_probe_cost(

                        variable,

                        value

                    )
                )


                commercial_risk = (
                    self.estimate_commercial_risk(

                        variable,

                        value

                    )
                )


                candidate = {

                    "candidate_id":
                        candidate_id,

                    "variable":
                        variable,

                    "candidate_value":
                        value,

                    "acceptance_probability":
                        information[
                            "acceptance_probability"
                        ],

                    "decision_entropy":
                        information[
                            "decision_entropy"
                        ],

                    "information_value":
                        information[
                            "information_value"
                        ],

                    "commercial_cost":
                        commercial_cost,

                    "commercial_risk":
                        commercial_risk

                }


                raw_candidates.append(
                    candidate
                )


                cost_map[
                    candidate_id
                ] = commercial_cost


        normalised_costs = (
            self.normalise_cost(
                cost_map
            )
        )


        scored_candidates = []


        for candidate in raw_candidates:

            normalised_cost = (
                normalised_costs[
                    candidate[
                        "candidate_id"
                    ]
                ]
            )


            utility = (

                candidate[
                    "information_value"
                ]

                -

                self.cost_weight
                *
                normalised_cost

                -

                self.risk_weight
                *
                candidate[
                    "commercial_risk"
                ]

            )


            candidate[
                "normalised_cost"
            ] = normalised_cost


            candidate[
                "utility_score"
            ] = utility


            scored_candidates.append(
                candidate
            )


        return scored_candidates


    # ========================================================
    # SELECT HIGHEST-UTILITY EXPERIMENT
    # ========================================================

    def select_next_experiment(
        self
    ):

        candidates = (
            self.score_candidate_experiments()
        )


        if not candidates:

            return None


        return max(

            candidates,

            key=lambda item: (

                item["utility_score"],

                item["information_value"],

                -item["commercial_cost"]

            )

        )


    # ========================================================
    # GENERATE BUYER PROBE
    # ========================================================

    def generate_probe(
        self,
        variable,
        candidate_value
    ):

        return replace(

            self.reference_proposal,

            **{
                variable:
                    candidate_value
            }

        )


    # ========================================================
    # QUERY BUYER
    # ========================================================

    def query_buyer(
        self,
        proposal,
        experiment
    ):

        response = (
            self.buyer.evaluate_proposal(
                proposal
            )
        )


        self.query_count += 1


        record = {

            "query":
                self.query_count,

            "variable":
                experiment["variable"],

            "candidate_value":
                experiment[
                    "candidate_value"
                ],

            "proposal":
                asdict(proposal),

            "decision":
                response["decision"],

            "information_value":
                experiment[
                    "information_value"
                ],

            "commercial_cost":
                experiment[
                    "commercial_cost"
                ],

            "normalised_cost":
                experiment[
                    "normalised_cost"
                ],

            "commercial_risk":
                experiment[
                    "commercial_risk"
                ],

            "utility_score":
                experiment[
                    "utility_score"
                ]

        }


        self.experiment_history.append(
            record
        )


        return (
            response["decision"]
            ==
            "ACCEPTED"
        )


    # ========================================================
    # UPDATE BELIEF
    # ========================================================

    def update_belief(
        self,
        variable,
        candidate_value,
        accepted
    ):

        belief = self.policy_beliefs[
            variable
        ]


        direction = belief[
            "direction"
        ]


        if direction == "maximum":

            if accepted:

                belief["lower"] = (
                    candidate_value
                )

            else:

                belief["upper"] = (
                    candidate_value
                )


        elif direction == "minimum":

            if accepted:

                belief["upper"] = (
                    candidate_value
                )

            else:

                belief["lower"] = (
                    candidate_value
                )


        else:

            raise ValueError(

                "Unknown policy direction."

            )


        uncertainty = (

            belief["upper"]
            -
            belief["lower"]

        )


        if uncertainty <= belief["tolerance"]:

            belief["resolved"] = True


            if direction == "maximum":

                belief[
                    "estimated_threshold"
                ] = belief["lower"]


            else:

                belief[
                    "estimated_threshold"
                ] = belief["upper"]


    # ========================================================
    # RUN NEXT COST-AWARE EXPERIMENT
    # ========================================================

    def run_next_experiment(
        self
    ):

        selected = (
            self.select_next_experiment()
        )


        if selected is None:

            return None


        variable = selected[
            "variable"
        ]


        candidate_value = selected[
            "candidate_value"
        ]


        uncertainty_before = (
            self.normalised_uncertainty(
                variable
            )
        )


        proposal = self.generate_probe(

            variable,

            candidate_value

        )


        accepted = self.query_buyer(

            proposal,

            selected

        )


        self.update_belief(

            variable,

            candidate_value,

            accepted

        )


        uncertainty_after = (
            self.normalised_uncertainty(
                variable
            )
        )


        realised_uncertainty_reduction = max(

            0.0,

            uncertainty_before
            -
            uncertainty_after

        )


        record = {

            "query":
                self.query_count,

            "selected_variable":
                variable,

            "candidate_value":
                candidate_value,

            "buyer_decision":
                (
                    "ACCEPTED"
                    if accepted
                    else
                    "REJECTED"
                ),

            "information_value":
                selected[
                    "information_value"
                ],

            "commercial_cost":
                selected[
                    "commercial_cost"
                ],

            "normalised_cost":
                selected[
                    "normalised_cost"
                ],

            "commercial_risk":
                selected[
                    "commercial_risk"
                ],

            "utility_score":
                selected[
                    "utility_score"
                ],

            "uncertainty_before":
                uncertainty_before,

            "uncertainty_after":
                uncertainty_after,

            "realised_uncertainty_reduction":
                realised_uncertainty_reduction

        }


        self.selection_history.append(
            record
        )


        return record


    # ========================================================
    # RUN DISCOVERY
    # ========================================================

    def discover_policy(
        self,
        maximum_queries=150
    ):

        print("\n" + "=" * 75)

        print(
            "MARS COST-AWARE INFORMATION "
            "GAIN POLICY DISCOVERY"
        )

        print("=" * 75)


        while self.query_count < maximum_queries:

            result = (
                self.run_next_experiment()
            )


            if result is None:

                break


            print(
                f"\nQuery {result['query']}"
            )


            print(
                "Selected Variable:",
                result[
                    "selected_variable"
                ]
            )


            print(
                "Candidate:",
                result[
                    "candidate_value"
                ]
            )


            print(
                "Information Value:",
                round(
                    result[
                        "information_value"
                    ],
                    6
                )
            )


            print(
                "Commercial Cost:",
                "£"
                f"{result['commercial_cost']:,.2f}"
            )


            print(
                "Commercial Risk:",
                round(
                    result[
                        "commercial_risk"
                    ],
                    6
                )
            )


            print(
                "Utility Score:",
                round(
                    result[
                        "utility_score"
                    ],
                    6
                )
            )


            print(
                "Buyer Decision:",
                result[
                    "buyer_decision"
                ]
            )


            print(
                "Uncertainty:",
                round(
                    result[
                        "uncertainty_before"
                    ],
                    6
                ),
                "→",
                round(
                    result[
                        "uncertainty_after"
                    ],
                    6
                )
            )


        return self.get_results()


    # ========================================================
    # DISCOVERED POLICY
    # ========================================================

    def get_discovered_policy(
        self
    ):

        discovered = {}


        for variable, belief in (

            self.policy_beliefs.items()

        ):

            if belief["resolved"]:

                discovered[variable] = (
                    belief[
                        "estimated_threshold"
                    ]
                )

            else:

                discovered[variable] = None


        return discovered


    # ========================================================
    # RESULTS
    # ========================================================

    def get_results(
        self
    ):

        return {

            "total_queries":
                self.query_count,

            "discovered_policy":
                self.get_discovered_policy(),

            "policy_beliefs":
                self.policy_beliefs,

            "experiment_history":
                self.experiment_history,

            "selection_history":
                self.selection_history,

            "cost_weight":
                self.cost_weight,

            "risk_weight":
                self.risk_weight

        }
