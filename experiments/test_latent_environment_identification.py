"""
MARS — Machine-Agent Revenue Science

Experiment 022

Latent Buyer Environment Identification
and Dynamic Meta-Policy Selection

Author: Kamran Khan

Purpose:
Test whether MARS can identify the behavioural environment
of an unknown stochastic buyer from black-box observations
and autonomously select an evidence-acquisition policy.

Experiment 021 selected sampling policies using the true
simulator noise level.

Experiment 022 removes that privileged information.

MARS must:

1. Infer an approximate buyer policy.
2. Generate diagnostic proposals near inferred boundaries.
3. Observe repeated buyer decisions.
4. Estimate behavioural instability.
5. Select an evidence-acquisition policy dynamically.
6. Discover the buyer policy using that selected strategy.
7. Compare autonomous selection with an oracle that knows
   the true simulated noise level.

Ground truth and simulator noise are used only for
post-experiment evaluation.
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

from inference.buyer_environment_estimator import (
    BuyerEnvironmentEstimator
)

from inference.diagnostic_probe_generator import (
    DiagnosticProbeGenerator
)

from inference.dynamic_meta_policy_controller import (
    DynamicMetaPolicyController
)


# ============================================================
# EXPERIMENT CONFIGURATION
# ============================================================

META_TRAINING_SEEDS = list(range(1, 11))

TEST_SEEDS = list(range(101, 106))

NOISE_LEVELS = [
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
    0.30
]

BOUNDARY_WIDTH = 0.05

DIAGNOSTIC_OBSERVATIONS = 15

ACCURACY_WEIGHT = 0.55
QUERY_WEIGHT = 0.30
FAILURE_WEIGHT = 0.15


# ============================================================
# SEARCH SPACE
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
# QUIET EXECUTION
# ============================================================

def run_quietly(callable_object):

    buffer = io.StringIO()

    with contextlib.redirect_stdout(buffer):
        return callable_object()


# ============================================================
# POLICY ERROR
# ============================================================

def calculate_policy_metrics(
    discovered_policy,
    ground_truth
):

    errors = []

    for variable in COMMERCIAL_VARIABLES:

        estimated = discovered_policy.get(
            variable
        )

        if estimated is None:
            continue

        actual = ground_truth[
            variable
        ]

        variable_range = (
            SEARCH_SPACE[variable]["upper"]
            -
            SEARCH_SPACE[variable]["lower"]
        )

        if variable_range <= 0:
            error = 0.0

        else:
            error = (
                abs(
                    estimated
                    -
                    actual
                )
                /
                variable_range
            )

        errors.append(
            error
        )

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
# RUN ADAPTIVE DISCOVERY
# ============================================================

def run_discovery(
    buyer,
    policy
):

    engine = AdaptiveSequentialEvidenceEngine(
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
            "discovered_policy": (
                result["discovered_policy"]
            ),
            "queries": (
                result["total_queries"]
            ),
            "coverage": (
                metrics["coverage"]
            ),
            "mean_error": (
                metrics["mean_error"]
            )
        }

    except Exception as error:

        return {
            "status": "FAILED",
            "discovered_policy": {},
            "queries": getattr(
                engine,
                "query_count",
                0
            ),
            "coverage": 0.0,
            "mean_error": None,
            "error": (
                f"{type(error).__name__}: "
                f"{str(error)}"
            )
        }


# ============================================================
# TRAIN META-POLICY
# ============================================================

def train_meta_policy():

    meta_engine = MetaPolicyLearningEngine(
        accuracy_weight=ACCURACY_WEIGHT,
        query_weight=QUERY_WEIGHT,
        failure_weight=FAILURE_WEIGHT
    )

    candidate_policies = (
        meta_engine.get_candidate_policies()
    )

    training_runs = 0

    print("\n" + "=" * 80)
    print("PHASE 1 — META-POLICY TRAINING")
    print("=" * 80)

    for noise_strength in NOISE_LEVELS:

        print(
            f"\nTraining noise regime: "
            f"{noise_strength:.2f}"
        )

        for policy in candidate_policies:

            for seed in META_TRAINING_SEEDS:

                buyer = (
                    ProbabilisticBuyerFactory.create_buyer(
                        random_seed=seed,
                        noise_strength=noise_strength,
                        boundary_width=BOUNDARY_WIDTH
                    )
                )

                result = run_discovery(
                    buyer=buyer,
                    policy=policy
                )

                meta_engine.record_result(
                    noise_strength=noise_strength,
                    seed=seed,
                    policy=policy,
                    status=result["status"],
                    mean_error=result["mean_error"],
                    queries=result["queries"],
                    coverage=result["coverage"],
                    early_stop_rate=None,
                    average_observations=None
                )

                training_runs += 1

        print(
            "Completed training runs:",
            training_runs
        )

    meta_engine.learn_meta_policy(
        NOISE_LEVELS
    )

    print(
        "\nMeta-policy training completed."
    )

    print(
        "Training discovery runs:",
        training_runs
    )

    return (
        meta_engine,
        training_runs
    )


# ============================================================
# INITIAL POLICY ESTIMATE
# ============================================================

def obtain_initial_policy_estimate(
    buyer,
    baseline_policy
):

    """
    Obtain an initial black-box policy estimate.

    This estimate is used only to position diagnostic
    probes close to likely commercial boundaries.
    """

    result = run_discovery(
        buyer=buyer,
        policy=baseline_policy
    )

    if result["status"] != "SUCCESS":

        raise RuntimeError(
            "Initial policy discovery failed: "
            +
            result.get(
                "error",
                "Unknown error"
            )
        )

    return result


# ============================================================
# DIAGNOSTIC ENVIRONMENT ESTIMATION
# ============================================================

def estimate_environment(
    buyer,
    estimated_policy
):

    generator = DiagnosticProbeGenerator(
        reference_proposal=REFERENCE_PROPOSAL,
        estimated_policy=estimated_policy
    )

    named_probes = (
        generator.generate_named_probes()
    )

    diagnostic_proposals = [
        probe["proposal"]
        for probe in named_probes
    ]

    estimator = BuyerEnvironmentEstimator(
        buyer=buyer,
        diagnostic_proposals=diagnostic_proposals,
        observations_per_probe=(
            DIAGNOSTIC_OBSERVATIONS
        )
    )

    environment_result = (
        estimator.estimate_environment()
    )

    return (
        environment_result,
        generator.generate_summary()
    )


# ============================================================
# HEADER
# ============================================================

print("\n" + "=" * 80)
print("MARS — EXPERIMENT 022")
print("LATENT BUYER ENVIRONMENT IDENTIFICATION")
print("AND DYNAMIC META-POLICY SELECTION")
print("=" * 80)

print(
    "\nMeta-Training Seeds:",
    len(META_TRAINING_SEEDS)
)

print(
    "Test Seeds:",
    len(TEST_SEEDS)
)

print(
    "Hidden Noise Regimes:",
    len(NOISE_LEVELS)
)

print(
    "Diagnostic Observations per Probe:",
    DIAGNOSTIC_OBSERVATIONS
)


# ============================================================
# TRAIN EXPERIMENT 021 META-POLICY
# ============================================================

meta_engine, training_runs = (
    train_meta_policy()
)

controller = DynamicMetaPolicyController(
    meta_policy_engine=meta_engine
)

candidate_policies = (
    meta_engine.get_candidate_policies()
)

baseline_policy = None

for policy in candidate_policies:

    if policy.name == "BALANCED":
        baseline_policy = policy
        break

if baseline_policy is None:
    baseline_policy = candidate_policies[0]


# ============================================================
# CLOSED-LOOP TESTING
# ============================================================

print("\n" + "=" * 80)
print("PHASE 2 — UNKNOWN BUYER CLOSED-LOOP TESTING")
print("=" * 80)

test_records = []

for true_noise in NOISE_LEVELS:

    print("\n" + "#" * 80)

    print(
        f"HIDDEN BUYER ENVIRONMENT: "
        f"{true_noise:.2f}"
    )

    print("#" * 80)

    for seed in TEST_SEEDS:

        print(
            f"\nTest Seed: {seed}"
        )

        buyer = (
            ProbabilisticBuyerFactory.create_buyer(
                random_seed=seed,
                noise_strength=true_noise,
                boundary_width=BOUNDARY_WIDTH
            )
        )

        # ----------------------------------------------------
        # STEP A — INITIAL BLACK-BOX POLICY ESTIMATE
        # ----------------------------------------------------

        try:

            initial_result = (
                obtain_initial_policy_estimate(
                    buyer=buyer,
                    baseline_policy=baseline_policy
                )
            )

        except Exception as error:

            print(
                "Initial policy discovery failed:",
                str(error)
            )

            test_records.append(
                {
                    "true_noise": true_noise,
                    "seed": seed,
                    "status": "FAILED_INITIAL_DISCOVERY"
                }
            )

            continue

        initial_policy = (
            initial_result[
                "discovered_policy"
            ]
        )

        initial_queries = (
            initial_result[
                "queries"
            ]
        )

        # ----------------------------------------------------
        # STEP B — GENERATE DIAGNOSTIC PROBES
        # ----------------------------------------------------

        try:

            environment_result, probe_summary = (
                estimate_environment(
                    buyer=buyer,
                    estimated_policy=initial_policy
                )
            )

        except Exception as error:

            print(
                "Environment estimation failed:",
                str(error)
            )

            test_records.append(
                {
                    "true_noise": true_noise,
                    "seed": seed,
                    "status": "FAILED_ENVIRONMENT_ESTIMATION"
                }
            )

            continue

        estimated_noise = (
            environment_result[
                "estimated_noise"
            ]
        )

        diagnostic_queries = (
            environment_result[
                "total_diagnostic_queries"
            ]
        )

        # ----------------------------------------------------
        # STEP C — DYNAMIC META-POLICY SELECTION
        # ----------------------------------------------------

        dynamic_selection = (
            controller.select_policy(
                environment_result
            )
        )

        selected_policy = (
            dynamic_selection[
                "selected_policy"
            ]
        )

        # ----------------------------------------------------
        # STEP D — ORACLE POLICY SELECTION
        # ----------------------------------------------------

        oracle_selection = (
            meta_engine.select_policy(
                estimated_noise=true_noise
            )
        )

        oracle_policy = (
            oracle_selection[
                "selected_policy"
            ]
        )

        policy_match = (
            selected_policy.name
            ==
            oracle_policy.name
        )

        # ----------------------------------------------------
        # STEP E — FINAL POLICY DISCOVERY
        # ----------------------------------------------------

        final_buyer = (
            ProbabilisticBuyerFactory.create_buyer(
                random_seed=seed + 10000,
                noise_strength=true_noise,
                boundary_width=BOUNDARY_WIDTH
            )
        )

        final_result = (
            run_discovery(
                buyer=final_buyer,
                policy=selected_policy
            )
        )

        final_queries = (
            final_result[
                "queries"
            ]
        )

        total_queries = (
            initial_queries
            +
            diagnostic_queries
            +
            final_queries
        )

        noise_estimation_error = abs(
            estimated_noise
            -
            true_noise
        )

        print(
            "Estimated Behavioural Instability:",
            f"{estimated_noise:.4f}"
        )

        print(
            "True Simulator Noise:",
            f"{true_noise:.4f}"
        )

        print(
            "Noise Estimation Error:",
            f"{noise_estimation_error:.4f}"
        )

        print(
            "Dynamic Policy:",
            selected_policy.name
        )

        print(
            "Oracle Policy:",
            oracle_policy.name
        )

        print(
            "Policy Match:",
            policy_match
        )

        print(
            "Final Discovery Status:",
            final_result["status"]
        )

        print(
            "Final Coverage:",
            f"{final_result['coverage'] * 100:.2f}%"
        )

        print(
            "Final Mean Error:",
            final_result["mean_error"]
        )

        print(
            "Initial Queries:",
            initial_queries
        )

        print(
            "Diagnostic Queries:",
            diagnostic_queries
        )

        print(
            "Final Queries:",
            final_queries
        )

        print(
            "Total Closed-Loop Queries:",
            total_queries
        )

        test_records.append(
            {
                "true_noise": true_noise,
                "seed": seed,
                "status": final_result["status"],
                "estimated_noise": estimated_noise,
                "noise_estimation_error": (
                    noise_estimation_error
                ),
                "dynamic_policy": (
                    selected_policy.name
                ),
                "oracle_policy": (
                    oracle_policy.name
                ),
                "policy_match": policy_match,
                "estimation_confidence": (
                    dynamic_selection[
                        "estimation_confidence"
                    ]
                ),
                "initial_queries": (
                    initial_queries
                ),
                "diagnostic_queries": (
                    diagnostic_queries
                ),
                "final_queries": (
                    final_queries
                ),
                "total_queries": (
                    total_queries
                ),
                "coverage": (
                    final_result[
                        "coverage"
                    ]
                ),
                "mean_error": (
                    final_result[
                        "mean_error"
                    ]
                ),
                "probe_count": (
                    probe_summary[
                        "total_probes"
                    ]
                )
            }
        )


# ============================================================
# SUCCESSFUL TEST RECORDS
# ============================================================

successful_records = [
    record
    for record in test_records
    if record.get("status") == "SUCCESS"
]


# ============================================================
# NOISE-LEVEL SUMMARY
# ============================================================

print("\n" + "=" * 80)
print("LATENT ENVIRONMENT IDENTIFICATION RESULTS")
print("=" * 80)

for true_noise in NOISE_LEVELS:

    records = [
        record
        for record in successful_records
        if abs(
            record["true_noise"]
            -
            true_noise
        ) < 0.000001
    ]

    if not records:

        print(
            f"\nNoise {true_noise:.2f}: "
            "NO SUCCESSFUL RUNS"
        )

        continue

    estimated_noise_values = [
        record["estimated_noise"]
        for record in records
    ]

    estimation_errors = [
        record["noise_estimation_error"]
        for record in records
    ]

    policy_matches = [
        record["policy_match"]
        for record in records
    ]

    coverages = [
        record["coverage"]
        for record in records
    ]

    final_errors = [
        record["mean_error"]
        for record in records
        if record["mean_error"] is not None
    ]

    total_queries = [
        record["total_queries"]
        for record in records
    ]

    mean_estimated_noise = (
        statistics.mean(
            estimated_noise_values
        )
    )

    mean_noise_error = (
        statistics.mean(
            estimation_errors
        )
    )

    policy_match_rate = (
        sum(
            1
            for value in policy_matches
            if value
        )
        /
        len(policy_matches)
    )

    mean_coverage = (
        statistics.mean(
            coverages
        )
    )

    mean_final_error = (
        statistics.mean(
            final_errors
        )
        if final_errors
        else None
    )

    mean_total_queries = (
        statistics.mean(
            total_queries
        )
    )

    print(
        f"\nTRUE NOISE: {true_noise:.2f}"
    )

    print(
        "Mean Estimated Instability:",
        f"{mean_estimated_noise:.6f}"
    )

    print(
        "Mean Absolute Estimation Error:",
        f"{mean_noise_error:.6f}"
    )

    print(
        "Oracle Policy Agreement:",
        f"{policy_match_rate * 100:.2f}%"
    )

    print(
        "Mean Policy Coverage:",
        f"{mean_coverage * 100:.2f}%"
    )

    print(
        "Mean Final Normalised Error:",
        mean_final_error
    )

    print(
        "Mean Closed-Loop Queries:",
        mean_total_queries
    )


# ============================================================
# GLOBAL RESULTS
# ============================================================

print("\n" + "=" * 80)
print("GLOBAL EXPERIMENT 022 RESULTS")
print("=" * 80)

total_test_runs = (
    len(NOISE_LEVELS)
    *
    len(TEST_SEEDS)
)

successful_test_runs = (
    len(successful_records)
)

success_rate = (
    successful_test_runs
    /
    total_test_runs
    if total_test_runs
    else 0.0
)

if successful_records:

    global_noise_error = (
        statistics.mean(
            record[
                "noise_estimation_error"
            ]
            for record in successful_records
        )
    )

    global_policy_match = (
        sum(
            1
            for record in successful_records
            if record[
                "policy_match"
            ]
        )
        /
        len(successful_records)
    )

    global_coverage = (
        statistics.mean(
            record[
                "coverage"
            ]
            for record in successful_records
        )
    )

    valid_final_errors = [
        record["mean_error"]
        for record in successful_records
        if record["mean_error"] is not None
    ]

    global_final_error = (
        statistics.mean(
            valid_final_errors
        )
        if valid_final_errors
        else None
    )

    global_queries = (
        statistics.mean(
            record[
                "total_queries"
            ]
            for record in successful_records
        )
    )

    global_diagnostic_queries = (
        statistics.mean(
            record[
                "diagnostic_queries"
            ]
            for record in successful_records
        )
    )

else:

    global_noise_error = None
    global_policy_match = 0.0
    global_coverage = 0.0
    global_final_error = None
    global_queries = None
    global_diagnostic_queries = None


print(
    "Meta-Policy Training Runs:",
    training_runs
)

print(
    "Closed-Loop Test Runs:",
    total_test_runs
)

print(
    "Successful Test Runs:",
    successful_test_runs
)

print(
    "Closed-Loop Success Rate:",
    f"{success_rate * 100:.2f}%"
)

print(
    "Mean Behavioural-Noise Estimation Error:",
    global_noise_error
)

print(
    "Dynamic vs Oracle Policy Agreement:",
    f"{global_policy_match * 100:.2f}%"
)

print(
    "Mean Final Policy Coverage:",
    f"{global_coverage * 100:.2f}%"
)

print(
    "Mean Final Normalised Error:",
    global_final_error
)

print(
    "Mean Diagnostic Query Cost:",
    global_diagnostic_queries
)

print(
    "Mean Total Closed-Loop Queries:",
    global_queries
)


# ============================================================
# AUTONOMY CHECK
# ============================================================

print("\n" + "=" * 80)
print("AUTONOMY CHECK")
print("=" * 80)

print(
    "True noise supplied to environment estimator: NO"
)

print(
    "True noise supplied to dynamic controller: NO"
)

print(
    "Hidden buyer thresholds supplied to estimator: NO"
)

print(
    "Diagnostic probes generated from inferred policy: YES"
)

print(
    "Sampling policy selected from observed behaviour: YES"
)

print(
    "True simulator noise used for evaluation only: YES"
)


# ============================================================
# EXPERIMENTAL SCALE
# ============================================================

meta_training_scale = (
    len(META_TRAINING_SEEDS)
    *
    len(NOISE_LEVELS)
    *
    len(candidate_policies)
)

closed_loop_scale = (
    len(TEST_SEEDS)
    *
    len(NOISE_LEVELS)
)

print("\n" + "=" * 80)
print("EXPERIMENTAL SCALE")
print("=" * 80)

print(
    "Meta-Policy Training Discovery Runs:",
    meta_training_scale
)

print(
    "Unknown Buyer Closed-Loop Runs:",
    closed_loop_scale
)

print(
    "Hidden Noise Regimes:",
    len(NOISE_LEVELS)
)

print(
    "Test Seeds per Environment:",
    len(TEST_SEEDS)
)

print(
    "Diagnostic Observations per Probe:",
    DIAGNOSTIC_OBSERVATIONS
)

print(
    "Total High-Level Experimental Runs:",
    (
        meta_training_scale
        +
        closed_loop_scale
    )
)


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 80)
print("MARS — EXPERIMENT 022 COMPLETED")
print("=" * 80)
