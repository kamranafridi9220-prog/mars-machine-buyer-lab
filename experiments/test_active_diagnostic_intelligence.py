"""
MARS — Machine-Agent Revenue Science

Experiment 023

Active Diagnostic Intelligence Benchmark

Author: Kamran Khan

Purpose:
Compare two autonomous buyer-environment diagnostic
architectures:

BASELINE — Experiment 022
    Fixed diagnostic evidence collection.
    16 diagnostic probes.
    15 observations per probe.
    Maximum diagnostic cost = 240 buyer queries.

ACTIVE — Experiment 023
    Adaptive diagnostic evidence collection.
    Probe prioritisation.
    Sequential belief updates.
    Early stopping.
    Maximum diagnostic cost = 120 buyer queries.

The experiment evaluates whether active diagnosis can
reduce buyer-query cost while preserving downstream
policy-discovery performance.

True simulator noise is NEVER supplied to either
diagnostic architecture.

It is used only for post-experiment evaluation.
"""

import contextlib
import io
import statistics

from buyer_lab.buyer_agent import (
    CommercialProposal
)

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

from inference.active_diagnostic_intelligence_engine import (
    ActiveDiagnosticIntelligenceEngine
)


# ============================================================
# EXPERIMENT CONFIGURATION
# ============================================================

META_TRAINING_SEEDS = list(
    range(
        1,
        11
    )
)

TEST_SEEDS = list(
    range(
        201,
        206
    )
)

NOISE_LEVELS = [
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
    0.30
]

BOUNDARY_WIDTH = 0.05

FIXED_DIAGNOSTIC_OBSERVATIONS = 15

ACTIVE_MIN_OBSERVATIONS = 3

ACTIVE_MAX_OBSERVATIONS = 15

ACTIVE_BATCH_SIZE = 2

ACTIVE_MIN_TOTAL_QUERIES = 20

ACTIVE_MAX_TOTAL_QUERIES = 120

ACTIVE_CONFIDENCE_THRESHOLD = 0.80

ACTIVE_STABILITY_THRESHOLD = 0.03

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

def run_quietly(
    callable_object
):

    buffer = io.StringIO()

    with contextlib.redirect_stdout(
        buffer
    ):

        return callable_object()


# ============================================================
# POLICY METRICS
# ============================================================

def calculate_policy_metrics(
    discovered_policy,
    ground_truth
):

    errors = []

    for variable in (
        COMMERCIAL_VARIABLES
    ):

        estimated = (
            discovered_policy.get(
                variable
            )
        )

        if estimated is None:
            continue

        actual = (
            ground_truth[
                variable
            ]
        )

        variable_range = (
            SEARCH_SPACE[
                variable
            ][
                "upper"
            ]
            -
            SEARCH_SPACE[
                variable
            ][
                "lower"
            ]
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
        len(
            errors
        )
        /
        len(
            COMMERCIAL_VARIABLES
        )
    )

    mean_error = (
        statistics.mean(
            errors
        )
        if errors
        else None
    )

    return {

        "coverage":
            coverage,

        "mean_error":
            mean_error
    }


# ============================================================
# RUN POLICY DISCOVERY
# ============================================================

def run_discovery(
    buyer,
    policy
):

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

        metrics = (
            calculate_policy_metrics(
                result[
                    "discovered_policy"
                ],
                ProbabilisticBuyerFactory.ground_truth()
            )
        )

        return {

            "status":
                "SUCCESS",

            "discovered_policy":
                result[
                    "discovered_policy"
                ],

            "queries":
                result[
                    "total_queries"
                ],

            "coverage":
                metrics[
                    "coverage"
                ],

            "mean_error":
                metrics[
                    "mean_error"
                ]
        }

    except Exception as error:

        return {

            "status":
                "FAILED",

            "discovered_policy":
                {},

            "queries":
                getattr(
                    engine,
                    "query_count",
                    0
                ),

            "coverage":
                0.0,

            "mean_error":
                None,

            "error":
                (
                    f"{type(error).__name__}: "
                    f"{str(error)}"
                )
        }


