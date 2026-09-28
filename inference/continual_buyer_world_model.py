"""
MARS — Machine-Agent Revenue Science

Experiment 025

Continual Buyer World Model

Author: Kamran Khan

Purpose:
Extend the Experiment 024 BuyerWorldModel with controlled
online adaptation.

The model begins with historical buyer experience learned
offline. When new buyers are encountered sequentially, it
can:

1. Predict the buyer environment.
2. Measure whether the behaviour is familiar.
3. Detect an experience gap.
4. Decide whether the episode should enter memory.
5. Update the world model after feedback becomes available.
6. Track whether accumulated experience improves later
   predictions.
7. Monitor possible catastrophic degradation.

Important experimental rule:

The true environment label is NEVER used to decide the
prediction for the current buyer.

It may only be supplied after the current prediction has
been recorded, representing delayed supervisory feedback
used for continual learning.
"""

import math
import statistics
from collections import Counter

from inference.buyer_world_model import (
    BuyerWorldModel
)


# ============================================================
# CONTINUAL BUYER WORLD MODEL
# ============================================================

class ContinualBuyerWorldModel:

    def __init__(
        self,
        base_world_model=None,
        k_neighbors=7,
        confidence_threshold=0.60,
        distance_threshold=2.50,
        entropy_threshold=1.25,
        minimum_novelty_score=0.35,
        memory_limit=None
    ):

        if base_world_model is None:

            base_world_model = (
                BuyerWorldModel(
                    k_neighbors=k_neighbors
                )
            )

        self.world_model = (
            base_world_model
        )

        self.confidence_threshold = float(
            confidence_threshold
        )

        self.distance_threshold = float(
            distance_threshold
        )

        self.entropy_threshold = float(
            entropy_threshold
        )

        self.minimum_novelty_score = float(
            minimum_novelty_score
        )

        self.memory_limit = (
            memory_limit
        )

        self.interaction_history = []

        self.learning_history = []

        self.performance_history = []

        self.environment_learning_counts = Counter()

        self.initial_memory_size = len(
            self.world_model.training_examples
        )

        self.total_predictions = 0

        self.total_updates = 0

        self.total_experience_gaps = 0

        self.total_high_confidence_predictions = 0


    # ========================================================
    # SAFE CLAMP
    # ========================================================

    @staticmethod
    def _clamp(
        value,
        minimum=0.0,
        maximum=1.0
    ):

        return max(
            minimum,
            min(
                maximum,
                float(value)
            )
        )


    # ========================================================
    # CHECK MODEL READY
    # ========================================================

    def _check_ready(
        self
    ):

        if not self.world_model.is_fitted:

            raise ValueError(
                "Underlying BuyerWorldModel must be fitted "
                "before continual prediction."
            )


    # ========================================================
    # DISTANCE NOVELTY
    # ========================================================

    def _distance_novelty(
        self,
        nearest_distance
    ):

        nearest_distance = float(
            nearest_distance
        )

        if self.distance_threshold <= 0.0:

            return 0.0

        return self._clamp(
            nearest_distance
            /
            self.distance_threshold
        )


    # ========================================================
    # CONFIDENCE NOVELTY
    # ========================================================

    def _confidence_novelty(
        self,
        confidence
    ):

        confidence = float(
            confidence
        )

        if self.confidence_threshold <= 0.0:

            return 0.0

        if confidence >= self.confidence_threshold:

            return 0.0

        return self._clamp(
            (
                self.confidence_threshold
                -
                confidence
            )
            /
            self.confidence_threshold
        )


    # ========================================================
    # ENTROPY NOVELTY
    # ========================================================

    def _entropy_novelty(
        self,
        entropy
    ):

        entropy = float(
            entropy
        )

        if self.entropy_threshold <= 0.0:

            return 0.0

        return self._clamp(
            entropy
            /
            self.entropy_threshold
        )


    # ========================================================
    # CALCULATE NOVELTY
    # ========================================================

    def calculate_novelty(
        self,
        prediction
    ):

        """
        Estimate how unfamiliar the current buyer episode
        appears relative to historical experience.

        The score uses only prediction-time quantities:

        - nearest historical distance
        - prediction confidence
        - predictive entropy

        No true environment label is used.
        """

        distance_component = (
            self._distance_novelty(
                prediction[
                    "nearest_distance"
                ]
            )
        )

        confidence_component = (
            self._confidence_novelty(
                prediction[
                    "confidence"
                ]
            )
        )

        entropy_component = (
            self._entropy_novelty(
                prediction[
                    "prediction_entropy"
                ]
            )
        )

        novelty_score = (
            0.40
            *
            distance_component
            +
            0.30
            *
            confidence_component
            +
            0.30
            *
            entropy_component
        )

        novelty_score = (
            self._clamp(
                novelty_score
            )
        )

        return {

            "novelty_score":
                novelty_score,

            "distance_component":
                distance_component,

            "confidence_component":
                confidence_component,

            "entropy_component":
                entropy_component
        }


    # ========================================================
    # DETECT EXPERIENCE GAP
    # ========================================================

    def detect_experience_gap(
        self,
        prediction
    ):

        novelty = (
            self.calculate_novelty(
                prediction
            )
        )

        low_confidence = (
            prediction[
                "confidence"
            ]
            <
            self.confidence_threshold
        )

        high_distance = (
            prediction[
                "nearest_distance"
            ]
            >
            self.distance_threshold
        )

        high_entropy = (
            prediction[
                "prediction_entropy"
            ]
            >
            self.entropy_threshold
        )

        novelty_trigger = (
            novelty[
                "novelty_score"
            ]
            >=
            self.minimum_novelty_score
        )

        experience_gap = (
            novelty_trigger
            or
            high_distance
            or
            (
                low_confidence
                and
                high_entropy
            )
        )

        reasons = []

        if novelty_trigger:

            reasons.append(
                "NOVELTY_SCORE"
            )

        if high_distance:

            reasons.append(
                "DISTANCE"
            )

        if low_confidence:

            reasons.append(
                "LOW_CONFIDENCE"
            )

        if high_entropy:

            reasons.append(
                "HIGH_ENTROPY"
            )

        if not reasons:

            reasons.append(
                "FAMILIAR_ENVIRONMENT"
            )

        return {

            "experience_gap":
                experience_gap,

            "reasons":
                reasons,

            **novelty
        }


    # ========================================================
    # PREDICT NEW BUYER
    # ========================================================

    def predict(
        self,
        diagnostic_result
    ):

        """
        Predict BEFORE any feedback label is supplied.

        This ordering is critical for Experiment 025.
        """

        self._check_ready()

        prediction = (
            self.world_model.predict_environment(
                diagnostic_result
            )
        )

        gap_analysis = (
            self.detect_experience_gap(
                prediction
            )
        )

        self.total_predictions += 1

        if (
            gap_analysis[
                "experience_gap"
            ]
        ):

            self.total_experience_gaps += 1


        if (
            prediction[
                "confidence"
            ]
            >=
            self.confidence_threshold
        ):

            self.total_high_confidence_predictions += 1


        interaction_record = {

            "interaction_number":
                self.total_predictions,

            "predicted_environment":
                prediction[
                    "predicted_environment"
                ],

            "expected_environment":
                prediction[
                    "expected_environment"
                ],

            "confidence":
                prediction[
                    "confidence"
                ],

            "prediction_entropy":
                prediction[
                    "prediction_entropy"
                ],

            "nearest_distance":
                prediction[
                    "nearest_distance"
                ],

            "mean_neighbor_distance":
                prediction[
                    "mean_neighbor_distance"
                ],

            "environment_probabilities":
                prediction[
                    "environment_probabilities"
                ],

            "experience_gap":
                gap_analysis[
                    "experience_gap"
                ],

            "experience_gap_reasons":
                gap_analysis[
                    "reasons"
                ],

            "novelty_score":
                gap_analysis[
                    "novelty_score"
                ],

            "distance_novelty":
                gap_analysis[
                    "distance_component"
                ],

            "confidence_novelty":
                gap_analysis[
                    "confidence_component"
                ],

            "entropy_novelty":
                gap_analysis[
                    "entropy_component"
                ],

            "memory_size_before_feedback":
                len(
                    self.world_model.training_examples
                )
        }

        self.interaction_history.append(
            interaction_record
        )

        return interaction_record


    # ========================================================
    # SHOULD LEARN
    # ========================================================

    def should_learn(
        self,
        interaction_record
    ):

        """
        Current Experiment 025 learning policy:

        Learn episodes identified as experience gaps.

        This prevents indiscriminately memorising every
        buyer interaction.
        """

        return bool(
            interaction_record[
                "experience_gap"
            ]
        )


    # ========================================================
    # MEMORY LIMIT
    # ========================================================

    def _enforce_memory_limit(
        self
    ):

        if self.memory_limit is None:

            return 0

        removed = 0

        while (
            len(
                self.world_model.training_examples
            )
            >
            self.memory_limit
        ):

            oldest = (
                self.world_model.training_examples.pop(
                    0
                )
            )

            environment = (
                oldest[
                    "environment_label"
                ]
            )

            if (
                self.world_model.environment_counts[
                    environment
                ]
                >
                0
            ):

                self.world_model.environment_counts[
                    environment
                ] -= 1

            removed += 1

        return removed


    # ========================================================
    # LEARN FROM DELAYED FEEDBACK
    # ========================================================

    def learn_from_feedback(
        self,
        diagnostic_result,
        true_environment,
        interaction_record,
        metadata=None
    ):

        """
        Delayed supervision stage.

        The current buyer has already been predicted before
        this method is called.

        Therefore the true environment cannot influence the
        prediction that is being evaluated.
        """

        learn = (
            self.should_learn(
                interaction_record
            )
        )

        memory_before = len(
            self.world_model.training_examples
        )


        if not learn:

            learning_record = {

                "interaction_number":
                    interaction_record[
                        "interaction_number"
                    ],

                "learned":
                    False,

                "true_environment":
                    float(
                        true_environment
                    ),

                "memory_before":
                    memory_before,

                "memory_after":
                    memory_before,

                "removed_for_memory_limit":
                    0
            }

            self.learning_history.append(
                learning_record
            )

            return learning_record


        learning_metadata = {

            "source":
                "CONTINUAL_FEEDBACK",

            "interaction_number":
                interaction_record[
                    "interaction_number"
                ],

            "novelty_score":
                interaction_record[
                    "novelty_score"
                ]
        }


        if metadata:

            learning_metadata.update(
                metadata
            )


        self.world_model.add_training_episode(
            diagnostic_result=(
                diagnostic_result
            ),
            environment_label=(
                true_environment
            ),
            metadata=(
                learning_metadata
            )
        )


        removed = (
            self._enforce_memory_limit()
        )


        self.world_model.fit()


        self.total_updates += 1

        self.environment_learning_counts[
            float(
                true_environment
            )
        ] += 1


        memory_after = len(
            self.world_model.training_examples
        )


        learning_record = {

            "interaction_number":
                interaction_record[
                    "interaction_number"
                ],

            "learned":
                True,

            "true_environment":
                float(
                    true_environment
                ),

            "memory_before":
                memory_before,

            "memory_after":
                memory_after,

            "removed_for_memory_limit":
                removed
        }


        self.learning_history.append(
            learning_record
        )

        return learning_record


    # ========================================================
    # RECORD PERFORMANCE
    # ========================================================

    def record_performance(
        self,
        interaction_record,
        true_environment
    ):

        true_environment = float(
            true_environment
        )

        predicted_environment = float(
            interaction_record[
                "predicted_environment"
            ]
        )

        expected_environment = float(
            interaction_record[
                "expected_environment"
            ]
        )


        exact_correct = (
            abs(
                predicted_environment
                -
                true_environment
            )
            <
            0.000001
        )


        absolute_error = abs(
            expected_environment
            -
            true_environment
        )


        record = {

            "interaction_number":
                interaction_record[
                    "interaction_number"
                ],

            "true_environment":
                true_environment,

            "predicted_environment":
                predicted_environment,

            "expected_environment":
                expected_environment,

            "exact_correct":
                exact_correct,

            "absolute_error":
                absolute_error,

            "confidence":
                interaction_record[
                    "confidence"
                ],

            "prediction_entropy":
                interaction_record[
                    "prediction_entropy"
                ],

            "novelty_score":
                interaction_record[
                    "novelty_score"
                ],

            "experience_gap":
                interaction_record[
                    "experience_gap"
                ]
        }


        self.performance_history.append(
            record
        )

        return record


    # ========================================================
    # PROCESS COMPLETE ONLINE EPISODE
    # ========================================================

    def process_episode(
        self,
        diagnostic_result,
        true_environment,
        metadata=None
    ):

        """
        Convenience method enforcing the correct causal order:

        1. Predict unknown buyer.
        2. Record prediction performance.
        3. Reveal delayed feedback.
        4. Optionally learn for future buyers.

        The label is never supplied before prediction.
        """

        interaction_record = (
            self.predict(
                diagnostic_result
            )
        )


        performance_record = (
            self.record_performance(
                interaction_record=(
                    interaction_record
                ),
                true_environment=(
                    true_environment
                )
            )
        )


        learning_record = (
            self.learn_from_feedback(
                diagnostic_result=(
                    diagnostic_result
                ),
                true_environment=(
                    true_environment
                ),
                interaction_record=(
                    interaction_record
                ),
                metadata=metadata
            )
        )


        return {

            "prediction":
                interaction_record,

            "performance":
                performance_record,

            "learning":
                learning_record
        }


    # ========================================================
    # PERFORMANCE WINDOW
    # ========================================================

    def calculate_window_performance(
        self,
        records
    ):

        if not records:

            return {

                "runs":
                    0,

                "accuracy":
                    None,

                "mean_absolute_error":
                    None,

                "mean_confidence":
                    None,

                "mean_novelty":
                    None
            }


        accuracy = (

            sum(
                1
                for record in records
                if record[
                    "exact_correct"
                ]
            )
            /
            len(
                records
            )
        )


        mean_absolute_error = (
            statistics.mean(
                record[
                    "absolute_error"
                ]
                for record in records
            )
        )


        mean_confidence = (
            statistics.mean(
                record[
                    "confidence"
                ]
                for record in records
            )
        )


        mean_novelty = (
            statistics.mean(
                record[
                    "novelty_score"
                ]
                for record in records
            )
        )


        return {

            "runs":
                len(
                    records
                ),

            "accuracy":
                accuracy,

            "mean_absolute_error":
                mean_absolute_error,

            "mean_confidence":
                mean_confidence,

            "mean_novelty":
                mean_novelty
        }


    # ========================================================
    # EARLY VS LATE PERFORMANCE
    # ========================================================

    def compare_early_late_performance(
        self
    ):

        records = (
            self.performance_history
        )

        if len(
            records
        ) < 2:

            return {

                "early":
                    self.calculate_window_performance(
                        records
                    ),

                "late":
                    self.calculate_window_performance(
                        []
                    )
            }


        midpoint = (
            len(
                records
            )
            //
            2
        )


        early = (
            records[
                :midpoint
            ]
        )

        late = (
            records[
                midpoint:
            ]
        )


        return {

            "early":
                self.calculate_window_performance(
                    early
                ),

            "late":
                self.calculate_window_performance(
                    late
                )
        }


    # ========================================================
    # SUMMARY
    # ========================================================

    def generate_summary(
        self
    ):

        all_performance = (
            self.calculate_window_performance(
                self.performance_history
            )
        )

        early_late = (
            self.compare_early_late_performance()
        )


        learned_count = sum(
            1
            for record in self.learning_history
            if record[
                "learned"
            ]
        )


        skipped_count = (
            len(
                self.learning_history
            )
            -
            learned_count
        )


        return {

            "initial_memory_size":
                self.initial_memory_size,

            "current_memory_size":
                len(
                    self.world_model.training_examples
                ),

            "total_predictions":
                self.total_predictions,

            "total_updates":
                self.total_updates,

            "experience_gaps":
                self.total_experience_gaps,

            "high_confidence_predictions":
                self.total_high_confidence_predictions,

            "learned_episodes":
                learned_count,

            "skipped_learning_episodes":
                skipped_count,

            "environment_learning_counts":
                dict(
                    sorted(
                        self.environment_learning_counts.items()
                    )
                ),

            "overall_performance":
                all_performance,

            "early_performance":
                early_late[
                    "early"
                ],

            "late_performance":
                early_late[
                    "late"
                ]
        }


    # ========================================================
    # PRINT SUMMARY
    # ========================================================

    def print_summary(
        self
    ):

        summary = (
            self.generate_summary()
        )


        print(
            "\n"
            +
            "=" * 80
        )

        print(
            "MARS — CONTINUAL BUYER WORLD MODEL"
        )

        print(
            "=" * 80
        )


        print(
            "Initial Memory Size:",
            summary[
                "initial_memory_size"
            ]
        )

        print(
            "Current Memory Size:",
            summary[
                "current_memory_size"
            ]
        )

        print(
            "Total Predictions:",
            summary[
                "total_predictions"
            ]
        )

        print(
            "Experience Gaps Detected:",
            summary[
                "experience_gaps"
            ]
        )

        print(
            "Continual Updates:",
            summary[
                "total_updates"
            ]
        )

        print(
            "Learned Episodes:",
            summary[
                "learned_episodes"
            ]
        )

        print(
            "Skipped Learning Episodes:",
            summary[
                "skipped_learning_episodes"
            ]
        )


        overall = (
            summary[
                "overall_performance"
            ]
        )


        if (
            overall[
                "accuracy"
            ]
            is not None
        ):

            print(
                "\nOverall Exact Accuracy:",
                f"{overall['accuracy'] * 100:.2f}%"
            )

            print(
                "Overall Mean Absolute Error:",
                overall[
                    "mean_absolute_error"
                ]
            )

            print(
                "Overall Mean Confidence:",
                overall[
                    "mean_confidence"
                ]
            )

            print(
                "Overall Mean Novelty:",
                overall[
                    "mean_novelty"
                ]
            )


        early = (
            summary[
                "early_performance"
            ]
        )

        late = (
            summary[
                "late_performance"
            ]
        )


        if (
            early[
                "accuracy"
            ]
            is not None
            and
            late[
                "accuracy"
            ]
            is not None
        ):

            print(
                "\nEARLY VS LATE PERFORMANCE"
            )

            print(
                "Early Accuracy:",
                f"{early['accuracy'] * 100:.2f}%"
            )

            print(
                "Late Accuracy:",
                f"{late['accuracy'] * 100:.2f}%"
            )

            print(
                "Early Mean Error:",
                early[
                    "mean_absolute_error"
                ]
            )

            print(
                "Late Mean Error:",
                late[
                    "mean_absolute_error"
                ]
            )


        print(
            "\nLearning Counts by Environment:"
        )


        for environment, count in (
            summary[
                "environment_learning_counts"
            ].items()
        ):

            print(
                f"{environment:.2f}: "
                f"{count}"
            )


        print(
            "=" * 80
        )
