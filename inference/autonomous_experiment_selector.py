"""
MARS — Machine-Agent Revenue Science

Experiment 013

Autonomous Next-Best Commercial Experiment Selector

Author: Kamran Khan

Purpose:
Autonomously select informative commercial experiments
for discovering hidden black-box buyer policies.

The selector does not access the buyer's private policy.

Instead, it maintains uncertainty intervals for commercial
variables and selects experiments intended to reduce
uncertainty through observable buyer decisions.
"""

from dataclasses import asdict, replace


# ============================================================
# AUTONOMOUS EXPERIMENT SELECTOR
# ============================================================

class AutonomousExperimentSelector:

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

        self.policy_beliefs = {}


        # ----------------------------------------------------
        # INITIAL SEARCH SPACE
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
        # INITIALISE BELIEF STATE
        # ----------------------------------------------------

        for variable, configuration in (
            self.search_space.items()
        ):

            self.policy_beliefs[variable] = {

                "lower": configuration["lower"],

                "upper": configuration["upper"],

                "direction": configuration["direction"],

                "tolerance": configuration["tolerance"],

                "resolved": False,

                "estimated_threshold": None

            }


    # ============================================================
    # NORMALISED UNCERTAINTY
    # ============================================================

    def calculate_uncertainty(
        self,
        variable
    ):

        belief = self.policy_beliefs[variable]

        current_width = (
            belief["upper"] -
            belief["lower"]
        )

        original = self.search_space[variable]

        original_width = (
            original["upper"] -
            original["lower"]
        )

        if original_width == 0:

            return 0

        return (
            current_width /
            original_width
        )


    # ============================================================
    # SELECT MOST UNCERTAIN VARIABLE
    # ============================================================

    def select_variable(self):

        unresolved = [

            variable

            for variable, belief
            in self.policy_beliefs.items()

            if not belief["resolved"]

        ]

        if not unresolved:

            return None


        uncertainties = {

            variable:
            self.calculate_uncertainty(variable)

            for variable in unresolved

        }


        selected_variable = max(

            uncertainties,

            key=uncertainties.get

        )


        return selected_variable


    # ============================================================
    # SELECT NEXT CANDIDATE VALUE
    # ============================================================

    def select_candidate_value(
        self,
        variable
    ):

        belief = self.policy_beliefs[variable]

        lower = belief["lower"]

        upper = belief["upper"]


        if variable in [

            "contract_months",

            "payment_days"

        ]:

            candidate = (

                lower + upper

            ) // 2

        else:

            candidate = (

                lower + upper

            ) / 2


        return candidate


    # ============================================================
    # GENERATE COMMERCIAL PROBE
    # ============================================================

    def generate_probe(
        self,
        variable,
        candidate_value
    ):

        return replace(

            self.reference_proposal,

            **{
                variable: candidate_value
            }

        )


    # ============================================================
    # QUERY BLACK-BOX BUYER
    # ============================================================

    def query_buyer(
        self,
        proposal,
        variable,
        candidate_value
    ):

        response = self.buyer.evaluate_proposal(

            proposal

        )

        self.query_count += 1


        record = {

            "query": self.query_count,

            "variable": variable,

            "candidate_value": candidate_value,

            "proposal": asdict(proposal),

            "decision": response["decision"]

        }


        self.experiment_history.append(

            record

        )


        return (
            response["decision"] == "ACCEPTED"
        )


    # ============================================================
    # UPDATE POLICY BELIEF
    # ============================================================

    def update_belief(
        self,
        variable,
        candidate_value,
        accepted
    ):

        belief = self.policy_beliefs[variable]

        direction = belief["direction"]


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

            belief["upper"] -
            belief["lower"]

        )


        # ----------------------------------------------------
        # DETERMINE WHETHER POLICY IS RESOLVED
        # ----------------------------------------------------

        if uncertainty <= belief["tolerance"]:

            belief["resolved"] = True


            if direction == "maximum":

                belief["estimated_threshold"] = (
                    belief["lower"]
                )

            else:

                belief["estimated_threshold"] = (
                    belief["upper"]
                )


    # ============================================================
    # RUN NEXT AUTONOMOUS EXPERIMENT
    # ============================================================

    def run_next_experiment(self):

        variable = self.select_variable()


        if variable is None:

            return None


        candidate_value = (
            self.select_candidate_value(
                variable
            )
        )


        proposal = self.generate_probe(

            variable,

            candidate_value

        )


        uncertainty_before = (
            self.calculate_uncertainty(
                variable
            )
        )


        accepted = self.query_buyer(

            proposal,

            variable,

            candidate_value

        )


        self.update_belief(

            variable,

            candidate_value,

            accepted

        )


        uncertainty_after = (
            self.calculate_uncertainty(
                variable
            )
        )


        selection_record = {

            "query": self.query_count,

            "selected_variable": variable,

            "candidate_value": candidate_value,

            "buyer_decision": (
                "ACCEPTED"
                if accepted
                else "REJECTED"
            ),

            "uncertainty_before": (
                uncertainty_before
            ),

            "uncertainty_after": (
                uncertainty_after
            ),

            "information_gain": (
                uncertainty_before -
                uncertainty_after
            )

        }


        self.selection_history.append(

            selection_record

        )


        return selection_record


    # ============================================================
    # RUN AUTONOMOUS DISCOVERY
    # ============================================================

    def discover_policy(
        self,
        maximum_queries=100
    ):

        print("\n" + "=" * 70)

        print(
            "MARS AUTONOMOUS EXPERIMENT SELECTION"
        )

        print("=" * 70)


        while self.query_count < maximum_queries:

            result = self.run_next_experiment()


            if result is None:

                break


            print(

                f"\nQuery {result['query']}"

            )

            print(

                "Selected Variable:",

                result["selected_variable"]

            )

            print(

                "Candidate Value:",

                result["candidate_value"]

            )

            print(

                "Buyer Decision:",

                result["buyer_decision"]

            )

            print(

                "Uncertainty Before:",

                round(
                    result[
                        "uncertainty_before"
                    ],
                    6
                )

            )

            print(

                "Uncertainty After:",

                round(
                    result[
                        "uncertainty_after"
                    ],
                    6
                )

            )

            print(

                "Information Gain:",

                round(
                    result[
                        "information_gain"
                    ],
                    6
                )

            )


        return self.get_results()


    # ============================================================
    # GET DISCOVERED POLICY
    # ============================================================

    def get_discovered_policy(self):

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


    # ============================================================
    # FINAL RESULTS
    # ============================================================

    def get_results(self):

        return {

            "total_queries": (
                self.query_count
            ),

            "discovered_policy": (
                self.get_discovered_policy()
            ),

            "policy_beliefs": (
                self.policy_beliefs
            ),

            "experiment_history": (
                self.experiment_history
            ),

            "selection_history": (
                self.selection_history
            )

        }