# ============================================================
# TRAIN META-POLICY
# ============================================================

def train_meta_policy():

    engine = (
        MetaPolicyLearningEngine(
            accuracy_weight=ACCURACY_WEIGHT,
            query_weight=QUERY_WEIGHT,
            failure_weight=FAILURE_WEIGHT
        )
    )

    candidate_policies = (
        engine.get_candidate_policies()
    )

    training_runs = 0

    print(
        "\n"
        +
        "=" * 80
    )

    print(
        "PHASE 1 — META-POLICY TRAINING"
    )

    print(
        "=" * 80
    )

    for noise_strength in (
        NOISE_LEVELS
    ):

        print(
            "\nTraining noise regime:",
            f"{noise_strength:.2f}"
        )

        for policy in (
            candidate_policies
        ):

            for seed in (
                META_TRAINING_SEEDS
            ):

                buyer = (
                    ProbabilisticBuyerFactory.create_buyer(
                        random_seed=seed,
                        noise_strength=noise_strength,
                        boundary_width=BOUNDARY_WIDTH
                    )
                )

                result = (
                    run_discovery(
                        buyer=buyer,
                        policy=policy
                    )
                )

                engine.record_result(
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

    engine.learn_meta_policy(
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
        engine,
        training_runs
    )


# ============================================================
# FIND BALANCED POLICY
# ============================================================

def get_baseline_policy(
    meta_engine
):

    policies = (
        meta_engine.get_candidate_policies()
    )

    for policy in policies:

        if policy.name == "BALANCED":

            return policy

    return policies[0]


# ============================================================
# INITIAL BLACK-BOX POLICY ESTIMATE
# ============================================================

def obtain_initial_policy(
    buyer,
    baseline_policy
):

    result = (
        run_discovery(
            buyer=buyer,
            policy=baseline_policy
        )
    )

    if (
        result[
            "status"
        ]
        !=
        "SUCCESS"
    ):

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
# GENERATE DIAGNOSTIC PROBES
# ============================================================

def generate_probes(
    estimated_policy
):

    generator = (
        DiagnosticProbeGenerator(
            reference_proposal=REFERENCE_PROPOSAL,
            estimated_policy=estimated_policy
        )
    )

    named_probes = (
        generator.generate_named_probes()
    )

    return (
        generator,
        named_probes
    )


# ============================================================
# FIXED DIAGNOSIS — EXPERIMENT 022
# ============================================================

def run_fixed_diagnosis(
    buyer,
    named_probes
):

    proposals = [

        probe[
            "proposal"
        ]

        for probe in (
            named_probes
        )
    ]

    estimator = (
        BuyerEnvironmentEstimator(
            buyer=buyer,
            diagnostic_proposals=proposals,
            observations_per_probe=(
                FIXED_DIAGNOSTIC_OBSERVATIONS
            )
        )
    )

    return (
        estimator.estimate_environment()
    )


# ============================================================
# ACTIVE DIAGNOSIS — EXPERIMENT 023
# ============================================================

def run_active_diagnosis(
    buyer,
    named_probes
):

    engine = (
        ActiveDiagnosticIntelligenceEngine(
            buyer=buyer,
            named_probes=named_probes,
            candidate_noise_levels=NOISE_LEVELS,
            minimum_observations_per_probe=(
                ACTIVE_MIN_OBSERVATIONS
            ),
            maximum_observations_per_probe=(
                ACTIVE_MAX_OBSERVATIONS
            ),
            batch_size=(
                ACTIVE_BATCH_SIZE
            ),
            minimum_total_queries=(
                ACTIVE_MIN_TOTAL_QUERIES
            ),
            maximum_total_queries=(
                ACTIVE_MAX_TOTAL_QUERIES
            ),
            confidence_threshold=(
                ACTIVE_CONFIDENCE_THRESHOLD
            ),
            stability_threshold=(
                ACTIVE_STABILITY_THRESHOLD
            )
        )
    )

    return (
        engine.diagnose()
    )


# ============================================================
# HEADER
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "MARS — EXPERIMENT 023"
)

