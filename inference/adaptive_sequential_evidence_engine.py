"""
MARS — Machine-Agent Revenue Science

Experiment 019

Adaptive Sequential Evidence Acquisition Engine

Author: Kamran Khan

Purpose:
Discover hidden autonomous buyer policies under
stochastic decision noise while dynamically deciding
how many buyer observations are required for each
candidate commercial proposal.

Research Objective:
Reduce the query cost of fixed repeated-evidence
policy discovery while preserving robustness against
noisy buyer decisions.

Core Principle:
Do not allocate the same number of observations to
every candidate.

Easy candidates should terminate early.

Ambiguous candidates near hidden policy boundaries
should receive additional observations.
"""

import math

from dataclasses import replace


# ============================================================
# ADAPTIVE SEQUENTIAL EVIDENCE ENGINE
# ============================================================

class AdaptiveSequentialEvidenceEngine:

    def __init__(
        self,
        buyer,
        reference_proposal,
        minimum_observations=3,
        maximum_observations=9,
        confidence_level=0.90,
        acceptance_threshold=0.50
    ):

        self.buyer = buyer

        self.reference_proposal = (
            reference_proposal
        )

        self.minimum_observations = (
            minimum_observations
        )

        self.maximum_observations = (
            maximum_observations
        )

        self.confidence_level = (
            confidence_level
        )

        self.acceptance_threshold = (
            acceptance_threshold
        )


        if (
            self.minimum_observations
            <
            1
        ):

            raise ValueError(
                "minimum_observations must be >= 1"
            )


        if (
            self.maximum_observations
            <
            self.minimum_observations
        ):

            raise ValueError(
                "maximum_observations must be "
                ">= minimum_observations"
            )


        if not (
            0.0
            <
            self.acceptance_threshold
            <
            1.0
        ):

            raise ValueError(
                "acceptance_threshold must be "
                "between 0 and 1"
            )


        self.query_count = 0

        self.candidate_count = 0

        self.early_stop_count = 0

        self.maximum_sample_count = 0

        self.history = []

        self.discovered_policy = {}

        self.final_intervals = {}


    # ========================================================
    # VARIABLE CONFIGURATIONS
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
    # Z-SCORE
    # ========================================================

    def _z_score(
        self
    ):

        # ----------------------------------------------------
        # Confidence levels used by Experiment 019.
        #
        # This avoids introducing scipy as a dependency.
        # ----------------------------------------------------

        confidence_map = {

            0.80:
                1.2816,

            0.85:
                1.4395,

            0.90:
                1.6449,

            0.95:
                1.9600,

            0.98:
                2.3263,

            0.99:
                2.5758

        }


        closest_level = min(

            confidence_map.keys(),

            key=lambda level: abs(
                level
                -
                self.confidence_level
            )

        )


        return confidence_map[
            closest_level
        ]


    # ========================================================
    # WILSON CONFIDENCE INTERVAL
    # ========================================================

    def _wilson_interval(
        self,
        accepted_count,
        total_count
    ):

        if total_count == 0:

            return (
                0.0,
                1.0
            )


        z = self._z_score()


        proportion = (

            accepted_count
            /
            total_count

        )


        denominator = (

            1.0
            +
            (
                z ** 2
                /
                total_count
            )

        )


        centre = (

            proportion
            +
            (
                z ** 2
                /
                (
                    2.0
                    *
                    total_count
                )
            )

        )


        margin = (

            z
            *
            math.sqrt(

                (
                    proportion
                    *
                    (
                        1.0
                        -
                        proportion
                    )
                    /
                    total_count
                )

                +

                (
                    z ** 2
                    /
                    (
                        4.0
                        *
                        (
                            total_count ** 2
                        )
                    )
                )

            )

        )


        lower = (

            centre
            -
            margin

        ) / denominator


        upper = (

            centre
            +
            margin

        ) / denominator


        return (

            max(
                0.0,
                lower
            ),

            min(
                1.0,
                upper
            )

        )


    # ========================================================
    # CONFIDENCE DECISION
    # ========================================================

    def _confidence_decision(
        self,
        accepted_count,
        total_count
    ):

        lower, upper = (
            self._wilson_interval(

                accepted_count,

                total_count

            )
        )


        if (
            lower
            >
            self.acceptance_threshold
        ):

            return {

                "confident":
                    True,

                "decision":
                    "ACCEPTED",

                "lower_confidence":
                    lower,

                "upper_confidence":
                    upper

            }


        if (
            upper
            <
            self.acceptance_threshold
        ):

            return {

                "confident":
                    True,

                "decision":
                    "REJECTED",

                "lower_confidence":
                    lower,

                "upper_confidence":
                    upper

            }


        return {

            "confident":
                False,

            "decision":
                None,

            "lower_confidence":
                lower,

            "upper_confidence":
                upper

        }


    # ========================================================
    # FINAL MAJORITY DECISION
    # ========================================================

    def _majority_decision(
        self,
        accepted_count,
        total_count
    ):

        acceptance_rate = (

            accepted_count
            /
            total_count

        )


        return (

            "ACCEPTED"

            if (
                acceptance_rate
                >=
                self.acceptance_threshold
            )

            else "REJECTED"

        )


    # ========================================================
    # ADAPTIVE CANDIDATE EVALUATION
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

        final_decision = None

        confidence_result = None

        stopped_early = False


        for observation_number in range(

            1,

            self.maximum_observations + 1

        ):

            response = (
                self.buyer.evaluate_proposal(
                    proposal
                )
            )


            self.query_count += 1


            decision = response[
                "decision"
            ]


            if decision == "ACCEPTED":

                accepted_count += 1

            else:

                rejected_count += 1


            observations.append({

                "observation":
                    observation_number,

                "decision":
                    decision

            })


            # ------------------------------------------------
            # Do not assess stopping before minimum evidence.
            # ------------------------------------------------

            if (
                observation_number
                <
                self.minimum_observations
            ):

                continue


            confidence_result = (
                self._confidence_decision(

                    accepted_count,

                    observation_number

                )
            )


            # ------------------------------------------------
            # Sequential stopping rule
            # ------------------------------------------------

            if confidence_result[
                "confident"
            ]:

                final_decision = (
                    confidence_result[
                        "decision"
                    ]
                )


                stopped_early = (

                    observation_number
                    <
                    self.maximum_observations

                )


                break


        total_observations = len(
            observations
        )


        # ----------------------------------------------------
        # If confidence never separated from 0.50, use the
        # aggregate majority after maximum evidence.
        # ----------------------------------------------------

        if final_decision is None:

            final_decision = (
                self._majority_decision(

                    accepted_count,

                    total_observations

                )
            )


            confidence_result = (
                self._confidence_decision(

                    accepted_count,

                    total_observations

                )
            )


        if stopped_early:

            self.early_stop_count += 1

        else:

            self.maximum_sample_count += 1


        self.candidate_count += 1


        acceptance_rate = (

            accepted_count
            /
            total_observations

        )


        record = {

            "candidate_number":
                self.candidate_count,

            "variable":
                variable,

            "candidate_value":
                candidate_value,

            "observations_used":
                total_observations,

            "accepted_observations":
                accepted_count,

            "rejected_observations":
                rejected_count,

            "acceptance_rate":
                acceptance_rate,

            "decision":
                final_decision,

            "statistically_confident":
                confidence_result[
                    "confident"
                ],

            "lower_confidence":
                confidence_result[
                    "lower_confidence"
                ],

            "upper_confidence":
                confidence_result[
                    "upper_confidence"
                ],

            "stopped_early":
                stopped_early,

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

            f"Obs: "
            f"{total_observations:2d} | "

            f"Accept: "
            f"{accepted_count:2d} | "

            f"Reject: "
            f"{rejected_count:2d} | "

            f"Rate: "
            f"{acceptance_rate:.3f} | "

            f"Decision: "
            f"{final_decision:8} | "

            f"Early Stop: "
            f"{stopped_early}"

        )


        return record


    # ========================================================
    # BOOLEAN CANDIDATE DECISION
    # ========================================================

    def candidate_is_accepted(
        self,
        variable,
        candidate_value
    ):

        result = (
            self.evaluate_candidate(

                variable,

                candidate_value

            )
        )


        return (

            result["decision"]
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
            "WITH ADAPTIVE EVIDENCE"
        )

        print("-" * 80)


        accepted_count = 0

        observations = 0

        final_decision = None


        for observation_number in range(

            1,

            self.maximum_observations + 1

        ):

            response = (
                self.buyer.evaluate_proposal(
                    self.reference_proposal
                )
            )


            self.query_count += 1

            observations += 1


            if (
                response["decision"]
                ==
                "ACCEPTED"
            ):

                accepted_count += 1


            if (
                observation_number
                <
                self.minimum_observations
            ):

                continue


            confidence_result = (
                self._confidence_decision(

                    accepted_count,

                    observation_number

                )
            )


            if confidence_result[
                "confident"
            ]:

                final_decision = (
                    confidence_result[
                        "decision"
                    ]
                )

                break


        if final_decision is None:

            final_decision = (
                self._majority_decision(

                    accepted_count,

                    observations

                )
            )


        print(
            "Reference Observations:",
            observations
        )


        print(
            "Reference Acceptances:",
            accepted_count
        )


        print(
            "Reference Decision:",
            final_decision
        )


        if (
            final_decision
            !=
            "ACCEPTED"
        ):

            raise ValueError(

                "Reference proposal failed "
                "adaptive-evidence validation."

            )


        return True


    # ========================================================
    # INFER ONE THRESHOLD
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
            "ADAPTIVE SEQUENTIAL DISCOVERY:",
            variable.upper()
        )

        print("=" * 80)


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
        # Validate boundary orientation.
        # ----------------------------------------------------

        if direction == "maximum":

            if (
                not lower_accepted
                or
                upper_accepted
            ):

                raise ValueError(

                    "Invalid adaptive-evidence "
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

                    "Invalid adaptive-evidence "
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
        # ADAPTIVE-EVIDENCE BINARY SEARCH
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


                if midpoint == lower:

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
            "\nADAPTIVE-EVIDENCE RESULT"
        )


        print(
            "Estimated Threshold:",
            estimated_threshold
        )


        print(
            "Final Interval:",
            f"[{lower}, {upper}]"
        )


        print(
            "Interval Width:",
            interval_width
        )


        return (

            self.final_intervals[
                variable
            ]

        )


    # ========================================================
    # COMPLETE POLICY DISCOVERY
    # ========================================================

    def discover_policy(
        self
    ):

        print("\n" + "=" * 80)

        print(
            "MARS — ADAPTIVE SEQUENTIAL "
            "EVIDENCE DISCOVERY"
        )

        print("=" * 80)


        print(
            "Minimum Observations:",
            self.minimum_observations
        )


        print(
            "Maximum Observations:",
            self.maximum_observations
        )


        print(
            "Confidence Level:",
            self.confidence_level
        )


        print(
            "Acceptance Threshold:",
            self.acceptance_threshold
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


        average_observations = (

            sum(

                record[
                    "observations_used"
                ]

                for record in self.history

            )
            /
            len(
                self.history
            )

            if self.history

            else 0.0

        )


        early_stop_rate = (

            self.early_stop_count
            /
            self.candidate_count

            if self.candidate_count

            else 0.0

        )


        print("\n" + "=" * 80)

        print(
            "ADAPTIVE SEQUENTIAL "
            "DISCOVERY SUMMARY"
        )

        print("=" * 80)


        print(
            "Candidate Experiments:",
            self.candidate_count
        )


        print(
            "Total Buyer Queries:",
            self.query_count
        )


        print(
            "Average Observations "
            "per Candidate:",
            round(
                average_observations,
                4
            )
        )


        print(
            "Early Stops:",
            self.early_stop_count
        )


        print(
            "Maximum-Sample Candidates:",
            self.maximum_sample_count
        )


        print(
            "Early Stop Rate:",
            round(
                early_stop_rate,
                6
            )
        )


        print(
            "\nDISCOVERED BUYER POLICY"
        )


        for variable, threshold in (
            self.discovered_policy.items()
        ):

            print(
                f"{variable}: "
                f"{threshold}"
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

            "average_observations_per_candidate":
                average_observations,

            "early_stop_count":
                self.early_stop_count,

            "maximum_sample_count":
                self.maximum_sample_count,

            "early_stop_rate":
                early_stop_rate,

            "history":
                self.history

        }
