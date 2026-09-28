"""
MARS — Machine-Agent Revenue Science

Experiment 020

Statistical Robustness Benchmark

Author: Kamran Khan

Purpose:
Evaluate black-box buyer-policy discovery
architectures across multiple stochastic buyer
environments, random seeds, and decision-noise
levels.

Architectures:

A. Single-Observation Discovery
B. Fixed Repeated-Evidence Discovery
C. Adaptive Sequential-Evidence Discovery

Research Objective:
Determine whether performance observed in individual
stochastic experiments generalises across repeated
randomised simulations.

Ground-truth buyer policies are used only after
discovery for evaluation.
"""

import contextlib
import io
import math
import statistics

from buyer_lab.buyer_agent import (
    CommercialProposal
)

from buyer_lab.probabilistic_buyer_agent import (
    ProbabilisticBuyerFactory
)

from inference.autonomous_experiment_selector import (
    AutonomousExperimentSelector
)

from inference.repeated_evidence_engine import (
    RepeatedEvidencePolicyDiscoveryEngine
)

from inference.adaptive_sequential_evidence_engine import (
    AdaptiveSequentialEvidenceEngine
)


# ============================================================
# COMMERCIAL VARIABLES
# ============================================================

COMMERCIAL_VARIABLES = [

    "annual_price",

    "contract_months",

    "service_availability",

    "payment_days",

    "supplier_reliability"

]


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
# NORMALISED ERROR
# ============================================================

def calculate_normalised_error(
    variable,
    estimated,
    actual
):

    if estimated is None:

        return None


    search_range = (

        SEARCH_SPACE[variable]["upper"]
        -
        SEARCH_SPACE[variable]["lower"]

    )


    if search_range <= 0:

        return 0.0


    return (

        abs(
            estimated - actual
        )
        /
        search_range

    )


# ============================================================
# POLICY ERROR
# ============================================================