print(
    "ACTIVE DIAGNOSTIC INTELLIGENCE"
)

print(
    "=" * 80
)

print(
    "\nMeta-Training Seeds:",
    len(
        META_TRAINING_SEEDS
    )
)

print(
    "Test Seeds:",
    len(
        TEST_SEEDS
    )
)

print(
    "Hidden Noise Regimes:",
    len(
        NOISE_LEVELS
    )
)

print(
    "Experiment 022 Fixed Diagnostic Budget:",
    16
    *
    FIXED_DIAGNOSTIC_OBSERVATIONS
)

print(
    "Experiment 023 Active Maximum Budget:",
    ACTIVE_MAX_TOTAL_QUERIES
)


# ============================================================
# PHASE 1 — TRAIN META-POLICY
# ============================================================

meta_engine, training_runs = (
    train_meta_policy()
)

baseline_policy = (
    get_baseline_policy(
        meta_engine
    )
)


# ============================================================
# PHASE 2 — BENCHMARK
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "PHASE 2 — FIXED VS ACTIVE DIAGNOSTIC BENCHMARK"
)

print(
    "=" * 80
)

records = []


for true_noise in (
    NOISE_LEVELS
):

    print(
        "\n"
        +
        "#" * 80
    )

    print(
        "HIDDEN BUYER ENVIRONMENT:",
        f"{true_noise:.2f}"
    )

    print(
        "#" * 80
    )

    for seed in (
        TEST_SEEDS
    ):

        print(
            "\nTest Seed:",
            seed
        )

        # ----------------------------------------------------
        # INITIAL POLICY ESTIMATION
        # ----------------------------------------------------

        initial_buyer = (
            ProbabilisticBuyerFactory.create_buyer(
                random_seed=seed,
                noise_strength=true_noise,
                boundary_width=BOUNDARY_WIDTH
            )
        )

        try:

            initial_result = (
                obtain_initial_policy(
                    buyer=initial_buyer,
                    baseline_policy=baseline_policy
                )
            )

        except Exception as error:

            print(
                "Initial policy estimation failed:",
                str(error)
            )

            records.append(
                {
                    "true_noise":
                        true_noise,

                    "seed":
                        seed,

                    "status":
                        "FAILED_INITIAL_DISCOVERY"
                }
            )

            continue

        estimated_policy = (
            initial_result[
                "discovered_policy"
            ]
        )

        initial_queries = (
            initial_result[
                "queries"
            ]
        )

        generator, named_probes = (
            generate_probes(
                estimated_policy
            )
        )

        # ----------------------------------------------------
        # CREATE MATCHED BUYERS
        # ----------------------------------------------------

        fixed_buyer = (
            ProbabilisticBuyerFactory.create_buyer(
                random_seed=seed + 10000,
                noise_strength=true_noise,
                boundary_width=BOUNDARY_WIDTH
            )
        )

        active_buyer = (
            ProbabilisticBuyerFactory.create_buyer(
                random_seed=seed + 10000,
                noise_strength=true_noise,
                boundary_width=BOUNDARY_WIDTH
            )
        )

        # ----------------------------------------------------
        # FIXED DIAGNOSIS
        # ----------------------------------------------------

        fixed_environment = (
            run_fixed_diagnosis(
                buyer=fixed_buyer,
                named_probes=named_probes
            )
        )

        fixed_controller = (
            DynamicMetaPolicyController(
                meta_policy_engine=meta_engine
            )
        )

        fixed_selection = (
            fixed_controller.select_policy(
                fixed_environment
            )
        )

        fixed_policy = (
            fixed_selection[
                "selected_policy"
            ]
        )

        # ----------------------------------------------------
        # ACTIVE DIAGNOSIS
        # ----------------------------------------------------

        active_environment = (
            run_active_diagnosis(
                buyer=active_buyer,
                named_probes=named_probes
            )
        )

        active_controller = (
            DynamicMetaPolicyController(
                meta_policy_engine=meta_engine
            )
        )

        active_selection = (
            active_controller.select_policy(
                active_environment
            )
        )

        active_policy = (
            active_selection[
                "selected_policy"
            ]
        )

        # ----------------------------------------------------
        # ORACLE POLICY
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

        # ----------------------------------------------------
        # FINAL MATCHED POLICY DISCOVERY
        # ----------------------------------------------------

        fixed_final_buyer = (
            ProbabilisticBuyerFactory.create_buyer(
                random_seed=seed + 20000,
                noise_strength=true_noise,
                boundary_width=BOUNDARY_WIDTH
            )
        )

        active_final_buyer = (
            ProbabilisticBuyerFactory.create_buyer(
                random_seed=seed + 20000,
                noise_strength=true_noise,
                boundary_width=BOUNDARY_WIDTH
            )
        )

        fixed_final = (
            run_discovery(
                buyer=fixed_final_buyer,
                policy=fixed_policy
            )
        )

        active_final = (
            run_discovery(
                buyer=active_final_buyer,
                policy=active_policy
            )
        )

        # ----------------------------------------------------
        # METRICS
        # ----------------------------------------------------

        fixed_diagnostic_queries = (
            fixed_environment[
                "total_diagnostic_queries"
            ]
        )

        active_diagnostic_queries = (
            active_environment[
                "total_diagnostic_queries"
            ]
        )

        queries_saved = (
            fixed_diagnostic_queries
            -
            active_diagnostic_queries
        )

        query_reduction = (
            queries_saved
            /
            fixed_diagnostic_queries
            if fixed_diagnostic_queries
            else 0.0
        )

        fixed_noise_error = abs(
            fixed_environment[
                "estimated_noise"
            ]
            -
            true_noise
        )

        active_noise_error = abs(
            active_environment[
                "estimated_noise"
            ]
            -
            true_noise
        )

        fixed_oracle_match = (
            fixed_policy.name
            ==
            oracle_policy.name
        )

        active_oracle_match = (
            active_policy.name
            ==
            oracle_policy.name
        )

        fixed_total_queries = (
            initial_queries
            +
            fixed_diagnostic_queries
            +
            fixed_final[
                "queries"
            ]
        )

        active_total_queries = (
            initial_queries
            +
            active_diagnostic_queries
            +
            active_final[
                "queries"
            ]
        )

        print(
            "Fixed Diagnostic Queries:",
            fixed_diagnostic_queries
        )

        print(
            "Active Diagnostic Queries:",
            active_diagnostic_queries
        )

        print(
            "Diagnostic Queries Saved:",
            queries_saved
        )

        print(
            "Diagnostic Query Reduction:",
            f"{query_reduction * 100:.2f}%"
        )

        print(
            "Fixed Estimated Instability:",
            f"{fixed_environment['estimated_noise']:.4f}"
        )

        print(
            "Active Estimated Noise:",
            f"{active_environment['estimated_noise']:.4f}"
        )

        print(
            "Fixed Policy:",
            fixed_policy.name
        )

        print(
            "Active Policy:",
            active_policy.name
        )

        print(
            "Oracle Policy:",
            oracle_policy.name
        )

        print(
            "Active Stopping Reason:",
            active_environment[
                "stopping_reason"
            ]
        )

        print(
            "Fixed Final Coverage:",
            f"{fixed_final['coverage'] * 100:.2f}%"
        )

        print(
            "Active Final Coverage:",
            f"{active_final['coverage'] * 100:.2f}%"
        )

        print(
            "Fixed Final Error:",
            fixed_final[
                "mean_error"
            ]
        )

        print(
            "Active Final Error:",
            active_final[
                "mean_error"
            ]
        )

        records.append(
            {
                "true_noise":
                    true_noise,

                "seed":
                    seed,

                "status":
                    (
                        "SUCCESS"
                        if (
                            fixed_final[
                                "status"
                            ]
                            ==
                            "SUCCESS"
                            and
                            active_final[
                                "status"
                            ]
                            ==
                            "SUCCESS"
                        )
                        else
                        "FAILED"
                    ),

                "fixed_diagnostic_queries":
                    fixed_diagnostic_queries,

                "active_diagnostic_queries":
                    active_diagnostic_queries,

                "queries_saved":
                    queries_saved,

                "query_reduction":
                    query_reduction,

                "fixed_noise_error":
                    fixed_noise_error,

                "active_noise_error":
                    active_noise_error,

                "fixed_policy":
                    fixed_policy.name,

                "active_policy":
                    active_policy.name,

                "oracle_policy":
                    oracle_policy.name,

                "fixed_oracle_match":
                    fixed_oracle_match,

                "active_oracle_match":
                    active_oracle_match,

                "fixed_coverage":
                    fixed_final[
                        "coverage"
                    ],

                "active_coverage":
                    active_final[
                        "coverage"
                    ],

                "fixed_final_error":
                    fixed_final[
                        "mean_error"
                    ],

                "active_final_error":
                    active_final[
                        "mean_error"
                    ],

                "fixed_total_queries":
                    fixed_total_queries,

                "active_total_queries":
                    active_total_queries,

                "active_stopping_reason":
                    active_environment[
                        "stopping_reason"
                    ],

                "active_environment_confidence":
                    active_environment[
                        "environment_confidence"
                    ]
            }
        )


