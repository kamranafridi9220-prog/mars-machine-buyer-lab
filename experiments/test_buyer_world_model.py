"""
MARS — Machine-Agent Revenue Science

Experiment 024

Autonomous Buyer World Model Learning

Author: Kamran Khan

Purpose:
Train and evaluate a learned buyer world model using
historical black-box interaction episodes.

Research question:
Can MARS learn the relationship between observable buyer
behaviour and latent buyer environments from historical
experience, rather than relying on a manually specified
likelihood function?

Training:
    20 seeds × 6 environments = 120 historical episodes

Held-out validation:
    10 seeds × 6 environments = 60 unseen episodes

True environment labels are used for supervised training
and post-prediction evaluation only. They are not supplied
to the world model during validation prediction.
"""

from buyer_lab.buyer_agent import (
    CommercialProposal
)

from inference.world_model_training_lab import (
    WorldModelTrainingLab
)


# ============================================================
# EXPERIMENT CONFIGURATION
# ============================================================

NOISE_LEVELS = [
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
    0.30
]

TRAINING_SEEDS = list(
    range(
        1,
        21
    )
)

VALIDATION_SEEDS = list(
    range(
        101,
        111
    )
)

BOUNDARY_WIDTH = 0.05

K_NEIGHBORS = 7


# ============================================================
# REFERENCE PROPOSAL
# ============================================================

REFERENCE_PROPOSAL = CommercialProposal(
    annual_price=80000,
    contract_months=12,
    service_availability=100.0,
    payment_days=60,
    supplier_reliability=100.0
)


# ============================================================
# POLICY ESTIMATE
# ============================================================
#
# This is the previously established buyer-policy estimate
# used to construct diagnostic probes.
#
# The world model itself does not receive hidden buyer
# thresholds during prediction.
# ============================================================

ESTIMATED_POLICY = {

    "annual_price":
        105000.0,

    "contract_months":
        36,

    "service_availability":
        98.0,

    "payment_days":
        30,

    "supplier_reliability":
        85.0
}


# ============================================================
# EXPERIMENT HEADER
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "MARS — EXPERIMENT 024"
)

print(
    "AUTONOMOUS BUYER WORLD MODEL LEARNING"
)

print(
    "=" * 80
)

print(
    "\nNoise Regimes:",
    len(
        NOISE_LEVELS
    )
)

print(
    "Training Seeds:",
    len(
        TRAINING_SEEDS
    )
)

print(
    "Validation Seeds:",
    len(
        VALIDATION_SEEDS
    )
)

print(
    "Expected Historical Training Episodes:",
    len(
        NOISE_LEVELS
    )
    *
    len(
        TRAINING_SEEDS
    )
)

print(
    "Expected Held-Out Validation Episodes:",
    len(
        NOISE_LEVELS
    )
    *
    len(
        VALIDATION_SEEDS
    )
)

print(
    "K Neighbors:",
    K_NEIGHBORS
)


# ============================================================
# CREATE TRAINING LAB
# ============================================================

lab = (
    WorldModelTrainingLab(
        reference_proposal=REFERENCE_PROPOSAL,
        estimated_policy=ESTIMATED_POLICY,
        noise_levels=NOISE_LEVELS,
        training_seeds=TRAINING_SEEDS,
        validation_seeds=VALIDATION_SEEDS,
        boundary_width=BOUNDARY_WIDTH,
        k_neighbors=K_NEIGHBORS,
        diagnostic_min_observations=3,
        diagnostic_max_observations=15,
        diagnostic_batch_size=2,
        diagnostic_min_total_queries=20,
        diagnostic_max_total_queries=120,
        diagnostic_confidence_threshold=0.80,
        diagnostic_stability_threshold=0.03
    )
)


# ============================================================
# PHASE 1 — BUILD HISTORICAL MEMORY
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "PHASE 1 — HISTORICAL BUYER EXPERIENCE GENERATION"
)

print(
    "=" * 80
)

training_summary = (
    lab.build_training_memory(
        verbose=True
    )
)


# ============================================================
# WORLD MODEL SUMMARY
# ============================================================

lab.world_model.print_training_summary()


# ============================================================
# TRAINING INTEGRITY CHECK
# ============================================================

expected_training_examples = (
    len(
        NOISE_LEVELS
    )
    *
    len(
        TRAINING_SEEDS
    )
)

actual_training_examples = (
    training_summary[
        "training_examples"
    ]
)

if (
    actual_training_examples
    !=
    expected_training_examples
):

    raise RuntimeError(
        "World model training memory is incomplete. "
        f"Expected {expected_training_examples} examples "
        f"but found {actual_training_examples}."
    )


if (
    training_summary[
        "environment_classes"
    ]
    !=
    len(
        NOISE_LEVELS
    )
):

    raise RuntimeError(
        "World model did not learn all configured "
        "environment classes."
    )


if not (
    training_summary[
        "fitted"
    ]
):

    raise RuntimeError(
        "World model was not fitted successfully."
    )


print(
    "\nTraining integrity check: PASSED"
)


# ============================================================
# PHASE 2 — HELD-OUT VALIDATION
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "PHASE 2 — HELD-OUT WORLD MODEL VALIDATION"
)

print(
    "=" * 80
)

