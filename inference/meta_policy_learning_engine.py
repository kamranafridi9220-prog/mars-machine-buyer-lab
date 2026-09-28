"""
MARS — Machine-Agent Revenue Science

Experiment 021

Autonomous Meta-Policy Learning Engine

Author: Kamran Khan

Purpose:
Learn how aggressively MARS should acquire evidence
when discovering hidden autonomous buyer policies.

Unlike earlier experiments, the evidence-acquisition
configuration is not treated as permanently fixed.

The engine evaluates candidate sampling policies and
learns which configuration provides the strongest
trade-off between:

- policy estimation accuracy
- buyer query consumption
- discovery success
- commercial interaction cost

The learned meta-policy can then be selected for
future buyer environments.
"""

from dataclasses import dataclass
import statistics


# ============================================================
# SAMPLING POLICY
# ============================================================

@dataclass(frozen=True)
class SamplingPolicy:

    name: str

    minimum_observations: int

    maximum_observations: int

    confidence_level: float


# ============================================================
# META-POLICY LEARNING ENGINE
# ============================================================

class MetaPolicyLearningEngine:

    def __init__(
        self,
        accuracy_weight=0.55,
        query_weight=0.30,
        failure_weight=0.15
    ):

        self.accuracy_weight = (
            accuracy_weight
        )

        self.query_weight = (
            query_weight
        )

        self.failure_weight = (
            failure_weight
        )


        total_weight = (

            self.accuracy_weight
            +
            self.query_weight
            +
            self.failure_weight

        )


        if abs(
            total_weight - 1.0
        ) > 0.000001:

            raise ValueError(
                "Meta-policy objective weights "
                "must sum to 1.0."
            )


        self.candidate_policies = (

            self._build_candidate_policies()

        )


        self.training_records = []

        self.policy_statistics = {}

        self.environment_statistics = {}


    # ========================================================
    # CANDIDATE META-POLICIES
    # ========================================================

    @staticmethod
    def _build_candidate_policies():

        return [

            SamplingPolicy(

                name="ECONOMICAL",

                minimum_observations=2,

                maximum_observations=5,

                confidence_level=0.80

            ),

            SamplingPolicy(

                name="BALANCED",

                minimum_observations=3,

                maximum_observations=7,

                confidence_level=0.90

            ),

            SamplingPolicy(

                name="ROBUST",

                minimum_observations=3,

                maximum_observations=9,

                confidence_level=0.95

            ),

            SamplingPolicy(

                name="HIGH_ASSURANCE",

                minimum_observations=5,

                maximum_observations=11,

                confidence_level=0.95

            )

        ]


    # ========================================================
    # GET POLICIES
    # ========================================================

    def get_candidate_policies(
        self
    ):

        return list(
            self.candidate_policies
        )


    # ========================================================
    # NORMALISE
    # ========================================================

    @staticmethod
    def _normalise(
        value,
        minimum,
        maximum
    ):

        if (
            maximum
            <=
            minimum
        ):

            return 0.0


        return (

            value
            -
            minimum

        ) / (

            maximum
            -
            minimum

        )


    # ========================================================
    # RECORD TRAINING RESULT
    # ========================================================

    def record_result(
        self,
        noise_strength,
        seed,
        policy,
        status,
        mean_error,
        queries,
        coverage,
        early_stop_rate=None,
        average_observations=None
    ):

        record = {

            "noise_strength":
                noise_strength,

            "seed":
                seed,

            "policy_name":
                policy.name,

            "minimum_observations":
                policy.minimum_observations,

            "maximum_observations":
                policy.maximum_observations,

            "confidence_level":
                policy.confidence_level,

            "status":
                status,

            "mean_error":
                mean_error,

            "queries":
                queries,

            "coverage":
                coverage,

            "early_stop_rate":
                early_stop_rate,

            "average_observations":
                average_observations

        }


        self.training_records.append(
            record
        )


        return record


    # ========================================================
    # GROUP RECORDS BY POLICY
    # ========================================================

    def _records_for_policy(
        self,
        policy_name,
        noise_strength=None
    ):

        records = [

            record

            for record in self.training_records

            if (
                record[
                    "policy_name"
                ]
                ==
                policy_name
            )

        ]


        if (
            noise_strength
            is not None
        ):

            records = [

                record

                for record in records

                if (
                    abs(
                        record[
                            "noise_strength"
                        ]
                        -
                        noise_strength
                    )
                    <
                    0.000001
                )

            ]


        return records


    # ========================================================
    # SAFE MEAN
    # ========================================================

    @staticmethod
    def _safe_mean(
        values
    ):

        values = [

            value

            for value in values

            if value is not None

        ]


        if not values:

            return None


        return statistics.mean(
            values
        )


    # ========================================================
    # CALCULATE RAW POLICY STATISTICS
    # ========================================================

    def calculate_policy_statistics(
        self,
        noise_strength=None
    ):

        statistics_by_policy = {}


        for policy in (
            self.candidate_policies
        ):

            records = (
                self._records_for_policy(

                    policy.name,

                    noise_strength

                )
            )


            successful = [

                record

                for record in records

                if (
                    record[
                        "status"
                    ]
                    ==
                    "SUCCESS"
                )

            ]


            errors = [

                record[
                    "mean_error"
                ]

                for record in successful

                if (
                    record[
                        "mean_error"
                    ]
                    is not None
                )

            ]


            queries = [

                record[
                    "queries"
                ]

                for record in successful

            ]


            coverages = [

                record[
                    "coverage"
                ]

                for record in successful

            ]


            early_stops = [

                record[
                    "early_stop_rate"
                ]

                for record in successful

                if (
                    record[
                        "early_stop_rate"
                    ]
                    is not None
                )

            ]


            observations = [

                record[
                    "average_observations"
                ]

                for record in successful

                if (
                    record[
                        "average_observations"
                    ]
                    is not None
                )

            ]


            success_rate = (

                len(
                    successful
                )
                /
                len(
                    records
                )

                if records

                else 0.0

            )


            statistics_by_policy[
                policy.name
            ] = {

                "policy":
                    policy,

                "runs":
                    len(
                        records
                    ),

                "successful_runs":
                    len(
                        successful
                    ),

                "failed_runs":
                    (
                        len(
                            records
                        )
                        -
                        len(
                            successful
                        )
                    ),

                "success_rate":
                    success_rate,

                "mean_error":
                    self._safe_mean(
                        errors
                    ),

                "mean_queries":
                    self._safe_mean(
                        queries
                    ),

                "mean_coverage":
                    self._safe_mean(
                        coverages
                    ),

                "mean_early_stop_rate":
                    self._safe_mean(
                        early_stops
                    ),

                "mean_observations":
                    self._safe_mean(
                        observations
                    )

            }


        return statistics_by_policy


    # ========================================================
    # SCORE META-POLICIES
    # ========================================================

    def score_policies(
        self,
        noise_strength=None
    ):

        policy_statistics = (
            self.calculate_policy_statistics(

                noise_strength

            )
        )


        usable = [

            result

            for result in (
                policy_statistics.values()
            )

            if (
                result[
                    "runs"
                ]
                >
                0
            )

        ]


        if not usable:

            return {}


        available_errors = [

            result[
                "mean_error"
            ]

            for result in usable

            if (
                result[
                    "mean_error"
                ]
                is not None
            )

        ]


        available_queries = [

            result[
                "mean_queries"
            ]

            for result in usable

            if (
                result[
                    "mean_queries"
                ]
                is not None
            )

        ]


        if not available_errors:

            return {}


        if not available_queries:

            return {}


        minimum_error = min(
            available_errors
        )


        maximum_error = max(
            available_errors
        )


        minimum_queries = min(
            available_queries
        )


        maximum_queries = max(
            available_queries
        )


        scored = {}


        for policy_name, result in (
            policy_statistics.items()
        ):

            if (
                result[
                    "runs"
                ]
                ==
                0
            ):

                continue


            mean_error = (
                result[
                    "mean_error"
                ]
            )


            mean_queries = (
                result[
                    "mean_queries"
                ]
            )


            if (
                mean_error
                is None
                or
                mean_queries
                is None
            ):

                continue


            normalised_error = (
                self._normalise(

                    mean_error,

                    minimum_error,

                    maximum_error

                )
            )


            normalised_queries = (
                self._normalise(

                    mean_queries,

                    minimum_queries,

                    maximum_queries

                )
            )


            failure_rate = (

                1.0
                -
                result[
                    "success_rate"
                ]

            )


            objective_cost = (

                self.accuracy_weight
                *
                normalised_error

                +

                self.query_weight
                *
                normalised_queries

                +

                self.failure_weight
                *
                failure_rate

            )


            scored[
                policy_name
            ] = {

                **result,

                "normalised_error":
                    normalised_error,

                "normalised_queries":
                    normalised_queries,

                "failure_rate":
                    failure_rate,

                "objective_cost":
                    objective_cost

            }


        return scored


    # ========================================================
    # LEARN POLICY FOR ONE ENVIRONMENT
    # ========================================================

    def learn_policy_for_noise(
        self,
        noise_strength
    ):

        scored = (
            self.score_policies(

                noise_strength

            )
        )


        if not scored:

            return None


        selected_name = min(

            scored,

            key=lambda name:
                scored[
                    name
                ][
                    "objective_cost"
                ]

        )


        selected = (
            scored[
                selected_name
            ]
        )


        result = {

            "noise_strength":
                noise_strength,

            "selected_policy":
                selected[
                    "policy"
                ],

            "objective_cost":
                selected[
                    "objective_cost"
                ],

            "mean_error":
                selected[
                    "mean_error"
                ],

            "mean_queries":
                selected[
                    "mean_queries"
                ],

            "success_rate":
                selected[
                    "success_rate"
                ],

            "mean_coverage":
                selected[
                    "mean_coverage"
                ],

            "all_policy_scores":
                scored

        }


        self.environment_statistics[
            noise_strength
        ] = result


        return result


    # ========================================================
    # LEARN COMPLETE META-POLICY
    # ========================================================

    def learn_meta_policy(
        self,
        noise_levels
    ):

        learned = {}


        for noise_strength in (
            noise_levels
        ):

            result = (
                self.learn_policy_for_noise(

                    noise_strength

                )
            )


            if result is not None:

                learned[
                    noise_strength
                ] = result


        return learned


    # ========================================================
    # SELECT POLICY FOR NEW NOISE LEVEL
    # ========================================================

    def select_policy(
        self,
        estimated_noise
    ):

        if not (
            self.environment_statistics
        ):

            raise ValueError(

                "Meta-policy has not been "
                "learned yet."

            )


        known_noise_levels = list(

            self.environment_statistics.keys()

        )


        nearest_noise = min(

            known_noise_levels,

            key=lambda level:
                abs(
                    level
                    -
                    estimated_noise
                )

        )


        learned_environment = (

            self.environment_statistics[
                nearest_noise
            ]

        )


        return {

            "estimated_noise":
                estimated_noise,

            "matched_training_noise":
                nearest_noise,

            "selected_policy":
                learned_environment[
                    "selected_policy"
                ],

            "training_objective_cost":
                learned_environment[
                    "objective_cost"
                ]

        }


    # ========================================================
    # PRINT LEARNED META-POLICY
    # ========================================================

    def print_meta_policy(
        self
    ):

        print("\n" + "=" * 80)

        print(
            "MARS — LEARNED META-POLICY"
        )

        print("=" * 80)


        if not (
            self.environment_statistics
        ):

            print(
                "No learned policy available."
            )

            return


        for noise_strength in sorted(

            self.environment_statistics.keys()

        ):

            result = (

                self.environment_statistics[
                    noise_strength
                ]

            )


            policy = (
                result[
                    "selected_policy"
                ]
            )


            print(
                f"\nNoise Strength: "
                f"{noise_strength:.2f}"
            )


            print(
                "Selected Policy:",
                policy.name
            )


            print(
                "Minimum Observations:",
                policy.minimum_observations
            )


            print(
                "Maximum Observations:",
                policy.maximum_observations
            )


            print(
                "Confidence Level:",
                policy.confidence_level
            )


            print(
                "Mean Error:",
                result[
                    "mean_error"
                ]
            )


            print(
                "Mean Queries:",
                result[
                    "mean_queries"
                ]
            )


            print(
                "Objective Cost:",
                result[
                    "objective_cost"
                ]
            )


        print("\n" + "=" * 80)