# ============================================================
# SUCCESSFUL RECORDS
# ============================================================

successful_records = [

    record

    for record in records

    if record.get(
        "status"
    ) == "SUCCESS"
]


# ============================================================
# PER-NOISE RESULTS
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "PER-ENVIRONMENT RESULTS"
)

print(
    "=" * 80
)


for noise_level in (
    NOISE_LEVELS
):

    environment_records = [

        record

        for record in (
            successful_records
        )

        if abs(
            record[
                "true_noise"
            ]
            -
            noise_level
        ) < 0.000001
    ]

    if not environment_records:

        print(
            f"\nNoise {noise_level:.2f}: "
            "NO SUCCESSFUL RUNS"
        )

        continue

    fixed_queries = statistics.mean(

        record[
            "fixed_diagnostic_queries"
        ]

        for record in (
            environment_records
        )
    )

    active_queries = statistics.mean(

        record[
            "active_diagnostic_queries"
        ]

        for record in (
            environment_records
        )
    )

    query_reduction = statistics.mean(

        record[
            "query_reduction"
        ]

        for record in (
            environment_records
        )
    )

    fixed_noise_error = statistics.mean(

        record[
            "fixed_noise_error"
        ]

        for record in (
            environment_records
        )
    )

    active_noise_error = statistics.mean(

        record[
            "active_noise_error"
        ]

        for record in (
            environment_records
        )
    )

    fixed_match = sum(

        1

        for record in (
            environment_records
        )

        if record[
            "fixed_oracle_match"
        ]

    ) / len(
        environment_records
    )

    active_match = sum(

        1

        for record in (
            environment_records
        )

        if record[
            "active_oracle_match"
        ]

    ) / len(
        environment_records
    )

    fixed_coverage = statistics.mean(

        record[
            "fixed_coverage"
        ]

        for record in (
            environment_records
        )
    )

    active_coverage = statistics.mean(

        record[
            "active_coverage"
        ]

        for record in (
            environment_records
        )
    )

    print(
        f"\nTRUE NOISE: {noise_level:.2f}"
    )

    print(
        "Fixed Mean Diagnostic Queries:",
        fixed_queries
    )

    print(
        "Active Mean Diagnostic Queries:",
        active_queries
    )

    print(
        "Mean Diagnostic Query Reduction:",
        f"{query_reduction * 100:.2f}%"
    )

    print(
        "Fixed Mean Noise Error:",
        fixed_noise_error
    )

    print(
        "Active Mean Noise Error:",
        active_noise_error
    )

    print(
        "Fixed Oracle Agreement:",
        f"{fixed_match * 100:.2f}%"
    )

    print(
        "Active Oracle Agreement:",
        f"{active_match * 100:.2f}%"
    )

    print(
        "Fixed Final Coverage:",
        f"{fixed_coverage * 100:.2f}%"
    )

    print(
        "Active Final Coverage:",
        f"{active_coverage * 100:.2f}%"
    )


