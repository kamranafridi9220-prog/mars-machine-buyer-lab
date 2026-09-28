"""
MARS — Machine-Agent Revenue Science

Experiment 021

Autonomous Meta-Policy Learning

Author: Kamran Khan

Purpose:
Evaluate multiple adaptive evidence-acquisition policies
across stochastic buyer environments and learn which
sampling configuration provides the strongest trade-off
between policy-estimation accuracy, buyer-query cost,
and discovery reliability.

Research Question:
Can MARS learn how aggressively it should acquire
evidence instead of relying on one manually fixed
sampling configuration?

Ground-truth buyer policy is used only for
post-discovery evaluation.
"""

import contextlib
import io
import statistics

from buyer_lab.buyer_agent import CommercialProposal

from buyer_lab.probabilistic_buyer_agent import (
    ProbabilisticBuyerFactory
)

from inference.adaptive_sequential_evidence_engine import (
    AdaptiveSequentialEvidenceEngine
)

from inference.meta_policy_learning_engine import (
    MetaPolicyLearningEngine
)


# ============================================================
# EXPERIMENT CONFIGURATION
# ============================================================

TRAINING_SEEDS = list(range(1, 16))

VALIDATION_SEEDS = list(range(101, 106))

NOISE_LEVELS = [
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
    0.30
]

BOUNDARY_WIDTH = 0.05

ACCURACY_WEIGHT = 0.55
QUERY_WEIGHT = 0.30
FAILURE_WEIGHT = 0.15


# ============================================================
# COMMERCIAL SEARCH SPACE
# ============================================================

SEARCH_SPACE = {

    "annual_price": {
        "lower": 50000.0,
        "upper": 150000.0
    },

    "contract_months": {
        "lower": 12,
        "upper": 60
    },

    "service_availability": {
        "lower": 90.0,
        "upper": 100.0
    },

    "payment_days": {
        "lower": 7,
        "upper": 90
    },

    "supplier_reliability": {
        "lower": 60.0,
        "upper": 100.0
    }
}


COMMERCIAL_VARIABLES = [
    "annual_price",
    "contract_months",
    "service_availability",
    "payment_days",
    "supplier_reliability"
]


# ============================================================
# COMMON REFERENCE PROPOSAL
# ============================================================

REFERENCE_PROPOSAL = CommercialProposal(
    annual_price=80000,
    contract_months=12,
    service_availability=100.0,
    payment_days=60,
    supplier_reliability=100.0
)


# ============================================================
# QUIET EXECUTION
# ============================================================

def run_quietly(callable_object):

    buffer = io.StringIO()

    with contextlib.redirect_stdout(buffer):
        return callable_object()


# ============================================================
# NORMALISED POLICY ERROR
# ============================================================

def calculate_policy_metrics(
    discovered_policy,
    ground_truth
):

    errors = []

    for variable in COMMERCIAL_VARIABLES:

        estimated = discovered_policy.get(variable)

        if estimated is None:
            continue

        actual = ground_truth[variable]

        variable_range = (
            SEARCH_SPACE[variable]["upper"]
            -
            SEARCH_SPACE[variable]["lower"]
        )

        if variable_range <= 0:
            error = 0.0

        else:
            error = (
                abs(estimated - actual)
                /
                variable_range
            )

        errors.append(error)

    coverage = (
        len(errors)
        /
        len(COMMERCIAL_VARIABLES)
    )

    mean_error = (
        statistics.mean(errors)
        if errors
        else None
    )

    return {
        "coverage": coverage,
        "mean_error": mean_error
    }


# ============================================================
# RUN ONE ADAPTIVE POLICY
# ============================================================

