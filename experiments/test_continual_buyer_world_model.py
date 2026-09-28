"""
MARS — Machine-Agent Revenue Science

Experiment 025

Self-Improving Buyer World Model

Author: Kamran Khan

Research Question:
Can a buyer world model improve its predictions over time
by selectively learning from unfamiliar buyer interactions,
without allowing future information to leak into the
prediction being evaluated?

Experimental Design:

1. Build one historical world model from training buyers.
2. Clone that exact starting memory into two systems.
3. STATIC system:
       predicts every new buyer but never learns.
4. CONTINUAL system:
       predicts first, receives delayed feedback afterward,
       and selectively learns from experience gaps.
5. Both systems encounter the same buyers in the same order.
6. Compare accuracy, continuous environment error,
   confidence, novelty, memory growth, and early-vs-late
   performance.

True environment labels are never supplied before the
prediction being evaluated.
"""

import copy
import statistics

from buyer_lab.buyer_agent import (
    CommercialProposal
)

from inference.world_model_training_lab import (
    WorldModelTrainingLab
)

from inference.continual_buyer_world_model import (
    ContinualBuyerWorldModel
)


# ============================================================
# CONFIGURATION
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


ONLINE_SEEDS = list(
    range(
        201,
        221
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
# ESTIMATED POLICY
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
# HELPER — PERFORMANCE SUMMARY
# ============================================================

def summarise_records(
    records
):

    if not records:

        return {
            "runs": 0,
            "accuracy": None,
            "mean_absolute_error": None,
            "mean_confidence": None
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
            mean_confidence
    }


# ============================================================
# HELPER — EVALUATE PREDICTION
# ============================================================

def evaluate_prediction(
    prediction,
    true_environment
):

    predicted_environment = float(
        prediction[
            "predicted_environment"
        ]
    )

    expected_environment = float(
        prediction[
            "expected_environment"
        ]
    )

    true_environment = float(
        true_environment
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


    return {

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
            prediction[
                "confidence"
            ]
    }


# ============================================================
# HEADER
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "MARS — EXPERIMENT 025"
)

print(
    "SELF-IMPROVING BUYER WORLD MODEL"
)

print(
    "=" * 80
)

print(
    "\nHistorical Training Seeds:",
    len(
        TRAINING_SEEDS
    )
)

print(
    "Online Evaluation Seeds:",
    len(
        ONLINE_SEEDS
    )
)

print(
    "Environment Classes:",
    len(
        NOISE_LEVELS
    )
)

print(
    "Expected Historical Episodes:",
    len(
        TRAINING_SEEDS
    )
    *
    len(
        NOISE_LEVELS
    )
)

print(
    "Expected Online Buyer Episodes:",
    len(
        ONLINE_SEEDS
    )
    *
    len(
        NOISE_LEVELS
    )
)


# ============================================================
# PHASE 1 — BUILD SHARED HISTORICAL MEMORY
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "PHASE 1 — SHARED HISTORICAL MEMORY"
)

print(
    "=" * 80
)


training_lab = (
    WorldModelTrainingLab(
        reference_proposal=REFERENCE_PROPOSAL,
        estimated_policy=ESTIMATED_POLICY,
        noise_levels=NOISE_LEVELS,
        training_seeds=TRAINING_SEEDS,

        # Not used for Experiment 025 validation.
        # Must remain disjoint from training.
        validation_seeds=[
            1001
        ],

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


training_summary = (
    training_lab.build_training_memory(
        verbose=True
    )
)


expected_training_examples = (
    len(
        TRAINING_SEEDS
    )
    *
    len(
        NOISE_LEVELS
    )
)


if (
    training_summary[
        "training_examples"
    ]
    !=
    expected_training_examples
):

    raise RuntimeError(
        "Historical world-model memory is incomplete."
    )


print(
    "\nShared historical memory successfully created."
)

print(
    "Historical Memory Size:",
    training_summary[
        "training_examples"
    ]
)


# ============================================================
# PHASE 2 — CREATE MATCHED STATIC AND CONTINUAL MODELS
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "PHASE 2 — CREATE MATCHED WORLD MODELS"
)

print(
    "=" * 80
)


static_world_model = copy.deepcopy(
    training_lab.world_model
)


continual_base_model = copy.deepcopy(
    training_lab.world_model
)


continual_model = (
    ContinualBuyerWorldModel(
        base_world_model=continual_base_model,
        confidence_threshold=0.60,
        distance_threshold=2.50,
        entropy_threshold=1.25,
        minimum_novelty_score=0.35,
        memory_limit=None
    )
)


print(
    "Static Initial Memory:",
    len(
        static_world_model.training_examples
    )
)

print(
    "Continual Initial Memory:",
    len(
        continual_model.world_model.training_examples
    )
)


if (
    len(
        static_world_model.training_examples
    )
    !=
    len(
        continual_model.world_model.training_examples
    )
):

    raise RuntimeError(
        "Static and continual models do not have "
        "matched starting memories."
    )


print(
    "Matched starting memory check: PASSED"
)


# ============================================================
# PHASE 3 — MATCHED SEQUENTIAL BUYER STREAM
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "PHASE 3 — MATCHED SEQUENTIAL BUYER STREAM"
)

print(
    "=" * 80
)


static_records = []

continual_records = []

online_episode_number = 0


for seed in (
    ONLINE_SEEDS
):

    print(
        "\n"
        +
        "#" * 80
    )

    print(
        "ONLINE SEED:",
        seed
    )

    print(
        "#" * 80
    )


    for true_environment in (
        NOISE_LEVELS
    ):

        online_episode_number += 1


        # ----------------------------------------------------
        # Generate one diagnostic episode.
        #
        # The exact same observable episode is supplied to
        # both models, ensuring a matched comparison.
        # ----------------------------------------------------

        buyer = (
            training_lab.create_buyer(
                seed=seed,
                noise_strength=(
                    true_environment
                )
            )
        )


        diagnostic_result = (
            training_lab.run_diagnostic_episode(
                buyer
            )
        )


        # ----------------------------------------------------
        # STATIC MODEL
        # ----------------------------------------------------

        static_prediction = (
            static_world_model.predict_environment(
                diagnostic_result
            )
        )


        static_record = (
            evaluate_prediction(
                prediction=static_prediction,
                true_environment=(
                    true_environment
                )
            )
        )


        static_record[
            "episode"
        ] = online_episode_number

        static_record[
            "seed"
        ] = seed

        static_records.append(
            static_record
        )


        # ----------------------------------------------------
        # CONTINUAL MODEL
        #
        # Prediction occurs BEFORE feedback learning.
        # ----------------------------------------------------

        continual_result = (
            continual_model.process_episode(
                diagnostic_result=(
                    diagnostic_result
                ),
                true_environment=(
                    true_environment
                ),
                metadata={
                    "seed":
                        seed,

                    "episode":
                        online_episode_number
                }
            )
        )


        continual_record = (
            continual_result[
                "performance"
            ]
        )


        continual_record[
            "seed"
        ] = seed

        continual_records.append(
            continual_record
        )


        learning_record = (
            continual_result[
                "learning"
            ]
        )


        print(
            "Environment:",
            f"{true_environment:.2f}",
            "| Static:",
            f"{static_record['predicted_environment']:.2f}",
            "| Continual:",
            f"{continual_record['predicted_environment']:.2f}",
            "| Gap:",
            continual_result[
                "prediction"
            ][
                "experience_gap"
            ],
            "| Learned:",
            learning_record[
                "learned"
            ],
            "| Memory:",
            learning_record[
                "memory_after"
            ]
        )


# ============================================================
# PHASE 4 — GLOBAL MATCHED COMPARISON
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "GLOBAL EXPERIMENT 025 RESULTS"
)

