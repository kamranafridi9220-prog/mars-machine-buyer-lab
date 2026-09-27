"""
MARS — Machine-Agent Revenue Science

Experiment 014

Comparative Black-Box Buyer Policy Discovery Benchmark

Author: Kamran Khan

Research Objective:
Compare the fixed multi-dimensional policy inference
architecture from Experiment 003 with the autonomous
next-best experiment selection architecture introduced
in Experiment 013.

Evaluation dimensions:

1. Buyer query count
2. Policy discovery coverage
3. Threshold accuracy
4. Absolute threshold error
5. Normalised threshold error
6. Residual uncertainty
7. Queries required per discovered policy

IMPORTANT:
Ground-truth buyer thresholds are used only by the
benchmark after discovery has completed. They are not
provided to either discovery algorithm.
"""

from buyer_lab.buyer_agent import (
    AutonomousBuyerAgent,
    CommercialProposal
)

from inference.multidimensional_inference import (
    MultiDimensionalInferenceEngine
)

from inference.autonomous_experiment_selector import (
    AutonomousExperimentSelector
)

from evaluation.policy_discovery_benchmark import (
    PolicyDiscoveryBenchmark
)


# ============================================================
# EXPERIMENT CONFIGURATION
# ============================================================

MAXIMUM_AUTONOMOUS_QUERIES = 100


# ============================================================
# EVALUATION-ONLY GROUND TRUTH
# ============================================================
#
# These values reproduce the hidden policy implemented by
# the simulated buyer laboratory.
#
# They are NEVER supplied to either inference architecture.
# They are used only after policy discovery to calculate
# benchmark error.
# ============================================================

GROUND_TRUTH_POLICY = {

    "annual_price": 105000,

    "contract_months": 36,

    "service_availability": 98.0,

    "payment_days": 30,

    "supplier_reliability": 85.0

}


# ============================================================
# COMMON SEARCH SPACE
# ============================================================