def run_policy(
    seed,
    noise_strength,
    policy
):

    buyer = (
        ProbabilisticBuyerFactory.create_buyer(
            random_seed=seed,
            noise_strength=noise_strength,
            boundary_width=BOUNDARY_WIDTH
        )
    )

    engine = (
        AdaptiveSequentialEvidenceEngine(
            buyer=buyer,
            reference_proposal=REFERENCE_PROPOSAL,
            minimum_observations=(
                policy.minimum_observations
            ),
            maximum_observations=(
                policy.maximum_observations
            ),
            confidence_level=(
                policy.confidence_level
            ),
            acceptance_threshold=0.50
        )
    )

    try:

        result = run_quietly(
            engine.discover_policy
        )

        metrics = calculate_policy_metrics(
            result["discovered_policy"],
            ProbabilisticBuyerFactory.ground_truth()
        )

        return {
            "status": "SUCCESS",
            "mean_error": metrics["mean_error"],
            "coverage": metrics["coverage"],
            "queries": result["total_queries"],
            "early_stop_rate": result.get(
                "early_stop_rate"
            ),
            "average_observations": result.get(
                "average_observations_per_candidate"
            )
        }

    except Exception as error:

        return {
            "status": "FAILED",
            "mean_error": None,
            "coverage": 0.0,
            "queries": getattr(
                engine,
                "query_count",
                0
            ),
            "early_stop_rate": None,
            "average_observations": None,
            "error": (
                f"{type(error).__name__}: "
                f"{str(error)}"
            )
        }


# ============================================================
# EXPERIMENT HEADER
# ============================================================

print("\n" + "=" * 80)
print("MARS — EXPERIMENT 021")
print("AUTONOMOUS META-POLICY LEARNING")
print("=" * 80)

print(
    "\nTraining Seeds:",
    len(TRAINING_SEEDS)
)

print(
    "Validation Seeds:",
    len(VALIDATION_SEEDS)
)

print(
    "Noise Regimes:",
    len(NOISE_LEVELS)
)


# ============================================================
# INITIALISE META-LEARNER
# ============================================================

meta_learner = MetaPolicyLearningEngine(
    accuracy_weight=ACCURACY_WEIGHT,
    query_weight=QUERY_WEIGHT,
    failure_weight=FAILURE_WEIGHT
)

candidate_policies = (
    meta_learner.get_candidate_policies()
)

print(
    "Candidate Sampling Policies:",
    len(candidate_policies)
)

print("\nObjective Weights:")

print(
    "Accuracy:",
    ACCURACY_WEIGHT
)

print(
    "Query Efficiency:",
    QUERY_WEIGHT
)

print(
    "Failure Avoidance:",
    FAILURE_WEIGHT
)

print("\nCandidate Policies:")

for policy in candidate_policies:

    print(
        f"  {policy.name}: "
        f"min={policy.minimum_observations}, "
        f"max={policy.maximum_observations}, "
        f"confidence={policy.confidence_level}"
    )


# ============================================================
# TRAINING PHASE
# ============================================================

print("\n" + "=" * 80)
print("META-POLICY TRAINING PHASE")
print("=" * 80)

training_runs = 0

for noise_strength in NOISE_LEVELS:

    print(
        f"\nTraining Noise Regime: "
        f"{noise_strength:.2f}"
    )

    for policy in candidate_policies:

        for seed in TRAINING_SEEDS:

            result = run_policy(
                seed=seed,
                noise_strength=noise_strength,
                policy=policy
            )

            meta_learner.record_result(
                noise_strength=noise_strength,
                seed=seed,
                policy=policy,
                status=result["status"],
                mean_error=result["mean_error"],
                queries=result["queries"],
                coverage=result["coverage"],
                early_stop_rate=(
                    result["early_stop_rate"]
                ),
                average_observations=(
                    result["average_observations"]
                )
            )

            training_runs += 1

    print(
        "Completed Training Runs:",
        training_runs
    )


# ============================================================
# LEARN META-POLICY
# ============================================================

learned_policy = (
    meta_learner.learn_meta_policy(
        NOISE_LEVELS
    )
)

meta_learner.print_meta_policy()


