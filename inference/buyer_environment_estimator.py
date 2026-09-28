"""
MARS — Machine-Agent Revenue Science

Experiment 022

Latent Buyer Environment Estimator

Author: Kamran Khan

Purpose:
Estimate the behavioural uncertainty of an autonomous
buyer using only observable black-box decisions.

The estimator does NOT access:

- the buyer's private procurement thresholds
- the simulator's configured noise strength
- hidden buyer policy variables

Instead, MARS repeatedly submits controlled diagnostic
proposals and measures decision disagreement.

The resulting behavioural instability estimate can be
used by the meta-policy layer to select an appropriate
evidence-acquisition strategy.
"""

import math
import statistics
from collections import Counter
from dataclasses import asdict


# ============================================================
# BUYER ENVIRONMENT ESTIMATOR
# ============================================================

class BuyerEnvironmentEstimator:

    def __init__(
        self,
        buyer,
        diagnostic_proposals,
        observations_per_probe=15
    ):

        if observations_per_probe < 2:

            raise ValueError(
                "observations_per_probe must be at least 2."
            )

        if not diagnostic_proposals:

            raise ValueError(
                "At least one diagnostic proposal is required."
            )

        self.buyer = buyer

        self.diagnostic_proposals = (
            diagnostic_proposals
        )

        self.observations_per_probe = (
            observations_per_probe
        )

        self.observation_history = []

        self.probe_statistics = []

        self.total_queries = 0


    # ========================================================
    # NORMALISE BUYER DECISION
    # ========================================================

    @staticmethod
    def _normalise_decision(
        response
    ):

        decision = response.get(
            "decision"
        )

        if decision not in [
            "ACCEPTED",
            "REJECTED"
        ]:

            raise ValueError(
                "Buyer response must contain "
                "ACCEPTED or REJECTED decision."
            )

        return decision


    # ========================================================
    # BINARY ENTROPY
    # ========================================================

    @staticmethod
    def _binary_entropy(
        probability
    ):

        if (
            probability <= 0.0
            or
            probability >= 1.0
        ):

            return 0.0

        return -(
            probability
            *
            math.log2(
                probability
            )
            +
            (
                1.0
                -
                probability
            )
            *
            math.log2(
                1.0
                -
                probability
            )
        )


    # ========================================================
    # DECISION DISAGREEMENT
    # ========================================================

    @staticmethod
    def _decision_disagreement(
        acceptance_rate
    ):

        """
        Converts an acceptance probability into a
        behavioural disagreement score.

        0.0 means perfectly stable decisions.

        1.0 means maximum observed disagreement,
        occurring around a 50/50 split.
        """

        return (

            2.0
            *
            min(
                acceptance_rate,
                1.0 - acceptance_rate
            )

        )


    # ========================================================
    # WILSON CONFIDENCE INTERVAL
    # ========================================================

    @staticmethod
    def _wilson_interval(
        successes,
        observations,
        z=1.96
    ):

        if observations <= 0:

            return (
                0.0,
                1.0
            )

        proportion = (
            successes
            /
            observations
        )

        denominator = (
            1.0
            +
            (
                z ** 2
                /
                observations
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
                    observations
                )
            )
        )

        adjustment = (
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
                    observations
                )
                +
                (
                    z ** 2
                    /
                    (
                        4.0
                        *
                        observations ** 2
                    )
                )
            )
        )

        lower = (
            centre
            -
            adjustment
        ) / denominator

        upper = (
            centre
            +
            adjustment
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
    # OBSERVE ONE DIAGNOSTIC PROBE
    # ========================================================

    def observe_probe(
        self,
        proposal,
        probe_name
    ):

        decisions = []

        for observation_number in range(
            1,
            self.observations_per_probe + 1
        ):

            response = (
                self.buyer.evaluate_proposal(
                    proposal
                )
            )

            decision = (
                self._normalise_decision(
                    response
                )
            )

            decisions.append(
                decision
            )

            self.total_queries += 1

            self.observation_history.append(
                {
                    "probe_name":
                        probe_name,

                    "observation":
                        observation_number,

                    "proposal":
                        asdict(
                            proposal
                        ),

                    "decision":
                        decision
                }
            )

        counts = Counter(
            decisions
        )

        accepted = counts.get(
            "ACCEPTED",
            0
        )

        rejected = counts.get(
            "REJECTED",
            0
        )

        total = (
            accepted
            +
            rejected
        )

        acceptance_rate = (
            accepted
            /
            total
        )

        disagreement = (
            self._decision_disagreement(
                acceptance_rate
            )
        )

        entropy = (
            self._binary_entropy(
                acceptance_rate
            )
        )

        lower_ci, upper_ci = (
            self._wilson_interval(
                successes=accepted,
                observations=total
            )
        )

        result = {

            "probe_name":
                probe_name,

            "proposal":
                asdict(
                    proposal
                ),

            "observations":
                total,

            "accepted":
                accepted,

            "rejected":
                rejected,

            "acceptance_rate":
                acceptance_rate,

            "decision_disagreement":
                disagreement,

            "decision_entropy":
                entropy,

            "acceptance_ci_lower":
                lower_ci,

            "acceptance_ci_upper":
                upper_ci,

            "acceptance_ci_width":
                (
                    upper_ci
                    -
                    lower_ci
                )
        }

        self.probe_statistics.append(
            result
        )

        return result


    # ========================================================
    # ESTIMATE ENVIRONMENT
    # ========================================================

    def estimate_environment(
        self
    ):

        self.probe_statistics = []

        self.observation_history = []

        self.total_queries = 0

        for index, proposal in enumerate(
            self.diagnostic_proposals,
            start=1
        ):

            self.observe_probe(
                proposal=proposal,
                probe_name=(
                    f"DIAGNOSTIC_PROBE_{index}"
                )
            )

        disagreements = [
            result[
                "decision_disagreement"
            ]
            for result in self.probe_statistics
        ]

        entropies = [
            result[
                "decision_entropy"
            ]
            for result in self.probe_statistics
        ]

        confidence_widths = [
            result[
                "acceptance_ci_width"
            ]
            for result in self.probe_statistics
        ]

        acceptance_rates = [
            result[
                "acceptance_rate"
            ]
            for result in self.probe_statistics
        ]

        mean_disagreement = (
            statistics.mean(
                disagreements
            )
        )

        median_disagreement = (
            statistics.median(
                disagreements
            )
        )

        maximum_disagreement = (
            max(
                disagreements
            )
        )

        mean_entropy = (
            statistics.mean(
                entropies
            )
        )

        mean_ci_width = (
            statistics.mean(
                confidence_widths
            )
        )

        acceptance_rate_stdev = (
            statistics.stdev(
                acceptance_rates
            )
            if len(
                acceptance_rates
            ) > 1
            else 0.0
        )

        estimated_noise = (
            mean_disagreement
        )

        return {

            "estimated_noise":
                estimated_noise,

            "mean_decision_disagreement":
                mean_disagreement,

            "median_decision_disagreement":
                median_disagreement,

            "maximum_decision_disagreement":
                maximum_disagreement,

            "mean_decision_entropy":
                mean_entropy,

            "mean_acceptance_ci_width":
                mean_ci_width,

            "acceptance_rate_stdev":
                acceptance_rate_stdev,

            "diagnostic_probes":
                len(
                    self.probe_statistics
                ),

            "observations_per_probe":
                self.observations_per_probe,

            "total_diagnostic_queries":
                self.total_queries,

            "probe_statistics":
                list(
                    self.probe_statistics
                )
        }


    # ========================================================
    # ESTIMATE NOISE ONLY
    # ========================================================

    def estimate_noise(
        self
    ):

        result = (
            self.estimate_environment()
        )

        return result[
            "estimated_noise"
        ]


    # ========================================================
    # PRINT ENVIRONMENT REPORT
    # ========================================================

    def print_environment_report(
        self,
        result
    ):

        print("\n" + "=" * 80)

        print(
            "MARS — LATENT BUYER ENVIRONMENT REPORT"
        )

        print("=" * 80)

        print(
            "Estimated Behavioural Noise:",
            result[
                "estimated_noise"
            ]
        )

        print(
            "Mean Decision Disagreement:",
            result[
                "mean_decision_disagreement"
            ]
        )

        print(
            "Median Decision Disagreement:",
            result[
                "median_decision_disagreement"
            ]
        )

        print(
            "Maximum Decision Disagreement:",
            result[
                "maximum_decision_disagreement"
            ]
        )

        print(
            "Mean Decision Entropy:",
            result[
                "mean_decision_entropy"
            ]
        )

        print(
            "Mean Acceptance CI Width:",
            result[
                "mean_acceptance_ci_width"
            ]
        )

        print(
            "Diagnostic Probes:",
            result[
                "diagnostic_probes"
            ]
        )

        print(
            "Observations per Probe:",
            result[
                "observations_per_probe"
            ]
        )

        print(
            "Total Diagnostic Queries:",
            result[
                "total_diagnostic_queries"
            ]
        )

        print("\nPROBE-LEVEL DIAGNOSTICS")
        print("-" * 80)

        for probe in result[
            "probe_statistics"
        ]:

            print(
                f"{probe['probe_name']} | "
                f"Accepted: "
                f"{probe['accepted']} | "
                f"Rejected: "
                f"{probe['rejected']} | "
                f"Acceptance Rate: "
                f"{probe['acceptance_rate']:.4f} | "
                f"Disagreement: "
                f"{probe['decision_disagreement']:.4f} | "
                f"Entropy: "
                f"{probe['decision_entropy']:.4f}"
            )

        print("=" * 80)
