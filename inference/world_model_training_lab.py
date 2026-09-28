"""
MARS — Machine-Agent Revenue Science

Experiment 024

Buyer World Model Training Laboratory

Author: Kamran Khan

Purpose:
Generate historical black-box buyer interaction episodes
and use them to train the BuyerWorldModel.

The laboratory separates:

TRAINING BUYERS
    Used to construct historical behavioural memory.

VALIDATION BUYERS
    Never added to the world model during initial training.

The world model receives true environment labels only for
historical supervised training.

During validation, environment labels remain hidden from
the model and are used only after prediction to calculate
evaluation metrics.
"""

import statistics

from buyer_lab.probabilistic_buyer_agent import (
    ProbabilisticBuyerFactory
)

from inference.active_diagnostic_intelligence_engine import (
    ActiveDiagnosticIntelligenceEngine
)

from inference.diagnostic_probe_generator import (
    DiagnosticProbeGenerator
)

from inference.buyer_world_model import (
    BuyerWorldModel
)


# ============================================================
# TRAINING LABORATORY
# ============================================================

class WorldModelTrainingLab:

    def __init__(
        self,
        reference_proposal,
        estimated_policy,
        noise_levels=None,
        training_seeds=None,
        validation_seeds=None,
        boundary_width=0.05,
        k_neighbors=7,
        diagnostic_min_observations=3,
        diagnostic_max_observations=15,
        diagnostic_batch_size=2,
        diagnostic_min_total_queries=20,
        diagnostic_max_total_queries=120,
        diagnostic_confidence_threshold=0.80,
        diagnostic_stability_threshold=0.03
    ):

        if noise_levels is None:

            noise_levels = [
                0.05,
                0.10,
                0.15,
                0.20,
                0.25,
                0.30
            ]


        if training_seeds is None:

            training_seeds = list(
                range(
                    1,
                    21
                )
            )


        if validation_seeds is None:

            validation_seeds = list(
                range(
                    101,
                    111
                )
            )


        overlap = set(
            training_seeds
        ).intersection(
            validation_seeds
        )

        if overlap:

            raise ValueError(
                "Training and validation seeds "
                "must not overlap."
            )


        self.reference_proposal = (
            reference_proposal
        )

        self.estimated_policy = (
            estimated_policy
        )

        self.noise_levels = [
            float(level)
            for level in noise_levels
        ]

        self.training_seeds = list(
            training_seeds
        )

        self.validation_seeds = list(
            validation_seeds
        )

        self.boundary_width = (
            boundary_width
        )

        self.diagnostic_min_observations = (
            diagnostic_min_observations
        )

        self.diagnostic_max_observations = (
            diagnostic_max_observations
        )

        self.diagnostic_batch_size = (
            diagnostic_batch_size
        )

        self.diagnostic_min_total_queries = (
            diagnostic_min_total_queries
        )

        self.diagnostic_max_total_queries = (
            diagnostic_max_total_queries
        )

        self.diagnostic_confidence_threshold = (
            diagnostic_confidence_threshold
        )

        self.diagnostic_stability_threshold = (
            diagnostic_stability_threshold
        )


        self.world_model = (
            BuyerWorldModel(
                k_neighbors=k_neighbors
            )
        )


        self.training_episode_count = 0

        self.validation_records = []

        self.training_diagnostic_queries = []

        self.validation_diagnostic_queries = []


    # ========================================================
    # GENERATE DIAGNOSTIC PROBES
    # ========================================================

    def generate_named_probes(
        self
    ):

        generator = (
            DiagnosticProbeGenerator(
                reference_proposal=(
                    self.reference_proposal
                ),
                estimated_policy=(
                    self.estimated_policy
                )
            )
        )

        return (
            generator.generate_named_probes()
        )


    # ========================================================
    # CREATE BUYER
    # ========================================================

    def create_buyer(
        self,
        seed,
        noise_strength
    ):

        return (
            ProbabilisticBuyerFactory.create_buyer(
                random_seed=seed,
                noise_strength=noise_strength,
                boundary_width=(
                    self.boundary_width
                )
            )
        )


    # ========================================================
    # RUN BLACK-BOX DIAGNOSTIC EPISODE
    # ========================================================

    def run_diagnostic_episode(
        self,
        buyer
    ):

        named_probes = (
            self.generate_named_probes()
        )

        diagnostic_engine = (
            ActiveDiagnosticIntelligenceEngine(
                buyer=buyer,
                named_probes=named_probes,
                candidate_noise_levels=(
                    self.noise_levels
                ),
                minimum_observations_per_probe=(
                    self.diagnostic_min_observations
                ),
                maximum_observations_per_probe=(
                    self.diagnostic_max_observations
                ),
                batch_size=(
                    self.diagnostic_batch_size
                ),
                minimum_total_queries=(
                    self.diagnostic_min_total_queries
                ),
                maximum_total_queries=(
                    self.diagnostic_max_total_queries
                ),
                confidence_threshold=(
                    self.diagnostic_confidence_threshold
                ),
                stability_threshold=(
                    self.diagnostic_stability_threshold
                )
            )
        )

        return (
            diagnostic_engine.diagnose()
        )


    # ========================================================
    # BUILD TRAINING MEMORY
    # ========================================================

    def build_training_memory(
        self,
        verbose=True
    ):

        if verbose:

            print(
                "\n"
                +
                "=" * 80
            )

            print(
                "BUILDING BUYER WORLD-MODEL MEMORY"
            )

            print(
                "=" * 80
            )


        for noise_strength in (
            self.noise_levels
        ):

            if verbose:

                print(
                    "\nTraining Environment:",
                    f"{noise_strength:.2f}"
                )


            environment_episode_count = 0


            for seed in (
                self.training_seeds
            ):

                buyer = (
                    self.create_buyer(
                        seed=seed,
                        noise_strength=(
                            noise_strength
                        )
                    )
                )

                diagnostic_result = (
                    self.run_diagnostic_episode(
                        buyer
                    )
                )


                self.world_model.add_training_episode(
                    diagnostic_result=(
                        diagnostic_result
                    ),
                    environment_label=(
                        noise_strength
                    ),
                    metadata={
                        "seed":
                            seed,

                        "source":
                            "TRAINING",

                        "diagnostic_queries":
                            diagnostic_result[
                                "total_diagnostic_queries"
                            ]
                    }
                )


                self.training_diagnostic_queries.append(
                    diagnostic_result[
                        "total_diagnostic_queries"
                    ]
                )


                self.training_episode_count += 1

                environment_episode_count += 1


            if verbose:

                print(
                    "Historical Episodes Added:",
                    environment_episode_count
                )


        training_summary = (
            self.world_model.fit()
        )


        if verbose:

            print(
                "\nWorld model fitted."
            )

            print(
                "Total Historical Episodes:",
                self.training_episode_count
            )


        return training_summary


    # ========================================================
    # VALIDATE WORLD MODEL
    # ========================================================

    def validate(
        self,
        verbose=True
    ):

        if not self.world_model.is_fitted:

            raise ValueError(
                "World model must be trained "
                "before validation."
            )


        self.validation_records = []

        self.validation_diagnostic_queries = []


        if verbose:

            print(
                "\n"
                +
                "=" * 80
            )

            print(
                "HELD-OUT BUYER WORLD-MODEL VALIDATION"
            )

            print(
                "=" * 80
            )


        for true_environment in (
            self.noise_levels
        ):

            if verbose:

                print(
                    "\nHidden Validation Environment:",
                    f"{true_environment:.2f}"
                )


            for seed in (
                self.validation_seeds
            ):

                buyer = (
                    self.create_buyer(
                        seed=seed,
                        noise_strength=(
                            true_environment
                        )
                    )
                )


                diagnostic_result = (
                    self.run_diagnostic_episode(
                        buyer
                    )
                )


                prediction = (
                    self.world_model.predict_environment(
                        diagnostic_result
                    )
                )


                predicted_environment = (
                    prediction[
                        "predicted_environment"
                    ]
                )

                expected_environment = (
                    prediction[
                        "expected_environment"
                    ]
                )


                classification_correct = (
                    abs(
                        predicted_environment
                        -
                        true_environment
                    )
                    <
                    0.000001
                )


                absolute_environment_error = abs(
                    expected_environment
                    -
                    true_environment
                )


                record = {

                    "true_environment":
                        true_environment,

                    "seed":
                        seed,

                    "predicted_environment":
                        predicted_environment,

                    "expected_environment":
                        expected_environment,

                    "classification_correct":
                        classification_correct,

                    "absolute_environment_error":
                        absolute_environment_error,

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

                    "diagnostic_queries":
                        diagnostic_result[
                            "total_diagnostic_queries"
                        ]
                }


                self.validation_records.append(
                    record
                )


                self.validation_diagnostic_queries.append(
                    diagnostic_result[
                        "total_diagnostic_queries"
                    ]
                )


                if verbose:

                    print(
                        "Seed:",
                        seed,
                        "| Predicted:",
                        f"{predicted_environment:.2f}",
                        "| Expected:",
                        f"{expected_environment:.4f}",
                        "| Confidence:",
                        f"{prediction['confidence']:.4f}",
                        "| Error:",
                        f"{absolute_environment_error:.4f}"
                    )


        return (
            self.generate_validation_summary()
        )


    # ========================================================
    # VALIDATION SUMMARY
    # ========================================================

    def generate_validation_summary(
        self
    ):

        if not self.validation_records:

            return {

                "validation_runs":
                    0,

                "classification_accuracy":
                    None,

                "mean_absolute_environment_error":
                    None,

                "mean_confidence":
                    None,

                "mean_prediction_entropy":
                    None,

                "mean_diagnostic_queries":
                    None
            }


        validation_runs = len(
            self.validation_records
        )


        correct_predictions = sum(

            1

            for record in (
                self.validation_records
            )

            if record[
                "classification_correct"
            ]
        )


        classification_accuracy = (
            correct_predictions
            /
            validation_runs
        )


        mean_absolute_environment_error = (
            statistics.mean(

                record[
                    "absolute_environment_error"
                ]

                for record in (
                    self.validation_records
                )
            )
        )


        mean_confidence = (
            statistics.mean(

                record[
                    "confidence"
                ]

                for record in (
                    self.validation_records
                )
            )
        )


        mean_prediction_entropy = (
            statistics.mean(

                record[
                    "prediction_entropy"
                ]

                for record in (
                    self.validation_records
                )
            )
        )


        mean_diagnostic_queries = (
            statistics.mean(
                self.validation_diagnostic_queries
            )
        )


        per_environment = {}


        for environment in (
            self.noise_levels
        ):

            environment_records = [

                record

                for record in (
                    self.validation_records
                )

                if abs(
                    record[
                        "true_environment"
                    ]
                    -
                    environment
                )
                <
                0.000001
            ]


            if not environment_records:

                continue


            environment_accuracy = (

                sum(

                    1

                    for record in (
                        environment_records
                    )

                    if record[
                        "classification_correct"
                    ]

                )
                /
                len(
                    environment_records
                )
            )


            environment_error = (
                statistics.mean(

                    record[
                        "absolute_environment_error"
                    ]

                    for record in (
                        environment_records
                    )
                )
            )


            environment_confidence = (
                statistics.mean(

                    record[
                        "confidence"
                    ]

                    for record in (
                        environment_records
                    )
                )
            )


            per_environment[
                environment
            ] = {

                "runs":
                    len(
                        environment_records
                    ),

                "classification_accuracy":
                    environment_accuracy,

                "mean_absolute_error":
                    environment_error,

                "mean_confidence":
                    environment_confidence
            }


        return {

            "validation_runs":
                validation_runs,

            "correct_classifications":
                correct_predictions,

            "classification_accuracy":
                classification_accuracy,

            "mean_absolute_environment_error":
                mean_absolute_environment_error,

            "mean_confidence":
                mean_confidence,

            "mean_prediction_entropy":
                mean_prediction_entropy,

            "mean_diagnostic_queries":
                mean_diagnostic_queries,

            "per_environment":
                per_environment
        }


    # ========================================================
    # PRINT VALIDATION SUMMARY
    # ========================================================

    def print_validation_summary(
        self
    ):

        summary = (
            self.generate_validation_summary()
        )


        print(
            "\n"
            +
            "=" * 80
        )

        print(
            "BUYER WORLD MODEL — VALIDATION SUMMARY"
        )

        print(
            "=" * 80
        )


        print(
            "Validation Runs:",
            summary[
                "validation_runs"
            ]
        )


        if (
            summary[
                "classification_accuracy"
            ]
            is None
        ):

            print(
                "No validation results available."
            )

            return


        print(
            "Correct Environment Classifications:",
            summary[
                "correct_classifications"
            ]
        )

        print(
            "Environment Classification Accuracy:",
            f"{summary['classification_accuracy'] * 100:.2f}%"
        )

        print(
            "Mean Absolute Environment Error:",
            summary[
                "mean_absolute_environment_error"
            ]
        )

        print(
            "Mean Prediction Confidence:",
            summary[
                "mean_confidence"
            ]
        )

        print(
            "Mean Prediction Entropy:",
            summary[
                "mean_prediction_entropy"
            ]
        )

        print(
            "Mean Diagnostic Queries:",
            summary[
                "mean_diagnostic_queries"
            ]
        )


        print(
            "\nPER-ENVIRONMENT PERFORMANCE"
        )


        for environment, result in (
            summary[
                "per_environment"
            ].items()
        ):

            print(
                "\nEnvironment:",
                f"{environment:.2f}"
            )

            print(
                "Runs:",
                result[
                    "runs"
                ]
            )

            print(
                "Classification Accuracy:",
                f"{result['classification_accuracy'] * 100:.2f}%"
            )

            print(
                "Mean Absolute Error:",
                result[
                    "mean_absolute_error"
                ]
            )

            print(
                "Mean Confidence:",
                result[
                    "mean_confidence"
                ]
            )


        print(
            "=" * 80
        )


    # ========================================================
    # AUTONOMY REPORT
    # ========================================================

    @staticmethod
    def print_autonomy_report():

        print(
            "\n"
            +
            "=" * 80
        )

        print(
            "WORLD MODEL AUTONOMY CHECK"
        )

        print(
            "=" * 80
        )

        print(
            "True environment used for historical "
            "supervised training: YES"
        )

        print(
            "True environment supplied during "
            "world-model prediction: NO"
        )

        print(
            "Hidden buyer thresholds supplied "
            "to world model: NO"
        )

        print(
            "Private buyer decision rules supplied "
            "to world model: NO"
        )

        print(
            "Predictions generated from observable "
            "behavioural features: YES"
        )

        print(
            "Training and validation seeds separated: YES"
        )

        print(
            "True validation environment used "
            "for evaluation only: YES"
        )

        print(
            "=" * 80
        )