validation_summary = (
    lab.validate(
        verbose=True
    )
)

lab.print_validation_summary()


# ============================================================
# VALIDATION INTEGRITY CHECK
# ============================================================

expected_validation_runs = (
    len(
        NOISE_LEVELS
    )
    *
    len(
        VALIDATION_SEEDS
    )
)

actual_validation_runs = (
    validation_summary[
        "validation_runs"
    ]
)


if (
    actual_validation_runs
    !=
    expected_validation_runs
):

    raise RuntimeError(
        "Held-out validation is incomplete. "
        f"Expected {expected_validation_runs} runs "
        f"but found {actual_validation_runs}."
    )


print(
    "\nValidation integrity check: PASSED"
)


# ============================================================
# PHASE 3 — GENERALISATION ANALYSIS
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "PHASE 3 — WORLD MODEL GENERALISATION ANALYSIS"
)

print(
    "=" * 80
)


classification_accuracy = (
    validation_summary[
        "classification_accuracy"
    ]
)

mean_absolute_error = (
    validation_summary[
        "mean_absolute_environment_error"
    ]
)

mean_confidence = (
    validation_summary[
        "mean_confidence"
    ]
)

mean_entropy = (
    validation_summary[
        "mean_prediction_entropy"
    ]
)

mean_diagnostic_queries = (
    validation_summary[
        "mean_diagnostic_queries"
    ]
)


print(
    "\nHeld-Out Environment Classification Accuracy:",
    f"{classification_accuracy * 100:.2f}%"
)

print(
    "Held-Out Mean Absolute Environment Error:",
    mean_absolute_error
)

print(
    "Mean Prediction Confidence:",
    mean_confidence
)

print(
    "Mean Prediction Entropy:",
    mean_entropy
)

print(
    "Mean Diagnostic Queries:",
    mean_diagnostic_queries
)


# ============================================================
# PER-ENVIRONMENT GENERALISATION
# ============================================================

print(
    "\n"
    +
    "-" * 80
)

print(
    "PER-ENVIRONMENT GENERALISATION"
)

print(
    "-" * 80
)


for environment in (
    NOISE_LEVELS
):

    result = (
        validation_summary[
            "per_environment"
        ][
            environment
        ]
    )

    print(
        "\nTrue Environment:",
        f"{environment:.2f}"
    )

    print(
        "Validation Runs:",
        result[
            "runs"
        ]
    )

    print(
        "Classification Accuracy:",
        f"{result['classification_accuracy'] * 100:.2f}%"
    )

    print(
        "Mean Absolute Environment Error:",
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


# ============================================================
# EXPERIENCE RETRIEVAL EXAMPLE
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "PHASE 4 — EXPERIENCE-BASED EXPLANATION"
)

print(
    "=" * 80
)


if (
    lab.validation_records
):

    example_record = (
        lab.validation_records[
            0
        ]
    )

    print(
        "\nExample Validation Environment:",
        f"{example_record['true_environment']:.2f}"
    )

    print(
        "World Model Prediction:",
        f"{example_record['predicted_environment']:.2f}"
    )

    print(
        "Expected Environment:",
        f"{example_record['expected_environment']:.4f}"
    )

    print(
        "Prediction Confidence:",
        f"{example_record['confidence']:.4f}"
    )

    print(
        "Nearest Historical Experience Distance:",
        example_record[
            "nearest_distance"
        ]
    )

    print(
        "Mean Neighbor Distance:",
        example_record[
            "mean_neighbor_distance"
        ]
    )


# ============================================================
# AUTONOMY CHECK
# ============================================================

lab.print_autonomy_report()


# ============================================================
# EXPERIMENTAL SCALE
# ============================================================

training_episodes = (
    len(
        NOISE_LEVELS
    )
    *
    len(
        TRAINING_SEEDS
    )
)

validation_episodes = (
    len(
        NOISE_LEVELS
    )
    *
    len(
        VALIDATION_SEEDS
    )
)

total_episodes = (
    training_episodes
    +
    validation_episodes
)


print(
    "\n"
    +
    "=" * 80
)

print(
    "EXPERIMENTAL SCALE"
)

print(
    "=" * 80
)

print(
    "Historical Training Episodes:",
    training_episodes
)

print(
    "Held-Out Validation Episodes:",
    validation_episodes
)

print(
    "Total Buyer Episodes:",
    total_episodes
)

print(
    "Environment Classes:",
    len(
        NOISE_LEVELS
    )
)

print(
    "Behavioural Features:",
    len(
        lab.world_model.feature_names
    )
)

print(
    "Training Seeds and Validation Seeds Overlap: NO"
)


# ============================================================
# SCIENTIFIC INTERPRETATION GUARDRAIL
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "INTERPRETATION GUARDRAIL"
)

print(
    "=" * 80
)

print(
    "This experiment evaluates generalisation within "
    "the simulated MARS buyer environment."
)

print(
    "It does not establish performance on real-world "
    "commercial autonomous purchasing systems."
)

print(
    "Environment labels are available during historical "
    "supervised training but hidden during validation prediction."
)


# ============================================================
# COMPLETION
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "MARS — EXPERIMENT 024 COMPLETED"
)

print(
    "=" * 80
)
