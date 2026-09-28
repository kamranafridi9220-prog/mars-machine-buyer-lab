"""
MARS — Machine-Agent Revenue Science

Experiment 018

Repeated-Evidence Buyer Policy Discovery Engine

Author: Kamran Khan

Purpose:
Discover hidden procurement-policy thresholds when
buyer decisions are probabilistic near commercial
decision boundaries.

Unlike deterministic binary-search inference, this
engine does not treat a single ACCEPTED or REJECTED
observation as conclusive evidence.

Each candidate commercial value is evaluated
multiple times. The engine aggregates repeated
observations and uses the observed acceptance rate
to determine the experimental outcome.

Research Objective:
Measure whether repeated evidence improves the
robustness of black-box buyer-policy discovery
under stochastic decision noise.
"""

from dataclasses import replace


# ============================================================
# REPEATED-EVIDENCE POLICY DISCOVERY ENGINE
# ============================================================

class RepeatedEvidencePolicyDiscoveryEngine:

    def __init__(
        self,
        buyer,
        reference_proposal,
        repetitions_per_candidate=7,
        acceptance_threshold=0.50,
        confidence_margin=0.20
    ):

        self.buyer = buyer

        self.reference_proposal = (
            reference_proposal
        )

        self.repetitions_per_candidate = (
            repetitions_per_candidate
        )

        self.acceptance_threshold = (
            acceptance_threshold
        )

        self.confidence_margin = (
            confidence_margin
        )

        self.query_count = 0

        self.candidate_count = 0

        self.history = []

        self.discovered_policy = {}

        self.final_intervals = {}


    # ========================================================
    # COMMERCIAL VARIABLE CONFIGURATION
    # ========================================================

    @staticmethod
    def get_variable_configurations():

        return {

            "annual_price": {

                "lower":
                    50000.0,

                "upper":
                    150000.0,

                "direction":
                    "maximum",

                "tolerance":
                    1.0

            },


            "contract_months": {

                "lower":
                    12,

                "upper":
                    60,

                "direction":
                    "maximum",

                "tolerance":
                    1

            },


            "service_availability": {

                "lower":
                    90.0,

                "upper":
                    100.0,

                "direction":
                    "minimum",

                "tolerance":
                    0.001

            },


            "payment_days": {

                "lower":
                    7,

                "upper":
                    90,

                "direction":
                    "minimum",

                "tolerance":
                    1

            },


            "supplier_reliability": {

                "lower":
                    60.0,

                "upper":
                    100.0,

                "direction":
                    "minimum",

                "tolerance":
                    0.001

            }

        }


    # ========================================================
    # REPEATED CANDIDATE EVALUATION
    # ========================================================

    def evaluate_candidate(
        self,
        variable,
        candidate_value
    ):

        proposal = replace(

            self.reference_proposal,

            **{
                variable:
                    candidate_value
            }

        )


        accepted_count = 0

        rejected_count = 0

        observations = []


        for repetition in range(

            1,

            self.repetitions_per_candidate + 1

        ):

            response = (
                self.buyer.evaluate_proposal(
                    proposal
                )
            )


            self.query_count += 1


            accepted = (

                response["decision"]
                ==
                "ACCEPTED"

            )


            if accepted:

                accepted_count += 1

            else:

                rejected_count += 1


            observations.append({

                "repetition":
                    repetition,

                "decision":
                    response[
                        "decision"
                    ]

            })


        self.candidate_count += 1


        acceptance_rate = (

            accepted_count
            /
            self.repetitions_per_candidate

        )


        aggregated_acceptance = (

            acceptance_rate
            >=
            self.acceptance_threshold

        )


        evidence_distance = abs(

            acceptance_rate
            -
            self.acceptance_threshold

        )


        confident = (

            evidence_distance
            >=
            self.confidence_margin

        )


        record = {

            "candidate_number":
                self.candidate_count,

            "variable":
                variable,

            "candidate_value":
                candidate_value,

            "accepted_observations":
                accepted_count,

            "rejected_observations":
                rejected_count,

            "acceptance_rate":
                acceptance_rate,

            "aggregated_decision":
                (
                    "ACCEPTED"

                    if aggregated_acceptance

                    else "REJECTED"
                ),

            "confident":
                confident,

            "observations":
                observations

        }


        self.history.append(
            record
        )


        print(

            f"Candidate "
            f"{self.candidate_count:03d} | "

            f"{variable:24} | "

            f"Value: "
            f"{candidate_value:12.6f} | "

            f"Accept: "
            f"{accepted_count}/"
            f"{self.repetitions_per_candidate} | "

            f"Rate: "
            f"{acceptance_rate:.3f} | "

            f"Aggregated: "
            f"{record['aggregated_decision']}"

        )


        return record


    # ========================================================
    # AGGREGATED BOOLEAN DECISION
    # ========================================================

    def candidate_is_accepted(
        self,
        variable,
        candidate_value
    ):

        record = (
            self.evaluate_candidate(

                variable,

                candidate_value

            )
        )


        return (

            record[
                "aggregated_decision"
            ]
            ==
            "ACCEPTED"

        )


    # ========================================================
    # VERIFY REFERENCE PROPOSAL
    # ========================================================

    def verify_reference_proposal(
        self
    ):

        print(
            "\nVERIFYING REFERENCE PROPOSAL "
            "WITH REPEATED EVIDENCE"
        )

        print("-" * 80)


        accepted_count = 0


        for repetition in range(

            1,

            self.repetitions_per_candidate + 1

        ):

            response = (
                self.buyer.evaluate_proposal(
                    self.reference_proposal
                )
            )


            self.query_count += 1


            if (
                response["decision"]
                ==
                "ACCEPTED"
            ):

                accepted_count += 1


        acceptance_rate = (

            accepted_count
            /
            self.repetitions_per_candidate

        )


        accepted = (

            acceptance_rate
            >=
            self.acceptance_threshold

        )


        print(
            "Reference Acceptance:",
            (
                f"{accepted_count}/"
                f"{self.repetitions_per_candidate}"
            )
        )


        print(
            "Reference Acceptance Rate:",
            round(
                acceptance_rate,
                4
            )
        )


        print(
            "Aggregated Reference Decision:",
            (
                "ACCEPTED"

                if accepted

                else "REJECTED"
            )
        )


        if not accepted:

            raise ValueError(

                "Reference proposal failed "
                "repeated-evidence validation."

            )


        return True


    # ========================================================
    # INFER ONE POLICY THRESHOLD
    # ========================================================

    def infer_threshold(
        self,
        variable,
        lower,
        upper,
        direction,
        tolerance
    ):

        print("\n" + "=" * 80)

        print(
            "REPEATED-EVIDENCE DISCOVERY:",
            variable.upper()
        )

        print("=" * 80)


        # ----------------------------------------------------
        # Establish search-boundary evidence.
        # ----------------------------------------------------

        lower_accepted = (
            self.candidate_is_accepted(

                variable,

                lower

            )
        )


        upper_accepted = (
            self.candidate_is_accepted(

                variable,

                upper

            )
        )


        # ----------------------------------------------------
        # Validate search-space orientation.
        # ----------------------------------------------------

        if direction == "maximum":

            if (
                not lower_accepted
                or
                upper_accepted
            ):

                raise ValueError(

                    "Invalid repeated-evidence "
                    f"maximum boundaries for "
                    f"{variable}."

                )


        elif direction == "minimum":

            if (
                lower_accepted
                or
                not upper_accepted
            ):

                raise ValueError(

                    "Invalid repeated-evidence "
                    f"minimum boundaries for "
                    f"{variable}."

                )


        else:

            raise ValueError(

                "Direction must be "
                "'maximum' or 'minimum'."

            )


        iterations = 0


        # ----------------------------------------------------
        # REPEATED-EVIDENCE BINARY SEARCH
        # ----------------------------------------------------

        while (

            upper - lower

            >
            tolerance

        ):

            iterations += 1


            if variable in [

                "contract_months",

                "payment_days"

            ]:

                midpoint = (

                    lower + upper

                ) // 2


                if (
                    midpoint == lower
                ):

                    break


            else:

                midpoint = (

                    lower + upper

                ) / 2


            accepted = (
                self.candidate_is_accepted(

                    variable,

                    midpoint

                )
            )


            if direction == "maximum":

                if accepted:

                    lower = midpoint

                else:

                    upper = midpoint


            else:

                if accepted:

                    upper = midpoint

                else:

                    lower = midpoint


        # ----------------------------------------------------
        # THRESHOLD ESTIMATE
        # ----------------------------------------------------

        estimated_threshold = (

            lower

            if direction == "maximum"

            else upper

        )


        interval_width = (

            upper - lower

        )


        self.discovered_policy[
            variable
        ] = estimated_threshold


        self.final_intervals[
            variable
        ] = {

            "lower_boundary":
                lower,

            "upper_boundary":
                upper,

            "interval_width":
                interval_width,

            "estimated_threshold":
                estimated_threshold,

            "iterations":
                iterations

        }


        print(
            "\nREPEATED-EVIDENCE RESULT"
        )


        print(
            "Estimated Threshold:",
            estimated_threshold
        )


        print(
            "Final Interval:",
            (
                f"[{lower}, {upper}]"
            )
        )


        print(
            "Interval Width:",
            interval_width
        )


        print(
            "Search Iterations:",
            iterations
        )


        return (

            self.final_intervals[
                variable
            ]

        )


    # ========================================================
    # DISCOVER COMPLETE BUYER POLICY
    # ========================================================

    def discover_policy(
        self
    ):

        print("\n" + "=" * 80)

        print(
            "MARS — REPEATED-EVIDENCE "
            "POLICY DISCOVERY"
        )

        print("=" * 80)


        print(
            "Repetitions per Candidate:",
            self.repetitions_per_candidate
        )


        print(
            "Acceptance Threshold:",
            self.acceptance_threshold
        )


        print(
            "Confidence Margin:",
            self.confidence_margin
        )


        self.verify_reference_proposal()


        configurations = (
            self.get_variable_configurations()
        )


        for variable, configuration in (
            configurations.items()
        ):

            self.infer_threshold(

                variable=variable,

                lower=configuration[
                    "lower"
                ],

                upper=configuration[
                    "upper"
                ],

                direction=configuration[
                    "direction"
                ],

                tolerance=configuration[
                    "tolerance"
                ]

            )


        print("\n" + "=" * 80)

        print(
            "REPEATED-EVIDENCE "
            "DISCOVERED BUYER POLICY"
        )

        print("=" * 80)


        for variable, threshold in (
            self.discovered_policy.items()
        ):

            print(

                f"{variable}: "
                f"{threshold}"

            )


        print(
            "\nCandidate Experiments:",
            self.candidate_count
        )


        print(
            "Total Buyer Queries:",
            self.query_count
        )


        return {

            "discovered_policy":
                self.discovered_policy,

            "final_intervals":
                self.final_intervals,

            "candidate_experiments":
                self.candidate_count,

            "total_queries":
                self.query_count,

            "repetitions_per_candidate":
                self.repetitions_per_candidate,

            "history":
                self.history

        }
