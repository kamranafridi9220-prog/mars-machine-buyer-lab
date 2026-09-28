"""
MARS — Machine-Agent Revenue Science

Experiment 022

Dynamic Meta-Policy Controller

Author: Kamran Khan

Purpose:
Select an evidence-acquisition strategy for an unknown
autonomous buyer using an inferred behavioural environment
rather than direct access to the simulator's hidden
noise-strength parameter.

The controller receives observable behavioural evidence
from the BuyerEnvironmentEstimator and maps that evidence
to the learned sampling policies established by the
MetaPolicyLearningEngine.

Important:
The MetaPolicyLearningEngine stores learned environment
results in `environment_statistics`.

The controller therefore reads the trained noise regimes
from that structure rather than expecting a separate
`learned_policy` attribute.
"""


class DynamicMetaPolicyController:

    def __init__(
        self,
        meta_policy_engine
    ):

        self.meta_policy_engine = (
            meta_policy_engine
        )

        self.selection_history = []


    # ========================================================
    # AVAILABLE TRAINED NOISE REGIMES
    # ========================================================

    def get_trained_noise_regimes(
        self
    ):

        environment_statistics = getattr(
            self.meta_policy_engine,
            "environment_statistics",
            None
        )

        if not environment_statistics:

            raise ValueError(
                "Meta-policy engine has no learned "
                "environment statistics. "
                "Run learn_meta_policy() before "
                "dynamic selection."
            )

        regimes = []

        for noise_level in (
            environment_statistics.keys()
        ):

            regimes.append(
                float(
                    noise_level
                )
            )

        if not regimes:

            raise ValueError(
                "No trained noise regimes are available."
            )

        return sorted(
            regimes
        )


    # ========================================================
    # CLAMP ESTIMATE
    # ========================================================

    def clamp_noise_estimate(
        self,
        estimated_noise
    ):

        regimes = (
            self.get_trained_noise_regimes()
        )

        minimum_noise = min(
            regimes
        )

        maximum_noise = max(
            regimes
        )

        estimated_noise = float(
            estimated_noise
        )

        return max(
            minimum_noise,
            min(
                maximum_noise,
                estimated_noise
            )
        )


    # ========================================================
    # FIND NEAREST TRAINED ENVIRONMENT
    # ========================================================

    def find_nearest_noise_regime(
        self,
        estimated_noise
    ):

        clamped_noise = (
            self.clamp_noise_estimate(
                estimated_noise
            )
        )

        regimes = (
            self.get_trained_noise_regimes()
        )

        nearest = min(
            regimes,
            key=lambda regime: (
                abs(
                    regime
                    -
                    clamped_noise
                ),
                regime
            )
        )

        return nearest


    # ========================================================
    # CLASSIFY ENVIRONMENT
    # ========================================================

    @staticmethod
    def classify_environment(
        estimated_noise
    ):

        noise = float(
            estimated_noise
        )

        if noise < 0.10:

            return "LOW_INSTABILITY"

        if noise < 0.20:

            return "MODERATE_INSTABILITY"

        if noise < 0.30:

            return "HIGH_INSTABILITY"

        return "VERY_HIGH_INSTABILITY"


    # ========================================================
    # CALCULATE ESTIMATION CONFIDENCE
    # ========================================================

    @staticmethod
    def calculate_estimation_confidence(
        environment_result
    ):

        ci_width = float(
            environment_result.get(
                "mean_acceptance_ci_width",
                1.0
            )
        )

        probe_count = int(
            environment_result.get(
                "diagnostic_probes",
                0
            )
        )

        observations_per_probe = int(
            environment_result.get(
                "observations_per_probe",
                0
            )
        )

        total_observations = (
            probe_count
            *
            observations_per_probe
        )

        interval_component = max(
            0.0,
            min(
                1.0,
                1.0 - ci_width
            )
        )

        observation_component = min(
            1.0,
            total_observations
            /
            240.0
        )

        confidence = (
            0.70
            *
            interval_component
            +
            0.30
            *
            observation_component
        )

        return max(
            0.0,
            min(
                1.0,
                confidence
            )
        )


    # ========================================================
    # SELECT POLICY
    # ========================================================

    def select_policy(
        self,
        environment_result
    ):

        if "estimated_noise" not in (
            environment_result
        ):

            raise ValueError(
                "Environment result does not contain "
                "estimated_noise."
            )

        estimated_noise = float(
            environment_result[
                "estimated_noise"
            ]
        )

        nearest_regime = (
            self.find_nearest_noise_regime(
                estimated_noise
            )
        )

        environment_class = (
            self.classify_environment(
                estimated_noise
            )
        )

        estimation_confidence = (
            self.calculate_estimation_confidence(
                environment_result
            )
        )

        # ----------------------------------------------------
        # IMPORTANT
        #
        # select_policy() belongs to the Experiment 021
        # MetaPolicyLearningEngine.
        #
        # It chooses the learned policy associated with
        # the nearest trained noise environment.
        #
        # The TRUE simulator noise is never passed here.
        # ----------------------------------------------------

        selection = (
            self.meta_policy_engine.select_policy(
                estimated_noise=nearest_regime
            )
        )

        selected_policy = (
            selection[
                "selected_policy"
            ]
        )

        result = {

            "raw_estimated_noise":
                estimated_noise,

            "nearest_trained_noise_regime":
                nearest_regime,

            "environment_class":
                environment_class,

            "estimation_confidence":
                estimation_confidence,

            "selected_policy":
                selected_policy,

            "selected_policy_name":
                selected_policy.name,

            "minimum_observations":
                selected_policy.minimum_observations,

            "maximum_observations":
                selected_policy.maximum_observations,

            "confidence_level":
                selected_policy.confidence_level,

            "training_objective_cost":
                selection.get(
                    "training_objective_cost"
                )
        }

        self.selection_history.append(
            result
        )

        return result


    # ========================================================
    # POLICY CHANGE DETECTION
    # ========================================================

    def policy_changed(
        self
    ):

        if len(
            self.selection_history
        ) < 2:

            return False

        previous = (
            self.selection_history[
                -2
            ][
                "selected_policy_name"
            ]
        )

        current = (
            self.selection_history[
                -1
            ][
                "selected_policy_name"
            ]
        )

        return (
            previous
            !=
            current
        )


    # ========================================================
    # GET CURRENT POLICY
    # ========================================================

    def get_current_policy(
        self
    ):

        if not self.selection_history:

            return None

        return (
            self.selection_history[
                -1
            ]
        )


    # ========================================================
    # GENERATE CONTROLLER SUMMARY
    # ========================================================

    def generate_summary(
        self
    ):

        if not self.selection_history:

            return {

                "selections":
                    0,

                "policy_changes":
                    0,

                "current_policy":
                    None,

                "history":
                    []
            }

        policy_changes = 0

        for index in range(
            1,
            len(
                self.selection_history
            )
        ):

            previous = (
                self.selection_history[
                    index - 1
                ][
                    "selected_policy_name"
                ]
            )

            current = (
                self.selection_history[
                    index
                ][
                    "selected_policy_name"
                ]
            )

            if previous != current:

                policy_changes += 1

        return {

            "selections":
                len(
                    self.selection_history
                ),

            "policy_changes":
                policy_changes,

            "current_policy":
                self.selection_history[
                    -1
                ][
                    "selected_policy_name"
                ],

            "history":
                list(
                    self.selection_history
                )
        }


    # ========================================================
    # PRINT DECISION
    # ========================================================

    def print_selection(
        self,
        result
    ):

        print(
            "\n"
            +
            "=" * 80
        )

        print(
            "MARS — DYNAMIC META-POLICY DECISION"
        )

        print(
            "=" * 80
        )

        print(
            "Observed Behavioural Instability:",
            f"{result['raw_estimated_noise']:.6f}"
        )

        print(
            "Nearest Learned Noise Regime:",
            f"{result['nearest_trained_noise_regime']:.2f}"
        )

        print(
            "Environment Classification:",
            result[
                "environment_class"
            ]
        )

        print(
            "Environment Estimation Confidence:",
            f"{result['estimation_confidence']:.4f}"
        )

        print(
            "Selected Evidence Policy:",
            result[
                "selected_policy_name"
            ]
        )

        print(
            "Minimum Observations:",
            result[
                "minimum_observations"
            ]
        )

        print(
            "Maximum Observations:",
            result[
                "maximum_observations"
            ]
        )

        print(
            "Decision Confidence Requirement:",
            result[
                "confidence_level"
            ]
        )

        print(
            "=" * 80
        )