def calculate_policy_error(
    discovered_policy,
    ground_truth
):

    errors = []


    for variable in COMMERCIAL_VARIABLES:

        estimated = (
            discovered_policy.get(
                variable
            )
        )


        if estimated is None:

            continue


        actual = ground_truth[
            variable
        ]


        error = (
            calculate_normalised_error(

                variable,

                estimated,

                actual

            )
        )


        errors.append(
            error
        )


    coverage = (

        len(errors)
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
# SINGLE-OBSERVATION RUN
# ============================================================

def run_single_observation(
    seed,
    noise_strength,
    boundary_width
):

    buyer = (
        ProbabilisticBuyerFactory
        .create_buyer(

            random_seed=seed,

            noise_strength=noise_strength,

            boundary_width=boundary_width

        )
    )


    engine = (
        AutonomousExperimentSelector(

            buyer=buyer,

            reference_proposal=(
                REFERENCE_PROPOSAL
            )

        )
    )


    try:

        results = run_quietly(

            lambda:
                engine.discover_policy(
                    maximum_queries=150
                )

        )


        return {

            "status":
                "SUCCESS",

            "policy":
                results[
                    "discovered_policy"
                ],

            "queries":
                results[
                    "total_queries"
                ],

            "diagnostics":
                buyer.get_diagnostics()

        }


    except Exception as error:

        return {

            "status":
                "FAILED",

            "policy":
                {},

            "queries":
                getattr(
                    engine,
                    "query_count",
                    0
                ),

            "diagnostics":
                buyer.get_diagnostics(),

            "error":
                (
                    f"{type(error).__name__}: "
                    f"{str(error)}"
                )

        }


# ============================================================
# FIXED REPEATED-EVIDENCE RUN
# ============================================================

def run_fixed_repeated(
    seed,
    noise_strength,
    boundary_width
):

    buyer = (
        ProbabilisticBuyerFactory
        .create_buyer(

            random_seed=seed,

            noise_strength=noise_strength,

            boundary_width=boundary_width

        )
    )


    engine = (
        RepeatedEvidencePolicyDiscoveryEngine(

            buyer=buyer,

            reference_proposal=(
                REFERENCE_PROPOSAL
            ),

            repetitions_per_candidate=7,

            acceptance_threshold=0.50,

            confidence_margin=0.20

        )
    )


    try:

        results = run_quietly(

            engine.discover_policy

        )


        return {

            "status":
                "SUCCESS",

            "policy":
                results[
                    "discovered_policy"
                ],

            "queries":
                results[
                    "total_queries"
                ],

            "diagnostics":
                buyer.get_diagnostics()

        }


    except Exception as error:

        return {

            "status":
                "FAILED",

            "policy":
                {},

            "queries":
                getattr(
                    engine,
                    "query_count",
                    0
                ),

            "diagnostics":
                buyer.get_diagnostics(),

            "error":
                (
                    f"{type(error).__name__}: "
                    f"{str(error)}"
                )

        }


# ============================================================
# ADAPTIVE SEQUENTIAL RUN
# ============================================================

def run_adaptive(
    seed,
    noise_strength,
    boundary_width
):

    buyer = (
        ProbabilisticBuyerFactory
        .create_buyer(

            random_seed=seed,

            noise_strength=noise_strength,

            boundary_width=boundary_width

        )
    )


    engine = (
        AdaptiveSequentialEvidenceEngine(

            buyer=buyer,

            reference_proposal=(
                REFERENCE_PROPOSAL
            ),

            minimum_observations=3,

            maximum_observations=9,

            confidence_level=0.90,

            acceptance_threshold=0.50

        )
    )


    try:

        results = run_quietly(

            engine.discover_policy

        )


        return {

            "status":
                "SUCCESS",

            "policy":
                results[
                    "discovered_policy"
                ],

            "queries":
                results[
                    "total_queries"
                ],

            "early_stop_rate":
                results[
                    "early_stop_rate"
                ],

            "average_observations":
                results[
                    "average_observations_per_candidate"
                ],

            "diagnostics":
                buyer.get_diagnostics()

        }


    except Exception as error:

        return {

            "status":
                "FAILED",

            "policy":
                {},

            "queries":
                getattr(
                    engine,
                    "query_count",
                    0
                ),

            "early_stop_rate":
                None,

            "average_observations":
                None,

            "diagnostics":
                buyer.get_diagnostics(),

            "error":
                (
                    f"{type(error).__name__}: "
                    f"{str(error)}"
                )

        }


# ============================================================
# BENCHMARK
# ============================================================

class StatisticalRobustnessBenchmark:

    def __init__(
        self,
        seeds,
        noise_levels,
        boundary_width=0.05
    ):

        self.seeds = seeds

        self.noise_levels = (
            noise_levels
        )

        self.boundary_width = (
            boundary_width
        )

        self.ground_truth = (
            ProbabilisticBuyerFactory
            .ground_truth()
        )

        self.records = []


    # ========================================================
    # RECORD ONE RUN
    # ========================================================

    def _record_result(
        self,
        method,
        seed,
        noise_strength,
        result
    ):

        evaluation = (
            calculate_policy_error(

                result[
                    "policy"
                ],

                self.ground_truth

            )
        )


        diagnostics = (
            result[
                "diagnostics"
            ]
        )


        record = {

            "method":
                method,

            "seed":
                seed,

            "noise_strength":
                noise_strength,

            "status":
                result[
                    "status"
                ],

            "queries":
                result[
                    "queries"
                ],

            "coverage":
                evaluation[
                    "coverage"
                ],

            "mean_error":
                evaluation[
                    "mean_error"
                ],

            "noise_events":
                diagnostics[
                    "noise_events"
                ],

            "realised_noise_rate":
                diagnostics[
                    "realised_noise_rate"
                ],

            "early_stop_rate":
                result.get(
                    "early_stop_rate"
                ),

            "average_observations":
                result.get(
                    "average_observations"
                ),

            "failure_reason":
                result.get(
                    "error"
                )

        }


        self.records.append(
            record
        )


    # ========================================================
    # RUN COMPLETE BENCHMARK
    # ========================================================

    def run(
        self
    ):

        total_environments = (

            len(
                self.seeds
            )
            *
            len(
                self.noise_levels
            )

        )


        total_runs = (

            total_environments
            *
            3

        )


        print("\n" + "=" * 80)

        print(
            "MARS — STATISTICAL ROBUSTNESS BENCHMARK"
        )

        print("=" * 80)


        print(
            "Random Seeds:",
            len(
                self.seeds
            )
        )


        print(
            "Noise Levels:",
            len(
                self.noise_levels
            )
        )


        print(
            "Stochastic Environments:",
            total_environments
        )


        print(
            "Discovery Architectures:",
            3
        )


        print(
            "Total Discovery Runs:",
            total_runs
        )


        completed = 0


        for noise_strength in (
            self.noise_levels
        ):

            print("\n" + "-" * 80)

            print(
                "NOISE LEVEL:",
                noise_strength
            )

            print("-" * 80)


            for seed in self.seeds:

                # --------------------------------------------
                # SINGLE OBSERVATION
                # --------------------------------------------

                single_result = (
                    run_single_observation(

                        seed,

                        noise_strength,

                        self.boundary_width

                    )
                )


                self._record_result(

                    "single",

                    seed,

                    noise_strength,

                    single_result

                )


                completed += 1


                # --------------------------------------------
                # FIXED REPEATED EVIDENCE
                # --------------------------------------------

                fixed_result = (
                    run_fixed_repeated(

                        seed,

                        noise_strength,

                        self.boundary_width

                    )
                )


                self._record_result(

                    "fixed_repeated",

                    seed,

                    noise_strength,

                    fixed_result

                )


                completed += 1


                # --------------------------------------------
                # ADAPTIVE SEQUENTIAL
                # --------------------------------------------

                adaptive_result = (
                    run_adaptive(

                        seed,

                        noise_strength,

                        self.boundary_width

                    )
                )


                self._record_result(

                    "adaptive",

                    seed,

                    noise_strength,

                    adaptive_result

                )


                completed += 1


            print(
                "Completed Runs:",
                f"{completed}/{total_runs}"
            )


        return self.records


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
    # SAFE MEDIAN
    # ========================================================

    @staticmethod
    def _safe_median(
        values
    ):

        values = [

            value

            for value in values

            if value is not None

        ]


        if not values:

            return None


        return statistics.median(
            values
        )


    # ========================================================
    # SAFE STANDARD DEVIATION
    # ========================================================

    @staticmethod
    def _safe_stdev(
        values
    ):

        values = [

            value

            for value in values

            if value is not None

        ]


        if len(values) < 2:

            return 0.0


        return statistics.stdev(
            values
        )


    # ========================================================
    # AGGREGATE METHOD
    # ========================================================

    def aggregate_method(
        self,
        method,
        noise_strength=None
    ):

        records = [

            record

            for record in self.records

            if (
                record[
                    "method"
                ]
                ==
                method
            )

        ]


        if (
            noise_strength
            is not None
        ):

            records = [

                record

                for record in records

                if math.isclose(

                    record[
                        "noise_strength"
                    ],

                    noise_strength

                )

            ]


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


        early_stop_rates = [

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


        average_observations = [

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


        return {

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
                    len(records)
                    -
                    len(successful)
                ),

            "success_rate":
                (
                    len(successful)
                    /
                    len(records)

                    if records

                    else 0.0
                ),

            "mean_error":
                self._safe_mean(
                    errors
                ),

            "median_error":
                self._safe_median(
                    errors
                ),

            "error_stdev":
                self._safe_stdev(
                    errors
                ),

            "mean_queries":
                self._safe_mean(
                    queries
                ),

            "query_stdev":
                self._safe_stdev(
                    queries
                ),

            "mean_coverage":
                self._safe_mean(
                    coverages
                ),

            "mean_early_stop_rate":
                self._safe_mean(
                    early_stop_rates
                ),

            "mean_observations":
                self._safe_mean(
                    average_observations
                )

        }


    # ========================================================
    # PRINT NOISE-LEVEL RESULTS
    # ========================================================

    def print_noise_level_results(
        self
    ):

        print("\n" + "=" * 80)

        print(
            "NOISE-LEVEL ROBUSTNESS RESULTS"
        )

        print("=" * 80)


        methods = [

            "single",

            "fixed_repeated",

            "adaptive"

        ]


        for noise_strength in (
            self.noise_levels
        ):

            print("\n" + "-" * 80)

            print(
                "NOISE STRENGTH:",
                noise_strength
            )

            print("-" * 80)


            for method in methods:

                result = (
                    self.aggregate_method(

                        method,

                        noise_strength

                    )
                )


                print(
                    f"{method:18} | "
                    f"Success: "
                    f"{result['success_rate'] * 100:6.2f}% | "
                    f"Coverage: "
                    f"{(result['mean_coverage'] or 0) * 100:6.2f}% | "
                    f"Mean Error: "
                    f"{result['mean_error']} | "
                    f"Mean Queries: "
                    f"{result['mean_queries']}"
                )


    # ========================================================
    # PRINT GLOBAL RESULTS
    # ========================================================

    def print_global_results(
        self
    ):

        print("\n" + "=" * 80)

        print(
            "GLOBAL STATISTICAL RESULTS"
        )

        print("=" * 80)


        methods = [

            "single",

            "fixed_repeated",

            "adaptive"

        ]


        for method in methods:

            result = (
                self.aggregate_method(
                    method
                )
            )


            print("\n" + method.upper())

            print("-" * 60)


            print(
                "Runs:",
                result[
                    "runs"
                ]
            )


            print(
                "Successful Runs:",
                result[
                    "successful_runs"
                ]
            )


            print(
                "Failed Runs:",
                result[
                    "failed_runs"
                ]
            )


            print(
                "Success Rate:",
                f"{result['success_rate'] * 100:.2f}%"
            )


            print(
                "Mean Coverage:",
                f"{(result['mean_coverage'] or 0) * 100:.2f}%"
            )


            print(
                "Mean Normalised Error:",
                result[
                    "mean_error"
                ]
            )


            print(
                "Median Normalised Error:",
                result[
                    "median_error"
                ]
            )


            print(
                "Error Standard Deviation:",
                result[
                    "error_stdev"
                ]
            )


            print(
                "Mean Buyer Queries:",
                result[
                    "mean_queries"
                ]
            )


            print(
                "Query Standard Deviation:",
                result[
                    "query_stdev"
                ]
            )


            if (
                result[
                    "mean_early_stop_rate"
                ]
                is not None
            ):

                print(
                    "Mean Early Stop Rate:",
                    (
                        f"{result['mean_early_stop_rate'] * 100:.2f}%"
                    )
                )


            if (
                result[
                    "mean_observations"
                ]
                is not None
            ):

                print(
                    "Mean Observations "
                    "per Candidate:",
                    result[
                        "mean_observations"
                    ]
                )


    # ========================================================
    # PRINT ADAPTIVE QUERY SAVINGS
    # ========================================================

    def print_adaptive_efficiency(
        self
    ):

        fixed = (
            self.aggregate_method(
                "fixed_repeated"
            )
        )


        adaptive = (
            self.aggregate_method(
                "adaptive"
            )
        )


        print("\n" + "=" * 80)

        print(
            "ADAPTIVE QUERY-EFFICIENCY ANALYSIS"
        )

        print("=" * 80)


        fixed_queries = (
            fixed[
                "mean_queries"
            ]
        )


        adaptive_queries = (
            adaptive[
                "mean_queries"
            ]
        )


        print(
            "Fixed Mean Queries:",
            fixed_queries
        )


        print(
            "Adaptive Mean Queries:",
            adaptive_queries
        )


        if (
            fixed_queries is not None
            and
            adaptive_queries is not None
            and
            fixed_queries > 0
        ):

            saved = (

                fixed_queries
                -
                adaptive_queries

            )


            reduction = (

                saved
                /
                fixed_queries

                *
                100

            )


            print(
                "Mean Queries Saved:",
                saved
            )


            print(
                "Mean Query Reduction:",
                f"{reduction:.2f}%"
            )


        print(
            "\nFixed Mean Error:",
            fixed[
                "mean_error"
            ]
        )


        print(
            "Adaptive Mean Error:",
            adaptive[
                "mean_error"
            ]
        )
