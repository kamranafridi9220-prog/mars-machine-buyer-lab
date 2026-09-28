"""
MARS — Machine-Agent Revenue Science

Experiment 023

Active Diagnostic Intelligence Engine

Author: Kamran Khan

Purpose:
Actively diagnose the behavioural environment of an
unknown autonomous buyer while minimizing unnecessary
buyer interactions.

Unlike Experiment 022, which evaluates every diagnostic
proposal a fixed number of times, this engine decides:

1. Which diagnostic probe should be evaluated next.
2. How many observations should be collected.
3. Whether additional evidence is still informative.
4. When environment diagnosis should stop.

The engine does NOT access:

- simulator noise strength
- hidden buyer thresholds
- private buyer decision rules

It operates only on observable buyer decisions.
"""

import math
import statistics
from collections import Counter


class ActiveDiagnosticIntelligenceEngine:

    def __init__(
        self,
        buyer,
        named_probes,
        candidate_noise_levels=None,
        minimum_observations_per_probe=3,
        maximum_observations_per_probe=15,
        batch_size=2,
        minimum_total_queries=20,
        maximum_total_queries=120,
        confidence_threshold=0.80,
        stability_threshold=0.03
    ):

        if candidate_noise_levels is None:

            candidate_noise_levels = [
                0.05,
                0.10,
                0.15,
                0.20,
                0.25,
                0.30
            ]

        if not named_probes:

            raise ValueError(
                "At least one diagnostic probe is required."
            )

        if minimum_observations_per_probe < 1:

            raise ValueError(
                "minimum_observations_per_probe must "
                "be at least 1."
            )

        if maximum_observations_per_probe < (
            minimum_observations_per_probe
        ):

            raise ValueError(
                "maximum_observations_per_probe cannot "
                "be lower than minimum_observations_per_probe."
            )

        if batch_size < 1:

            raise ValueError(
                "batch_size must be at least 1."
            )

        if maximum_total_queries < minimum_total_queries:

            raise ValueError(
                "maximum_total_queries cannot be lower "
                "than minimum_total_queries."
            )

        self.buyer = buyer

        self.named_probes = (
            named_probes
        )

        self.candidate_noise_levels = sorted(
            float(level)
            for level in candidate_noise_levels
        )

        self.minimum_observations_per_probe = (
            minimum_observations_per_probe
        )

        self.maximum_observations_per_probe = (
            maximum_observations_per_probe
        )

        self.batch_size = (
            batch_size
        )

        self.minimum_total_queries = (
            minimum_total_queries
        )

        self.maximum_total_queries = (
            maximum_total_queries
        )

        self.confidence_threshold = (
            confidence_threshold
        )

        self.stability_threshold = (
            stability_threshold
        )

        self.total_queries = 0

        self.round_number = 0

        self.observation_history = []

        self.selection_history = []

        self.belief_history = []

        self.probe_states = {}

        self.environment_belief = {}

        self._initialise_probe_states()

        self._initialise_environment_belief()


    # ========================================================
    # INITIALISE PROBE STATES
    # ========================================================

    def _initialise_probe_states(
        self
    ):

        for probe in self.named_probes:

            name = probe[
                "name"
            ]

            self.probe_states[
                name
            ] = {

                "name":
                    name,

                "variable":
                    probe.get(
                        "variable"
                    ),

                "probe_type":
                    probe.get(
                        "probe_type"
                    ),

                "proposal":
                    probe[
                        "proposal"
                    ],

                "accepted":
                    0,

                "rejected":
                    0,

                "observations":
                    0,

                "acceptance_rate":
                    None,

                "minority_rate":
                    None,

                "disagreement":
                    None,

                "entropy":
                    None,

                "priority":
                    1.0
            }


    # ========================================================
    # INITIALISE ENVIRONMENT BELIEF
    # ========================================================

    def _initialise_environment_belief(
        self
    ):

        probability = (
            1.0
            /
            len(
                self.candidate_noise_levels
            )
        )

        self.environment_belief = {

            noise:
                probability

            for noise in (
                self.candidate_noise_levels
            )
        }


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
                "ACCEPTED or REJECTED."
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
    # BELIEF ENTROPY
    # ========================================================

    def _belief_entropy(
        self
    ):

        entropy = 0.0

        for probability in (
            self.environment_belief.values()
        ):

            if probability > 0.0:

                entropy -= (
                    probability
                    *
                    math.log2(
                        probability
                    )
                )

        return entropy


    # ========================================================
    # UPDATE PROBE STATISTICS
    # ========================================================

    def _update_probe_statistics(
        self,
        probe_state
    ):

        observations = (
            probe_state[
                "observations"
            ]
        )

        if observations <= 0:

            return

        accepted = (
            probe_state[
                "accepted"
            ]
        )

        rejected = (
            probe_state[
                "rejected"
            ]
        )

        acceptance_rate = (
            accepted
            /
            observations
        )

        minority_rate = (
            min(
                accepted,
                rejected
            )
            /
            observations
        )

        disagreement = (
            2.0
            *
            minority_rate
        )

        entropy = (
            self._binary_entropy(
                acceptance_rate
            )
        )

        probe_state[
            "acceptance_rate"
        ] = acceptance_rate

        probe_state[
            "minority_rate"
        ] = minority_rate

        probe_state[
            "disagreement"
        ] = disagreement

        probe_state[
            "entropy"
        ] = entropy


    # ========================================================
    # OBSERVE PROBE
    # ========================================================

    def _observe_probe(
        self,
        probe_name,
        observations_to_collect
    ):

        probe_state = (
            self.probe_states[
                probe_name
            ]
        )

        remaining_probe_capacity = (
            self.maximum_observations_per_probe
            -
            probe_state[
                "observations"
            ]
        )

        remaining_global_capacity = (
            self.maximum_total_queries
            -
            self.total_queries
        )

        observations_to_collect = min(
            observations_to_collect,
            remaining_probe_capacity,
            remaining_global_capacity
        )

        if observations_to_collect <= 0:

            return 0

        collected = 0

        for _ in range(
            observations_to_collect
        ):

            response = (
                self.buyer.evaluate_proposal(
                    probe_state[
                        "proposal"
                    ]
                )
            )

            decision = (
                self._normalise_decision(
                    response
                )
            )

            if decision == "ACCEPTED":

                probe_state[
                    "accepted"
                ] += 1

            else:

                probe_state[
                    "rejected"
                ] += 1

            probe_state[
                "observations"
            ] += 1

            self.total_queries += 1

            collected += 1

            self.observation_history.append(
                {
                    "round":
                        self.round_number,

                    "probe_name":
                        probe_name,

                    "decision":
                        decision,

                    "total_queries":
                        self.total_queries
                }
            )

        self._update_probe_statistics(
            probe_state
        )

        return collected


    # ========================================================
    # BOOTSTRAP DIAGNOSTICS
    # ========================================================

    def _bootstrap(
        self
    ):

        """
        Give every probe a small initial evidence base.

        This prevents the active selector from making its
        first decision using completely unobserved probes.
        """

        for probe_name in (
            self.probe_states
        ):

            if (
                self.total_queries
                >=
                self.maximum_total_queries
            ):

                break

            probe_state = (
                self.probe_states[
                    probe_name
                ]
            )

            required = (
                self.minimum_observations_per_probe
                -
                probe_state[
                    "observations"
                ]
            )

            if required > 0:

                self._observe_probe(
                    probe_name,
                    required
                )


    # ========================================================
    # ESTIMATE OBSERVED INSTABILITY
    # ========================================================

    def estimate_observed_instability(
        self
    ):

        minority_rates = []

        weights = []

        for probe_state in (
            self.probe_states.values()
        ):

            if (
                probe_state[
                    "observations"
                ]
                <= 0
            ):

                continue

            minority_rate = (
                probe_state[
                    "minority_rate"
                ]
            )

            if minority_rate is None:

                continue

            minority_rates.append(
                minority_rate
            )

            weights.append(
                probe_state[
                    "observations"
                ]
            )

        if not minority_rates:

            return 0.0

        weighted_total = sum(

            rate
            *
            weight

            for rate, weight in zip(
                minority_rates,
                weights
            )
        )

        total_weight = sum(
            weights
        )

        if total_weight <= 0:

            return 0.0

        return (
            weighted_total
            /
            total_weight
        )


    # ========================================================
    # NOISE LIKELIHOOD
    # ========================================================

    @staticmethod
    def _noise_likelihood(
        observed_instability,
        candidate_noise
    ):

        """
        Approximate likelihood kernel.

        Experiment 023 deliberately treats the candidate
        noise regimes as latent environment hypotheses.

        The width prevents the posterior from becoming
        unrealistically certain after only a few queries.
        """

        sigma = 0.075

        difference = (
            observed_instability
            -
            candidate_noise
        )

        exponent = -(
            difference ** 2
        ) / (
            2.0
            *
            sigma ** 2
        )

        return math.exp(
            exponent
        )


    # ========================================================
    # UPDATE ENVIRONMENT BELIEF
    # ========================================================

    def update_environment_belief(
        self
    ):

        observed_instability = (
            self.estimate_observed_instability()
        )

        posterior = {}

        for noise_level in (
            self.candidate_noise_levels
        ):

            prior = (
                self.environment_belief[
                    noise_level
                ]
            )

            likelihood = (
                self._noise_likelihood(
                    observed_instability,
                    noise_level
                )
            )

            posterior[
                noise_level
            ] = (
                prior
                *
                likelihood
            )

        normaliser = sum(
            posterior.values()
        )

        if normaliser <= 0:

            probability = (
                1.0
                /
                len(
                    self.candidate_noise_levels
                )
            )

            posterior = {

                noise:
                    probability

                for noise in (
                    self.candidate_noise_levels
                )
            }

        else:

            posterior = {

                noise:
                    value
                    /
                    normaliser

                for noise, value in (
                    posterior.items()
                )
            }

        self.environment_belief = (
            posterior
        )

        self.belief_history.append(
            {
                "round":
                    self.round_number,

                "queries":
                    self.total_queries,

                "observed_instability":
                    observed_instability,

                "belief":
                    dict(
                        posterior
                    ),

                "entropy":
                    self._belief_entropy()
            }
        )

        return posterior


    # ========================================================
    # CURRENT ENVIRONMENT ESTIMATE
    # ========================================================

    def get_environment_estimate(
        self
    ):

        expected_noise = sum(

            noise
            *
            probability

            for noise, probability in (
                self.environment_belief.items()
            )
        )

        most_likely_noise = max(
            self.environment_belief,
            key=self.environment_belief.get
        )

        confidence = (
            self.environment_belief[
                most_likely_noise
            ]
        )

        return {

            "estimated_noise":
                expected_noise,

            "most_likely_noise":
                most_likely_noise,

            "confidence":
                confidence,

            "belief_entropy":
                self._belief_entropy(),

            "belief":
                dict(
                    self.environment_belief
                )
        }


    # ========================================================
    # PROBE PRIORITY
    # ========================================================

    def calculate_probe_priority(
        self,
        probe_state
    ):

        observations = (
            probe_state[
                "observations"
            ]
        )

        if observations <= 0:

            return 1.0

        if observations >= (
            self.maximum_observations_per_probe
        ):

            return -1.0

        entropy = (
            probe_state[
                "entropy"
            ]
        )

        if entropy is None:

            entropy = 1.0

        disagreement = (
            probe_state[
                "disagreement"
            ]
        )

        if disagreement is None:

            disagreement = 1.0

        uncertainty_component = (
            0.55
            *
            entropy
        )

        disagreement_component = (
            0.30
            *
            disagreement
        )

        evidence_scarcity = (
            1.0
            -
            (
                observations
                /
                self.maximum_observations_per_probe
            )
        )

        scarcity_component = (
            0.15
            *
            evidence_scarcity
        )

        priority = (
            uncertainty_component
            +
            disagreement_component
            +
            scarcity_component
        )

        return priority


    # ========================================================
    # SELECT NEXT PROBE
    # ========================================================

    def select_next_probe(
        self
    ):

        candidates = []

        for probe_name, probe_state in (
            self.probe_states.items()
        ):

            priority = (
                self.calculate_probe_priority(
                    probe_state
                )
            )

            probe_state[
                "priority"
            ] = priority

            if priority >= 0.0:

                candidates.append(
                    (
                        priority,
                        probe_name
                    )
                )

        if not candidates:

            return None

        candidates.sort(
            key=lambda item: (
                -item[0],
                item[1]
            )
        )

        selected_priority, selected_name = (
            candidates[0]
        )

        self.selection_history.append(
            {
                "round":
                    self.round_number,

                "probe_name":
                    selected_name,

                "priority":
                    selected_priority,

                "queries_before":
                    self.total_queries
            }
        )

        return selected_name


    # ========================================================
    # ESTIMATE STABILITY
    # ========================================================

    def estimate_recent_stability(
        self
    ):

        if len(
            self.belief_history
        ) < 2:

            return None

        previous = (
            self.belief_history[
                -2
            ][
                "observed_instability"
            ]
        )

        current = (
            self.belief_history[
                -1
            ][
                "observed_instability"
            ]
        )

        return abs(
            current
            -
            previous
        )


    # ========================================================
    # STOPPING RULE
    # ========================================================

    def should_stop(
        self
    ):

        if (
            self.total_queries
            >=
            self.maximum_total_queries
        ):

            return (
                True,
                "MAXIMUM_QUERY_BUDGET"
            )

        if (
            self.total_queries
            <
            self.minimum_total_queries
        ):

            return (
                False,
                "MINIMUM_EVIDENCE_NOT_REACHED"
            )

        estimate = (
            self.get_environment_estimate()
        )

        confidence = (
            estimate[
                "confidence"
            ]
        )

        stability = (
            self.estimate_recent_stability()
        )

        if (
            confidence
            >=
            self.confidence_threshold
            and
            stability is not None
            and
            stability
            <=
            self.stability_threshold
        ):

            return (
                True,
                "CONFIDENT_AND_STABLE"
            )

        all_probes_exhausted = all(

            probe_state[
                "observations"
            ]
            >=
            self.maximum_observations_per_probe

            for probe_state in (
                self.probe_states.values()
            )
        )

        if all_probes_exhausted:

            return (
                True,
                "ALL_PROBES_EXHAUSTED"
            )

        return (
            False,
            "MORE_INFORMATION_REQUIRED"
        )


    # ========================================================
    # RUN ACTIVE DIAGNOSIS
    # ========================================================

    def diagnose(
        self
    ):

        self._bootstrap()

        self.round_number += 1

        self.update_environment_belief()

        stop, reason = (
            self.should_stop()
        )

        while not stop:

            selected_probe = (
                self.select_next_probe()
            )

            if selected_probe is None:

                reason = (
                    "NO_AVAILABLE_PROBES"
                )

                break

            self.round_number += 1

            collected = (
                self._observe_probe(
                    selected_probe,
                    self.batch_size
                )
            )

            if collected <= 0:

                reason = (
                    "NO_QUERY_CAPACITY"
                )

                break

            self.update_environment_belief()

            stop, reason = (
                self.should_stop()
            )

        estimate = (
            self.get_environment_estimate()
        )

        active_probes = sum(

            1

            for probe_state in (
                self.probe_states.values()
            )

            if probe_state[
                "observations"
            ] > 0
        )

        exhausted_probes = sum(

            1

            for probe_state in (
                self.probe_states.values()
            )

            if probe_state[
                "observations"
            ]
            >=
            self.maximum_observations_per_probe
        )

        probe_statistics = {}

        for probe_name, probe_state in (
            self.probe_states.items()
        ):

            probe_statistics[
                probe_name
            ] = {

                key:
                    value

                for key, value in (
                    probe_state.items()
                )

                if key != "proposal"
            }

        return {

            "estimated_noise":
                estimate[
                    "estimated_noise"
                ],

            "most_likely_noise":
                estimate[
                    "most_likely_noise"
                ],

            "environment_confidence":
                estimate[
                    "confidence"
                ],

            "belief_entropy":
                estimate[
                    "belief_entropy"
                ],

            "environment_belief":
                estimate[
                    "belief"
                ],

            "observed_instability":
                self.estimate_observed_instability(),

            "total_diagnostic_queries":
                self.total_queries,

            "diagnostic_probes":
                active_probes,

            "exhausted_probes":
                exhausted_probes,

            "observations_per_probe":
                None,

            "stopping_reason":
                reason,

            "rounds":
                self.round_number,

            "probe_statistics":
                probe_statistics,

            "selection_history":
                list(
                    self.selection_history
                ),

            "belief_history":
                list(
                    self.belief_history
                )
        }


    # ========================================================
    # PRINT REPORT
    # ========================================================

    def print_report(
        self,
        result
    ):

        print(
            "\n"
            +
            "=" * 80
        )

        print(
            "MARS — ACTIVE DIAGNOSTIC INTELLIGENCE"
        )

        print(
            "=" * 80
        )

        print(
            "Estimated Noise:",
            f"{result['estimated_noise']:.6f}"
        )

        print(
            "Most Likely Noise Regime:",
            f"{result['most_likely_noise']:.2f}"
        )

        print(
            "Environment Confidence:",
            f"{result['environment_confidence']:.4f}"
        )

        print(
            "Observed Instability:",
            f"{result['observed_instability']:.6f}"
        )

        print(
            "Belief Entropy:",
            f"{result['belief_entropy']:.6f}"
        )

        print(
            "Diagnostic Queries:",
            result[
                "total_diagnostic_queries"
            ]
        )

        print(
            "Active Probes:",
            result[
                "diagnostic_probes"
            ]
        )

        print(
            "Stopping Reason:",
            result[
                "stopping_reason"
            ]
        )

        print(
            "Diagnostic Rounds:",
            result[
                "rounds"
            ]
        )

        print(
            "=" * 80
        )