# ============================================================
# GLOBAL BENCHMARK
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "GLOBAL EXPERIMENT 023 RESULTS"
)

print(
    "=" * 80
)


if successful_records:

    mean_fixed_diagnostic_queries = (
        statistics.mean(

            record[
                "fixed_diagnostic_queries"
            ]

            for record in (
                successful_records
            )
        )
    )

    mean_active_diagnostic_queries = (
        statistics.mean(

            record[
                "active_diagnostic_queries"
            ]

            for record in (
                successful_records
            )
        )
    )

    mean_queries_saved = (
        statistics.mean(

            record[
                "queries_saved"
            ]

            for record in (
                successful_records
            )
        )
    )

    mean_query_reduction = (
        statistics.mean(

            record[
                "query_reduction"
            ]

            for record in (
                successful_records
            )
        )
    )

    mean_fixed_noise_error = (
        statistics.mean(

            record[
                "fixed_noise_error"
            ]

            for record in (
                successful_records
            )
        )
    )

    mean_active_noise_error = (
        statistics.mean(

            record[
                "active_noise_error"
            ]

            for record in (
                successful_records
            )
        )
    )

    fixed_oracle_agreement = (
        sum(

            1

            for record in (
                successful_records
            )

            if record[
                "fixed_oracle_match"
            ]

        )
        /
        len(
            successful_records
        )
    )

    active_oracle_agreement = (
        sum(

            1

            for record in (
                successful_records
            )

            if record[
                "active_oracle_match"
            ]

        )
        /
        len(
            successful_records
        )
    )

    mean_fixed_coverage = (
        statistics.mean(

            record[
                "fixed_coverage"
            ]

            for record in (
                successful_records
            )
        )
    )

    mean_active_coverage = (
        statistics.mean(

            record[
                "active_coverage"
            ]

            for record in (
                successful_records
            )
        )
    )

    fixed_errors = [

        record[
            "fixed_final_error"
        ]

        for record in (
            successful_records
        )

        if record[
            "fixed_final_error"
        ] is not None
    ]

    active_errors = [

        record[
            "active_final_error"
        ]

        for record in (
            successful_records
        )

        if record[
            "active_final_error"
        ] is not None
    ]

    mean_fixed_final_error = (
        statistics.mean(
            fixed_errors
        )
        if fixed_errors
        else None
    )

    mean_active_final_error = (
        statistics.mean(
            active_errors
        )
        if active_errors
        else None
    )

    mean_fixed_total_queries = (
        statistics.mean(

            record[
                "fixed_total_queries"
            ]

            for record in (
                successful_records
            )
        )
    )

    mean_active_total_queries = (
        statistics.mean(

            record[
                "active_total_queries"
            ]

            for record in (
                successful_records
            )
        )
    )