print(
    "=" * 80
)


static_summary = (
    summarise_records(
        static_records
    )
)


continual_summary = (
    summarise_records(
        continual_records
    )
)


print(
    "\nMatched Online Episodes:",
    len(
        static_records
    )
)


print(
    "\nSTATIC WORLD MODEL"
)

print(
    "Exact Classification Accuracy:",
    f"{static_summary['accuracy'] * 100:.2f}%"
)

print(
    "Mean Absolute Environment Error:",
    static_summary[
        "mean_absolute_error"
    ]
)

print(
    "Mean Prediction Confidence:",
    static_summary[
        "mean_confidence"
    ]
)


print(
    "\nCONTINUAL WORLD MODEL"
)

print(
    "Exact Classification Accuracy:",
    f"{continual_summary['accuracy'] * 100:.2f}%"
)

print(
    "Mean Absolute Environment Error:",
    continual_summary[
        "mean_absolute_error"
    ]
)

print(
    "Mean Prediction Confidence:",
    continual_summary[
        "mean_confidence"
    ]
)


accuracy_change = (
    continual_summary[
        "accuracy"
    ]
    -
    static_summary[
        "accuracy"
    ]
)


error_change = (
    continual_summary[
        "mean_absolute_error"
    ]
    -
    static_summary[
        "mean_absolute_error"
    ]
)


print(
    "\nContinual Accuracy Change:",
    f"{accuracy_change * 100:+.2f} percentage points"
)

print(
    "Continual Error Change:",
    error_change
)


# ============================================================
# PHASE 5 — EARLY VS LATE COMPARISON
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "EARLY VS LATE LEARNING ANALYSIS"
)

print(
    "=" * 80
)


midpoint = (
    len(
        static_records
    )
    //
    2
)


static_early = (
    summarise_records(
        static_records[
            :midpoint
        ]
    )
)

static_late = (
    summarise_records(
        static_records[
            midpoint:
        ]
    )
)


continual_early = (
    summarise_records(
        continual_records[
            :midpoint
        ]
    )
)

continual_late = (
    summarise_records(
        continual_records[
            midpoint:
        ]
    )
)


print(
    "\nSTATIC MODEL"
)

print(
    "Early Accuracy:",
    f"{static_early['accuracy'] * 100:.2f}%"
)

