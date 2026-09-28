"""
MARS — Machine-Agent Revenue Science

Experiment 022 / 023

Dynamic Meta-Policy Controller

Author: Kamran Khan

Purpose:
Select an evidence-acquisition strategy for an unknown
autonomous buyer using an inferred behavioural environment
rather than direct access to the simulator's hidden
noise-strength parameter.

Compatible with:

Experiment 022
    Fixed diagnostic sampling.

Experiment 023
    Active adaptive diagnostic sampling with unequal
    observations across probes.

The controller never requires the true simulator noise.
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

        regimes = [

            float(
                noise_level
            )

            for noise_level in (
                environment_statistics.keys()
            )
        ]

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
    # SAFE NUMERIC CONVERSION
    # ========================================================

    @staticmethod
    def _safe_float(
        value,
        default=0.0
    ):

        if value is None:

            return float(
                default
            )

        try:

            return float(
                value
            )

        except (
            TypeError,
            ValueError
        ):

            return float(
                default
            )


    # ========================================================
    # CALCULATE ESTIMATION CONFIDENCE
    # ========================================================

    @classmethod
    def calculate_estimation_confidence(
        cls,
        environment_result
    ):

        """
        Supports both diagnostic architectures.

        Experiment 022:
            Uses fixed observations per probe and
            confidence-interval width.

        Experiment 023:
            Uses adaptive total diagnostic queries and
            the environment posterior confidence produced
            by ActiveDiagnosticIntelligenceEngine.

        This avoids assuming that every active probe
        receives the same number of observations.
        """

        # ----------------------------------------------------
        # ACTIVE DIAGNOSTIC CONFIDENCE
        # ----------------------------------------------------

        active_confidence = (
            environment_result.get(
                "environment_confidence"
            )
        )

        if active_confidence is not None:

            active_confidence = (
                cls._safe_float(
                    active_confidence,
                    default=0.0
                )
            )

            total_queries = (
                cls._safe_float(
                    environment_result.get(
                        "total_diagnostic_queries"
                    ),
                    default=0.0
                )
            )

            query_component = min(
                1.0,
                total_queries
                /
                120.0
            )

            confidence = (
                0.80
                *
                active_confidence
                +
                0.20
                *
                query_component
            )

            return max(
                0.0,
                min(
                    1.0,
                    confidence
                )
            )


        # ----------------------------------------------------
        # FIXED DIAGNOSTIC CONFIDENCE
        # ----------------------------------------------------

        ci_width = (
            cls._safe_float(
                environment_result.get(
                    "mean_acceptance_ci_width"
                ),
                default=1.0
            )
        )

        probe_count = (
            cls._safe_float(
                environment_result.get(
                    "diagnostic_probes"
                ),
                default=0.0
            )
        )

        observations_per_probe = (
            environment_result.get(
                "observations_per_probe"
            )
        )

        total_queries = (
            environment_result.get(
                "total_diagnostic_queries"
            )
        )

        # Prefer the directly observed query count.
        if total_queries is not None:

            total_observations = (
                cls._safe_float(
                    total_queries,
                    default=0.0
                )
            )

        else:

            observations_per_probe = (
                cls._safe_float(
                    observations_per_probe,
                    default=0.0
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
                1.0
                -
                ci_width
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

        if (
            "estimated_noise"
            not in environment_result
        ):

            raise ValueError(
                "Environment result does not contain "
                "estimated_noise."
            )

        estimated_noise = (
            self._safe_float(
                environment_result[
                    "estimated_noise"
                ]
            )
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
        # META-POLICY SELECTION
        #
        # Only the inferred environment is used here.
        # The true simulator noise is not supplied.
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
    # GENERATE SUMMARY
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