SEARCH_SPACE = {

    "annual_price": {
        "lower": 50000,
        "upper": 150000
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


# ============================================================
# COMMON REFERENCE PROPOSAL
# ============================================================

REFERENCE_PROPOSAL = CommercialProposal(

    annual_price=100000,

    contract_months=24,

    service_availability=99.0,

    payment_days=30,

    supplier_reliability=90.0

)


# ============================================================
# EXPERIMENT HEADER
# ============================================================

print("\n" + "=" * 75)

print("MARS — EXPERIMENT 014")

print("COMPARATIVE BLACK-BOX POLICY DISCOVERY BENCHMARK")

print("=" * 75)


print(
    "\nBenchmark Objective:"
)

print(
    "Compare fixed policy inference with autonomous "
    "next-best commercial experiment selection."
)


# ============================================================
# VERIFY COMMON REFERENCE PROPOSAL
# ============================================================

verification_buyer = AutonomousBuyerAgent()

verification_result = (
    verification_buyer.evaluate_proposal(
        REFERENCE_PROPOSAL
    )
)


print("\nREFERENCE PROPOSAL VERIFICATION")

print(
    "Buyer Decision:",
    verification_result["decision"]
)


if verification_result["decision"] != "ACCEPTED":

    raise ValueError(

        "Benchmark reference proposal must be accepted."

    )


# ============================================================
# METHOD A
# EXPERIMENT 003 — FIXED MULTI-DIMENSIONAL INFERENCE
# ============================================================

print("\n" + "=" * 75)

print("METHOD A")

print("FIXED MULTI-DIMENSIONAL POLICY INFERENCE")

print("=" * 75)


fixed_buyer = AutonomousBuyerAgent()


fixed_engine = MultiDimensionalInferenceEngine(

    buyer=fixed_buyer

)


fixed_policy = (
    fixed_engine.discover_all_policies()
)


fixed_query_count = (
    fixed_engine.query_count
)


print(
    "\nMETHOD A COMPLETE"
)

print(
    "Buyer Queries:",
    fixed_query_count
)


# ============================================================
# METHOD B
# EXPERIMENT 013 — AUTONOMOUS EXPERIMENT SELECTION
# ============================================================

print("\n" + "=" * 75)

print("METHOD B")

print("AUTONOMOUS NEXT-BEST EXPERIMENT SELECTION")

print("=" * 75)


autonomous_buyer = AutonomousBuyerAgent()


autonomous_engine = (
    AutonomousExperimentSelector(

        buyer=autonomous_buyer,

        reference_proposal=REFERENCE_PROPOSAL

    )
)


autonomous_results = (
    autonomous_engine.discover_policy(

        maximum_queries=(
            MAXIMUM_AUTONOMOUS_QUERIES
        )

    )
)


autonomous_policy = (
    autonomous_results[
        "discovered_policy"
    ]
)


autonomous_beliefs = (
    autonomous_results[
        "policy_beliefs"
    ]
)


autonomous_query_count = (
    autonomous_results[
        "total_queries"
    ]
)


print(
    "\nMETHOD B COMPLETE"
)

print(
    "Buyer Queries:",
    autonomous_query_count
)


# ============================================================
# INITIALISE BENCHMARK
# ============================================================

benchmark = PolicyDiscoveryBenchmark(

    ground_truth=GROUND_TRUTH_POLICY,

    search_space=SEARCH_SPACE

)


# ============================================================
# EVALUATE METHOD A
# ============================================================

fixed_benchmark = (
    benchmark.evaluate_method(

        method_name=(
            "Fixed Multi-Dimensional Inference"
        ),

        discovered_policy=fixed_policy,

        query_count=fixed_query_count

    )
)


# ============================================================
# EVALUATE METHOD B
# ============================================================

autonomous_benchmark = (
    benchmark.evaluate_method(

        method_name=(
            "Autonomous Experiment Selection"
        ),

        discovered_policy=autonomous_policy,

        query_count=autonomous_query_count,

        belief_state=autonomous_beliefs

    )
)


# ============================================================
# PRINT INDIVIDUAL BENCHMARK REPORTS
# ============================================================

benchmark.print_method_report(

    "Fixed Multi-Dimensional Inference"

)


benchmark.print_method_report(

    "Autonomous Experiment Selection"

)


# ============================================================
# DIRECT COMPARISON
# ============================================================

comparison = benchmark.compare_methods(

    method_a=(
        "Fixed Multi-Dimensional Inference"
    ),

    method_b=(
        "Autonomous Experiment Selection"
    )

)


# ============================================================
# QUERY EFFICIENCY
# ============================================================

query_difference = (
    autonomous_query_count
    -
    fixed_query_count
)


if fixed_query_count > 0:

    query_change_percentage = (

        query_difference
        /
        fixed_query_count
        *
        100

    )

else:

    query_change_percentage = None


# ============================================================
# FINAL COMPARATIVE RESULTS
# ============================================================

print("\n" + "=" * 75)

print("MARS — EXPERIMENT 014 RESULTS")

print("=" * 75)


print("\nQUERY EFFICIENCY")

print("-" * 75)


print(
    "Fixed Inference Queries:",
    fixed_query_count
)


print(
    "Autonomous Selection Queries:",
    autonomous_query_count
)


print(
    "Query Difference:",
    query_difference
)


if query_change_percentage is not None:

    print(
        "Query Change:",
        f"{query_change_percentage:.2f}%"
    )


# ============================================================
# POLICY COVERAGE
# ============================================================

print("\nPOLICY DISCOVERY COVERAGE")

print("-" * 75)


print(
    "Fixed Inference:",
    f"{fixed_benchmark['coverage'] * 100:.2f}%"
)


print(
    "Autonomous Selection:",
    f"{autonomous_benchmark['coverage'] * 100:.2f}%"
)


# ============================================================
# POLICY ACCURACY
# ============================================================

print("\nPOLICY DISCOVERY ACCURACY")

print("-" * 75)


print(
    "Fixed Mean Absolute Error:",
    fixed_benchmark[
        "mean_absolute_error"
    ]
)


print(
    "Autonomous Mean Absolute Error:",
    autonomous_benchmark[
        "mean_absolute_error"
    ]
)


print(
    "Fixed Mean Normalised Error:",
    fixed_benchmark[
        "mean_normalised_error"
    ]
)


print(
    "Autonomous Mean Normalised Error:",
    autonomous_benchmark[
        "mean_normalised_error"
    ]
)


# ============================================================
# RESIDUAL UNCERTAINTY
# ============================================================

print("\nRESIDUAL POLICY UNCERTAINTY")

print("-" * 75)


print(
    "Fixed Mean Residual Uncertainty:",
    fixed_benchmark[
        "mean_residual_uncertainty"
    ]
)


print(
    "Autonomous Mean Residual Uncertainty:",
    autonomous_benchmark[
        "mean_residual_uncertainty"
    ]
)


# ============================================================
# QUERY COST PER POLICY
# ============================================================

print("\nQUERY COST PER DISCOVERED POLICY")

print("-" * 75)


print(
    "Fixed Inference:",
    fixed_benchmark[
        "queries_per_discovered_policy"
    ]
)


print(
    "Autonomous Selection:",
    autonomous_benchmark[
        "queries_per_discovered_policy"
    ]
)


# ============================================================
# VARIABLE-LEVEL COMPARISON
# ============================================================

print("\nVARIABLE-LEVEL COMPARISON")

print("-" * 75)


for variable in GROUND_TRUTH_POLICY:

    fixed_data = (
        fixed_benchmark[
            "variables"
        ][variable]
    )


    autonomous_data = (
        autonomous_benchmark[
            "variables"
        ][variable]
    )


    print(
        f"\n{variable}"
    )


    print(
        "  Ground Truth:",
        GROUND_TRUTH_POLICY[
            variable
        ]
    )


    print(
        "  Fixed Estimate:",
        fixed_data[
            "estimated_threshold"
        ]
    )


    print(
        "  Autonomous Estimate:",
        autonomous_data[
            "estimated_threshold"
        ]
    )


    print(
        "  Fixed Absolute Error:",
        fixed_data[
            "absolute_error"
        ]
    )


    print(
        "  Autonomous Absolute Error:",
        autonomous_data[
            "absolute_error"
        ]
    )


# ============================================================
# MACHINE-READABLE COMPARISON SUMMARY
# ============================================================

print("\nCOMPARISON SUMMARY")

print("-" * 75)


print(
    "Query Difference:",
    comparison[
        "query_difference"
    ]
)


print(
    "Coverage Difference:",
    comparison[
        "coverage_difference"
    ]
)


print(
    "Normalised Error Difference:",
    comparison[
        "normalised_error_difference"
    ]
)


# ============================================================
# EXPERIMENT COMPLETION
# ============================================================

print("\n" + "=" * 75)

print("EXPERIMENT 014 COMPLETED")

print("=" * 75)
