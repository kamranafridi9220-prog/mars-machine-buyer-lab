"""
MARS — Machine-Agent Revenue Science

Experiment 020

Multi-Seed Statistical Robustness Benchmark

Author: Kamran Khan

Purpose:
Run repeated stochastic evaluations of MARS buyer-policy
discovery architectures across multiple random seeds and
buyer decision-noise levels.

Architectures evaluated:

1. Single-Observation Discovery
2. Fixed Repeated-Evidence Discovery
3. Adaptive Sequential-Evidence Discovery

Experimental Design:

20 random seeds
x
6 buyer noise levels
x
3 discovery architectures

=
360 total discovery runs

The experiment evaluates:

- policy-discovery accuracy
- policy-discovery coverage
- run success/failure
- buyer-query consumption
- error variance
- robustness across noise regimes
- adaptive early stopping
- adaptive query efficiency

Ground truth is used only for post-discovery evaluation.
"""

from evaluation.statistical_robustness_benchmark import (
    StatisticalRobustnessBenchmark
)


# ============================================================
# EXPERIMENT CONFIGURATION
# ============================================================

RANDOM_SEEDS = list(
    range(
        1,
        21
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


# ============================================================
# EXPERIMENT HEADER
# ============================================================

print("\n" + "=" * 80)

print(
    "MARS — EXPERIMENT 020"
)

print(
    "MULTI-SEED STATISTICAL ROBUSTNESS BENCHMARK"
)

print("=" * 80)


print(
    "\nRandom Seeds:",
    len(
        RANDOM_SEEDS
    )
)


print(
    "Noise Levels:",
    len(
        NOISE_LEVELS
    )
)


print(
    "Discovery Architectures:",
    3
)


TOTAL_ENVIRONMENTS = (

    len(
        RANDOM_SEEDS
    )
    *
    len(
        NOISE_LEVELS
    )

)


TOTAL_RUNS = (

    TOTAL_ENVIRONMENTS
    *
    3

)


print(
    "Stochastic Buyer Environments:",
    TOTAL_ENVIRONMENTS
)


print(
    "Total Discovery Runs:",
    TOTAL_RUNS
)


print(
    "Boundary Width:",
    BOUNDARY_WIDTH
)


print(
    "\nNoise Regimes:"
)


for noise in NOISE_LEVELS:

    print(
        f"  {noise:.2f}"
    )


# ============================================================
# INITIALISE BENCHMARK
# ============================================================

benchmark = (
    StatisticalRobustnessBenchmark(

        seeds=RANDOM_SEEDS,

        noise_levels=NOISE_LEVELS,

        boundary_width=BOUNDARY_WIDTH

    )
)


# ============================================================
# RUN BENCHMARK
# ============================================================

print("\n" + "=" * 80)

print(
    "STARTING STATISTICAL BENCHMARK"
)

print("=" * 80)


records = (
    benchmark.run()
)


# ============================================================
# NOISE-LEVEL RESULTS
# ============================================================

benchmark.print_noise_level_results()


# ============================================================
# GLOBAL RESULTS
# ============================================================

benchmark.print_global_results()


# ============================================================
# ADAPTIVE EFFICIENCY
# ============================================================

benchmark.print_adaptive_efficiency()


# ============================================================
# FAILURE ANALYSIS
# ============================================================

print("\n" + "=" * 80)

print(
    "FAILURE ANALYSIS"
)

print("=" * 80)


methods = [

    "single",

    "fixed_repeated",

    "adaptive"

]


for method in methods:

    method_records = [

        record

        for record in records

        if (
            record[
                "method"
            ]
            ==
            method
        )

    ]


    failures = [

        record

        for record in method_records

        if (
            record[
                "status"
            ]
            !=
            "SUCCESS"
        )

    ]


    print(
        f"\n{method.upper()}"
    )


    print(
        "Total Runs:",
        len(
            method_records
        )
    )


    print(
        "Failures:",
        len(
            failures
        )
    )


    if failures:

        failure_reasons = {}


        for failure in failures:

            reason = (

                failure[
                    "failure_reason"
                ]
                or
                "Unknown failure"

            )


            failure_reasons[
                reason
            ] = (

                failure_reasons.get(
                    reason,
                    0
                )
                +
                1

            )


        print(
            "Failure Reasons:"
        )


        for reason, count in (
            failure_reasons.items()
        ):

            print(
                f"  {count}x — {reason}"
            )


# ============================================================
# NOISE DEGRADATION ANALYSIS
# ============================================================

print("\n" + "=" * 80)

print(
    "NOISE DEGRADATION ANALYSIS"
)

print("=" * 80)


for noise in NOISE_LEVELS:

    single = (
        benchmark.aggregate_method(

            "single",

            noise

        )
    )


    fixed = (
        benchmark.aggregate_method(

            "fixed_repeated",

            noise

        )
    )


    adaptive = (
        benchmark.aggregate_method(

            "adaptive",

            noise

        )
    )


    print(
        f"\nNoise Strength: {noise:.2f}"
    )


    print(
        "  Single Error:",
        single[
            "mean_error"
        ]
    )


    print(
        "  Fixed Error:",
        fixed[
            "mean_error"
        ]
    )


    print(
        "  Adaptive Error:",
        adaptive[
            "mean_error"
        ]
    )


    print(
        "  Single Queries:",
        single[
            "mean_queries"
        ]
    )


    print(
        "  Fixed Queries:",
        fixed[
            "mean_queries"
        ]
    )


    print(
        "  Adaptive Queries:",
        adaptive[
            "mean_queries"
        ]
    )


# ============================================================
# ADAPTIVE VS FIXED ANALYSIS
# ============================================================

print("\n" + "=" * 80)

print(
    "ADAPTIVE VS FIXED REPEATED EVIDENCE"
)

print("=" * 80)


fixed_global = (
    benchmark.aggregate_method(
        "fixed_repeated"
    )
)


adaptive_global = (
    benchmark.aggregate_method(
        "adaptive"
    )
)


fixed_queries = (
    fixed_global[
        "mean_queries"
    ]
)


adaptive_queries = (
    adaptive_global[
        "mean_queries"
    ]
)


fixed_error = (
    fixed_global[
        "mean_error"
    ]
)


adaptive_error = (
    adaptive_global[
        "mean_error"
    ]
)


if (
    fixed_queries is not None
    and
    adaptive_queries is not None
    and
    fixed_queries > 0
):

    query_difference = (

        fixed_queries
        -
        adaptive_queries

    )


    query_reduction = (

        query_difference
        /
        fixed_queries

        *
        100

    )


    print(
        "Fixed Mean Buyer Queries:",
        fixed_queries
    )


    print(
        "Adaptive Mean Buyer Queries:",
        adaptive_queries
    )


    print(
        "Mean Queries Saved:",
        query_difference
    )


    print(
        "Mean Query Reduction:",
        f"{query_reduction:.2f}%"
    )


print(
    "\nFixed Mean Normalised Error:",
    fixed_error
)


print(
    "Adaptive Mean Normalised Error:",
    adaptive_error
)


if (
    fixed_error is not None
    and
    adaptive_error is not None
):

    error_difference = (

        adaptive_error
        -
        fixed_error

    )


    print(
        "Adaptive Error Difference:",
        error_difference
    )


# ============================================================
# EXPERIMENTAL SCALE
# ============================================================

print("\n" + "=" * 80)

print(
    "EXPERIMENTAL SCALE"
)

print("=" * 80)


print(
    "Random Seeds Tested:",
    len(
        RANDOM_SEEDS
    )
)


print(
    "Noise Regimes Tested:",
    len(
        NOISE_LEVELS
    )
)


print(
    "Buyer Environments:",
    TOTAL_ENVIRONMENTS
)


print(
    "Architectures Evaluated:",
    3
)


print(
    "Total Discovery Runs:",
    len(
        records
    )
)


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 80)

print(
    "MARS — EXPERIMENT 020 COMPLETED"
)

print("=" * 80)