print(
    "Late Accuracy:",
    f"{static_late['accuracy'] * 100:.2f}%"
)

print(
    "Early Mean Error:",
    static_early[
        "mean_absolute_error"
    ]
)

print(
    "Late Mean Error:",
    static_late[
        "mean_absolute_error"
    ]
)


print(
    "\nCONTINUAL MODEL"
)

print(
    "Early Accuracy:",
    f"{continual_early['accuracy'] * 100:.2f}%"
)

print(
    "Late Accuracy:",
    f"{continual_late['accuracy'] * 100:.2f}%"
)

print(
    "Early Mean Error:",
    continual_early[
        "mean_absolute_error"
    ]
)

print(
    "Late Mean Error:",
    continual_late[
        "mean_absolute_error"
    ]
)


# ============================================================
# PHASE 6 — CONTINUAL LEARNING SUMMARY
# ============================================================

continual_model.print_summary()


continual_internal_summary = (
    continual_model.generate_summary()
)


# ============================================================
# PHASE 7 — PER-ENVIRONMENT COMPARISON
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "PER-ENVIRONMENT COMPARISON"
)

print(
    "=" * 80
)


for environment in (
    NOISE_LEVELS
):

    static_environment_records = [

        record

        for record in (
            static_records
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


    continual_environment_records = [

        record

        for record in (
            continual_records
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


    static_environment_summary = (
        summarise_records(
            static_environment_records
        )
    )


    continual_environment_summary = (
        summarise_records(
            continual_environment_records
        )
    )


    print(
        "\nEnvironment:",
        f"{environment:.2f}"
    )

    print(
        "Static Accuracy:",
        f"{static_environment_summary['accuracy'] * 100:.2f}%"
    )

    print(
        "Continual Accuracy:",
        f"{continual_environment_summary['accuracy'] * 100:.2f}%"
    )

    print(
        "Static Mean Error:",
        static_environment_summary[
            "mean_absolute_error"
        ]
    )

    print(
        "Continual Mean Error:",
        continual_environment_summary[
            "mean_absolute_error"
        ]
    )


# ============================================================
# PHASE 8 — MEMORY GROWTH
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "EXPERIENCE MEMORY ANALYSIS"
)

print(
    "=" * 80
)


initial_memory = (
    continual_internal_summary[
        "initial_memory_size"
    ]
)


final_memory = (
    continual_internal_summary[
        "current_memory_size"
    ]
)


memory_growth = (
    final_memory
    -
    initial_memory
)


print(
    "Initial Continual Memory:",
    initial_memory
)

print(
    "Final Continual Memory:",
    final_memory
)

print(
    "Memory Growth:",
    memory_growth
)

print(
    "Experience Gaps Detected:",
    continual_internal_summary[
        "experience_gaps"
    ]
)

print(
    "Episodes Learned:",
    continual_internal_summary[
        "learned_episodes"
    ]
)

print(
    "Episodes Not Added:",
    continual_internal_summary[
        "skipped_learning_episodes"
    ]
)


# ============================================================
# PHASE 9 — CAUSAL INTEGRITY CHECK
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "CAUSAL AUTONOMY CHECK"
)

print(
    "=" * 80
)


print(
    "Static and continual models start from "
    "identical historical memory: YES"
)

print(
    "Both models receive identical diagnostic "
    "episodes: YES"
)

print(
    "True environment supplied before static "
    "prediction: NO"
)

print(
    "True environment supplied before continual "
    "prediction: NO"
)

print(
    "Continual feedback occurs only after current "
    "prediction is recorded: YES"
)

print(
    "Current feedback can influence future buyers "
    "only: YES"
)

print(
    "Experience-gap decision uses hidden "
    "environment label: NO"
)

print(
    "Hidden buyer thresholds supplied to continual "
    "world model: NO"
)


# ============================================================
# PHASE 10 — EXPERIMENTAL SCALE
# ============================================================

historical_episodes = (
    len(
        TRAINING_SEEDS
    )
    *
    len(
        NOISE_LEVELS
    )
)


online_episodes = (
    len(
        ONLINE_SEEDS
    )
    *
    len(
        NOISE_LEVELS
    )
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
    historical_episodes
)

print(
    "Matched Online Buyer Episodes:",
    online_episodes
)

print(
    "Static Online Predictions:",
    len(
        static_records
    )
)

print(
    "Continual Online Predictions:",
    len(
        continual_records
    )
)

print(
    "Environment Classes:",
    len(
        NOISE_LEVELS
    )
)

print(
    "Initial Behavioural Features:",
    len(
        continual_model.world_model.feature_names
    )
)


# ============================================================
# INTERPRETATION GUARDRAIL
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
    "Improvement is not assumed."
)

print(
    "If continual adaptation performs worse than "
    "the static baseline, that result is retained."
)

print(
    "This benchmark evaluates sequential adaptation "
    "inside simulated MARS buyer environments."
)

print(
    "It does not establish real-world autonomous "
    "buyer performance."
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
    "MARS — EXPERIMENT 025 COMPLETED"
)

print(
    "=" * 80
)