# ============================================================
# PRINT ALL POLICY SCORES
# ============================================================

print("\n" + "=" * 80)
print("META-POLICY TRAINING COMPARISON")
print("=" * 80)

for noise_strength in NOISE_LEVELS:

    scores = meta_learner.score_policies(
        noise_strength
    )

    print(
        f"\nNOISE STRENGTH: "
        f"{noise_strength:.2f}"
    )

    for policy_name, result in scores.items():

        print(
            f"{policy_name:15} | "
            f"Error: {result['mean_error']} | "
            f"Queries: {result['mean_queries']} | "
            f"Success: "
            f"{result['success_rate'] * 100:.2f}% | "
            f"Objective: "
            f"{result['objective_cost']:.6f}"
        )


# ============================================================
# VALIDATION PHASE
# ============================================================

print("\n" + "=" * 80)
print("OUT-OF-SAMPLE META-POLICY VALIDATION")
print("=" * 80)

validation_records = []

for noise_strength in NOISE_LEVELS:

    selection = meta_learner.select_policy(
        estimated_noise=noise_strength
    )

    selected_policy = (
        selection["selected_policy"]
    )

    print(
        f"\nNoise Strength: "
        f"{noise_strength:.2f}"
    )

    print(
        "Selected Policy:",
        selected_policy.name
    )

    for seed in VALIDATION_SEEDS:

        result = run_policy(
            seed=seed,
            noise_strength=noise_strength,
            policy=selected_policy
        )

        validation_records.append(
            {
                "noise_strength": noise_strength,
                "seed": seed,
                "policy_name": selected_policy.name,
                **result
            }
        )


# ============================================================
# VALIDATION SUMMARY
# ============================================================

print("\n" + "=" * 80)
print("OUT-OF-SAMPLE VALIDATION RESULTS")
print("=" * 80)

for noise_strength in NOISE_LEVELS:

    records = [
        record
        for record in validation_records
        if abs(
            record["noise_strength"]
            -
            noise_strength
        ) < 0.000001
    ]

    successful = [
        record
        for record in records
        if record["status"] == "SUCCESS"
    ]

    errors = [
        record["mean_error"]
        for record in successful
        if record["mean_error"] is not None
    ]

    queries = [
        record["queries"]
        for record in successful
    ]

    coverages = [
        record["coverage"]
        for record in successful
    ]

    if records:
        policy_name = records[0]["policy_name"]
    else:
        policy_name = "NONE"

    if errors:
        mean_error = statistics.mean(errors)
    else:
        mean_error = None

    if queries:
        mean_queries = statistics.mean(queries)
    else:
        mean_queries = None

    if coverages:
        mean_coverage = statistics.mean(coverages)
    else:
        mean_coverage = 0.0

    if records:
        success_rate = (
            len(successful)
            /
            len(records)
        )
    else:
        success_rate = 0.0

    print(
        f"\nNoise: {noise_strength:.2f}"
    )

    print(
        "Selected Policy:",
        policy_name
    )

    print(
        "Validation Runs:",
        len(records)
    )

    print(
        "Success Rate:",
        f"{success_rate * 100:.2f}%"
    )

    print(
        "Mean Coverage:",
        f"{mean_coverage * 100:.2f}%"
    )

    print(
        "Mean Normalised Error:",
        mean_error
    )

    print(
        "Mean Buyer Queries:",
        mean_queries
    )


# ============================================================
# GLOBAL VALIDATION SUMMARY
# ============================================================

successful_validation = [
    record
    for record in validation_records
    if record["status"] == "SUCCESS"
]

validation_errors = [
    record["mean_error"]
    for record in successful_validation
    if record["mean_error"] is not None
]

validation_queries = [
    record["queries"]
    for record in successful_validation
]

validation_coverages = [
    record["coverage"]
    for record in successful_validation
]


if validation_records:

    validation_success_rate = (
        len(successful_validation)
        /
        len(validation_records)
        *
        100
    )

