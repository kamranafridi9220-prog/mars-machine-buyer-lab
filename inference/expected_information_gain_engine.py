"""
MARS — Machine-Agent Revenue Science

Experiment 015

Expected Information Gain Policy Discovery Engine

Author: Kamran Khan

Purpose:
Select commercial experiments according to their
expected ability to reduce uncertainty about hidden
black-box buyer procurement policies.

The engine does not access the buyer's private
decision-policy variables.

Instead, it maintains bounded beliefs about each
commercial constraint, generates candidate probes,
estimates the expected information gain of each probe,
selects the highest-value experiment, observes the
buyer's decision, and updates its belief state.
"""

from dataclasses import asdict, replace
import math


class ExpectedInformationGainEngine:

    def __init__(
        self,
        buyer,
        reference_proposal
    ):

        self.buyer = buyer
        self.reference_proposal = reference_proposal

        self.query_count = 0

        self.experiment_history = []
        self.selection_history = []

        # ----------------------------------------------------
        # COMMERCIAL POLICY SEARCH SPACE
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # INITIAL POLICY BELIEFS
        # ----------------------------------------------------

        self.policy_beliefs = {}

        for variable, configuration in self.search_space.items():

            self.policy_beliefs[variable] = {

                "lower": configuration["lower"],

                "upper": configuration["upper"],

                "direction": configuration["direction"],

                "tolerance": configuration["tolerance"],

                "resolved": False,

                "estimated_threshold": None

            }


    # ========================================================
    # INTERVAL WIDTH
    # ========================================================

    def interval_width(
        self,
        variable
    ):

        belief = self.policy_beliefs[variable]

        return max(

            0,

            belief["upper"]
            -
            belief["lower"]

        )


    # ========================================================
    # NORMALISED UNCERTAINTY
    # ========================================================

    def normalised_uncertainty(
        self,
        variable
    ):

        current_width = self.interval_width(
            variable
        )

        original = self.search_space[variable]

        original_width = (

            original["upper"]
            -
            original["lower"]

        )

        if original_width <= 0:

            return 0.0

        return (

            current_width
            /
            original_width

        )


    # ========================================================
    # ENTROPY OF POLICY INTERVAL
    # ========================================================

    def interval_entropy(
        self,
        variable
    ):

        uncertainty = self.normalised_uncertainty(
            variable
        )

        if uncertainty <= 0:

            return 0.0

        return math.log2(

            1.0 + uncertainty

        )


    # ========================================================
    # GENERATE CANDIDATE VALUES
    # ========================================================

    def generate_candidate_values(
        self,
        variable
    ):

        belief = self.policy_beliefs[variable]

        lower = belief["lower"]
        upper = belief["upper"]

        width = upper - lower

        if width <= belief["tolerance"]:

            return []


        # ----------------------------------------------------
        # THREE INTERNAL PROBES
        #
        # 25% point
        # 50% point
        # 75% point
        # ----------------------------------------------------

        fractions = [

            0.25,

            0.50,

            0.75

        ]


        candidates = []


        for fraction in fractions:

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
    # ESTIMATE DECISION PROBABILITY
    # ========================================================

    def estimate_acceptance_probability(
        self,
        variable,
        candidate_value
    ):

        belief = self.policy_beliefs[variable]

        lower = belief["lower"]
        upper = belief["upper"]

        width = upper - lower

        if width <= 0:

            return 1.0


        direction = belief["direction"]


        # ----------------------------------------------------
        # Assume a uniform prior over the currently feasible
        # threshold interval.
        #
        # Maximum constraint:
        # proposal accepted when candidate <= threshold.
        #
        # Minimum constraint:
        # proposal accepted when candidate >= threshold.
        # ----------------------------------------------------

        if direction == "maximum":

            probability = (

                upper - candidate_value

            ) / width


        elif direction == "minimum":

            probability = (

                candidate_value - lower

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
    # BINARY DECISION ENTROPY
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
    # EXPECTED INFORMATION GAIN
    # ========================================================

    def expected_information_gain(
        self,
        variable,
        candidate_value
    ):

        acceptance_probability = (
            self.estimate_acceptance_probability(

                variable,

                candidate_value

            )
        )


        # ----------------------------------------------------
        # For a deterministic threshold buyer under a
        # uniform threshold prior, the entropy of the
        # ACCEPT / REJECT observation represents the
        # expected information obtained from the probe.
        # ----------------------------------------------------

        decision_entropy = (
            self.binary_entropy(
                acceptance_probability
            )
        )


        # ----------------------------------------------------
        # Weight the information value by unresolved
        # normalised policy uncertainty.
        # ----------------------------------------------------

        uncertainty_weight = (
            self.normalised_uncertainty(
                variable
            )
        )


        score = (

            decision_entropy
            *
            uncertainty_weight

        )


        return {

            "variable":
                variable,

            "candidate_value":
                candidate_value,

            "acceptance_probability":
                acceptance_probability,

            "decision_entropy":
                decision_entropy,

            "uncertainty_weight":
                uncertainty_weight,

            "expected_information_gain":
                score

        }


    # ========================================================
    # SCORE ALL AVAILABLE EXPERIMENTS
    # ========================================================

    def score_candidate_experiments(
        self
    ):

        candidates = []


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

                score = (
                    self.expected_information_gain(

                        variable,

                        value

                    )
                )


                candidates.append(
                    score
                )


        return candidates


    # ========================================================
    # SELECT NEXT-BEST EXPERIMENT
    # ========================================================

    def select_next_experiment(
        self
    ):

        candidates = (
            self.score_candidate_experiments()
        )


        if not candidates:

            return None


        selected = max(

            candidates,

            key=lambda item: (
                item[
                    "expected_information_gain"
                ],
                item[
                    "decision_entropy"
                ],
                item[
                    "uncertainty_weight"
                ]
            )

        )


        return selected


    # ========================================================
    # GENERATE COMMERCIAL PROBE
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
    # QUERY BLACK-BOX BUYER
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

            "expected_information_gain":
                experiment[
                    "expected_information_gain"
                ],

            "acceptance_probability":
                experiment[
                    "acceptance_probability"
                ],

            "proposal":
                asdict(proposal),

            "decision":
                response["decision"]

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
    # UPDATE POLICY BELIEF
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
    # RUN ONE ACTIVE-LEARNING STEP
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


        entropy_before = (
            self.interval_entropy(
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


        entropy_after = (
            self.interval_entropy(
                variable
            )
        )


        realised_information_gain = max(

            0.0,

            entropy_before
            -
            entropy_after

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

            "acceptance_probability":
                selected[
                    "acceptance_probability"
                ],

            "decision_entropy":
                selected[
                    "decision_entropy"
                ],

            "expected_information_gain":
                selected[
                    "expected_information_gain"
                ],

            "uncertainty_before":
                uncertainty_before,

            "uncertainty_after":
                uncertainty_after,

            "realised_information_gain":
                realised_information_gain

        }


        self.selection_history.append(
            record
        )


        return record


    # ========================================================
    # RUN POLICY DISCOVERY
    # ========================================================

    def discover_policy(
        self,
        maximum_queries=100
    ):

        print("\n" + "=" * 72)

        print(
            "MARS EXPECTED INFORMATION GAIN "
            "POLICY DISCOVERY"
        )

        print("=" * 72)


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
                "Candidate Value:",
                result[
                    "candidate_value"
                ]
            )


            print(
                "Expected Information Gain:",
                round(
                    result[
                        "expected_information_gain"
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


            print(
                "Realised Information Gain:",
                round(
                    result[
                        "realised_information_gain"
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
    # FINAL RESULTS
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
                self.selection_history

        }