else:

    mean_fixed_diagnostic_queries = None
    mean_active_diagnostic_queries = None
    mean_queries_saved = None
    mean_query_reduction = None
    mean_fixed_noise_error = None
    mean_active_noise_error = None
    fixed_oracle_agreement = 0.0
    active_oracle_agreement = 0.0
    mean_fixed_coverage = 0.0
    mean_active_coverage = 0.0
    mean_fixed_final_error = None
    mean_active_final_error = None
    mean_fixed_total_queries = None
    mean_active_total_queries = None


print(
    "Successful Matched Benchmark Runs:",
    len(
        successful_records
    ),
    "/",
    len(
        NOISE_LEVELS
    )
    *
    len(
        TEST_SEEDS
    )
)

print(
    "\nExperiment 022 Mean Diagnostic Queries:",
    mean_fixed_diagnostic_queries
)

print(
    "Experiment 023 Mean Diagnostic Queries:",
    mean_active_diagnostic_queries
)

print(
    "Mean Diagnostic Queries Saved:",
    mean_queries_saved
)

print(
    "Mean Diagnostic Query Reduction:",
    (
        f"{mean_query_reduction * 100:.2f}%"
        if mean_query_reduction is not None
        else None
    )
)

print(
    "\nExperiment 022 Mean Noise Error:",
    mean_fixed_noise_error
)