else:

    validation_success_rate = 0.0


if validation_coverages:

    mean_validation_coverage = (
        statistics.mean(
            validation_coverages
        )
        *
        100
    )

    coverage_display = (
        f"{mean_validation_coverage:.2f}%"
    )

else:

    coverage_display = "N/A"


if validation_errors:

    mean_validation_error = (
        statistics.mean(
            validation_errors
        )
    )

else:

    mean_validation_error = None


if validation_queries:

    mean_validation_queries = (
        statistics.mean(
            validation_queries
        )
    )

else:

    mean_validation_queries = None


print("\n" + "=" * 80)
print("GLOBAL META-POLICY VALIDATION")
print("=" * 80)

print(
    "Training Runs:",
    training_runs
)

print(
    "Validation Runs:",
    len(validation_records)
)

print(
    "Successful Validation Runs:",
    len(successful_validation)
)

print(
    "Validation Success Rate:",
    f"{validation_success_rate:.2f}%"
)

print(
    "Mean Validation Coverage:",
    coverage_display
)

print(
    "Mean Validation Error:",
    mean_validation_error
)

print(
    "Mean Validation Queries:",
    mean_validation_queries
)


# ============================================================
# LEARNED POLICY MAP
# ============================================================

print("\n" + "=" * 80)
print("LEARNED EVIDENCE-ACQUISITION POLICY MAP")
print("=" * 80)

for noise_strength in NOISE_LEVELS:

    result = learned_policy[
        noise_strength
    ]

    policy = result[
        "selected_policy"
    ]

    print(
        f"Noise {noise_strength:.2f} "
        f"-> {policy.name} "
        f"(min={policy.minimum_observations}, "
        f"max={policy.maximum_observations}, "
        f"confidence={policy.confidence_level})"
    )


# ============================================================
# FAILURE ANALYSIS
# ============================================================

print("\n" + "=" * 80)
print("VALIDATION FAILURE ANALYSIS")
print("=" * 80)

failed_validation = [
    record
    for record in validation_records
    if record["status"] != "SUCCESS"
]

print(
    "Failed Validation Runs:",
    len(failed_validation)
)

if failed_validation:

    failure_reasons = {}

    for record in failed_validation:

        reason = record.get(
            "error",
            "Unknown failure"
        )

        failure_reasons[reason] = (
            failure_reasons.get(
                reason,
                0
            )
            +
            1
        )

    for reason, count in failure_reasons.items():

        print(
            f"{count}x — {reason}"
        )

else:

    print(
        "No validation failures detected."
    )


# ============================================================
# EXPERIMENTAL SCALE
# ============================================================

TOTAL_TRAINING_RUNS = (
    len(TRAINING_SEEDS)
    *
    len(NOISE_LEVELS)
    *
    len(candidate_policies)
)

TOTAL_VALIDATION_RUNS = (
    len(VALIDATION_SEEDS)
    *
    len(NOISE_LEVELS)
)

TOTAL_EXPERIMENT_RUNS = (
    TOTAL_TRAINING_RUNS
    +
    TOTAL_VALIDATION_RUNS
)


print("\n" + "=" * 80)
print("EXPERIMENTAL SCALE")
print("=" * 80)

print(
    "Training Seeds:",
    len(TRAINING_SEEDS)
)

print(
    "Validation Seeds:",
    len(VALIDATION_SEEDS)
)

print(
    "Noise Regimes:",
    len(NOISE_LEVELS)
)

print(
    "Candidate Meta-Policies:",
    len(candidate_policies)
)

print(
    "Training Discovery Runs:",
    TOTAL_TRAINING_RUNS
)

print(
    "Validation Discovery Runs:",
    TOTAL_VALIDATION_RUNS
)

print(
    "Total Experiment 021 Runs:",
    TOTAL_EXPERIMENT_RUNS
)


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 80)
print("MARS — EXPERIMENT 021 COMPLETED")
print("=" * 80)