print(
    "Experiment 023 Mean Noise Error:",
    mean_active_noise_error
)

print(
    "\nExperiment 022 Oracle Agreement:",
    f"{fixed_oracle_agreement * 100:.2f}%"
)

print(
    "Experiment 023 Oracle Agreement:",
    f"{active_oracle_agreement * 100:.2f}%"
)

print(
    "\nExperiment 022 Final Coverage:",
    f"{mean_fixed_coverage * 100:.2f}%"
)

print(
    "Experiment 023 Final Coverage:",
    f"{mean_active_coverage * 100:.2f}%"
)

print(
    "\nExperiment 022 Final Normalised Error:",
    mean_fixed_final_error
)

print(
    "Experiment 023 Final Normalised Error:",
    mean_active_final_error
)

print(
    "\nExperiment 022 Mean Total Queries:",
    mean_fixed_total_queries
)

print(
    "Experiment 023 Mean Total Queries:",
    mean_active_total_queries
)


# ============================================================
# STOPPING BEHAVIOUR
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "ACTIVE DIAGNOSTIC STOPPING BEHAVIOUR"
)

print(
    "=" * 80
)

stopping_reasons = {}

for record in (
    successful_records
):

    reason = (
        record[
            "active_stopping_reason"
        ]
    )

    stopping_reasons[
        reason
    ] = (
        stopping_reasons.get(
            reason,
            0
        )
        +
        1
    )


for reason, count in sorted(
    stopping_reasons.items()
):

    print(
        reason,
        ":",
        count
    )


# ============================================================
# AUTONOMY CHECK
# ============================================================

print(
    "\n"
    +
    "=" * 80
)

print(
    "AUTONOMY CHECK"
)

print(
    "=" * 80
)

print(
    "True noise supplied to active diagnostic engine: NO"
)

print(
    "True noise supplied to active controller: NO"
)

print(
    "Hidden buyer thresholds supplied to diagnostic engine: NO"
)

print(
    "Probe selection determined from observed decisions: YES"
)

print(
    "Diagnostic stopping determined autonomously: YES"
)

print(
    "Environment belief updated sequentially: YES"
)

print(
    "True simulator noise used for evaluation only: YES"
)


# ============================================================
# EXPERIMENTAL SCALE
# ============================================================

meta_training_runs = (
    len(
        META_TRAINING_SEEDS
    )
    *
    len(
        NOISE_LEVELS
    )
    *
    len(
        meta_engine.get_candidate_policies()
    )
)

matched_benchmark_runs = (
    len(
        TEST_SEEDS
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
    "Meta-Policy Training Runs:",
    meta_training_runs
)

print(
    "Matched Fixed-vs-Active Buyer Environments:",
    matched_benchmark_runs
)

print(
    "Hidden Noise Regimes:",
    len(
        NOISE_LEVELS
    )
)

print(
    "Test Seeds per Noise Regime:",
    len(
        TEST_SEEDS
    )
)

print(
    "Fixed Diagnostic Query Budget:",
    (
        16
        *
        FIXED_DIAGNOSTIC_OBSERVATIONS
    )
)

print(
    "Active Maximum Diagnostic Budget:",
    ACTIVE_MAX_TOTAL_QUERIES
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
    "MARS — EXPERIMENT 023 COMPLETED"
)

print(
    "=" * 80
)
