"""
MARS — Machine-Agent Revenue Science

Experiment 019

Adaptive Sequential Evidence Acquisition
Under Buyer Decision Noise

Author: Kamran Khan

Research Objective:
Evaluate whether adaptive sequential evidence
acquisition can preserve the robustness of fixed
repeated-evidence buyer-policy discovery while
reducing the number of buyer interactions required.

Experiment 019 compares:

A. Fixed Repeated-Evidence Discovery
   - 7 observations for every candidate

B. Adaptive Sequential Evidence Discovery
   - minimum 3 observations
   - maximum 9 observations
   - early stopping when evidence becomes decisive

Both methods interact with independently instantiated
probabilistic buyers generated from the same hidden
commercial policy and stochastic configuration.

Ground truth is used only after discovery for
evaluation.
"""

from buyer_lab.buyer_agent import (
    CommercialProposal
)

from buyer_lab.probabilistic_buyer_agent import (
    ProbabilisticBuyerFactory
)

from inference.repeated_evidence_engine import (
    RepeatedEvidencePolicyDiscoveryEngine
)

from inference.adaptive_sequential_evidence_engine import (
    AdaptiveSequentialEvidenceEngine
)


# ============================================================
# EXPERIMENT CONFIGURATION
# ============================================================

RANDOM_SEED = 42

NOISE_STRENGTH = 0.15

BOUNDARY_WIDTH = 0.05

FIXED_REPETITIONS = 7

ADAPTIVE_MINIMUM_OBSERVATIONS = 3

ADAPTIVE_MAXIMUM_OBSERVATIONS = 9

ADAPTIVE_CONFIDENCE_LEVEL = 0.90

ACCEPTANCE_THRESHOLD = 0.50


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
# POLICY EVALUATION
# ============================================================

def evaluate_policy(
    discovered_policy,
    ground_truth
):

    variable_results = {}

    discovered_count = 0

    total_error = 0.0


    for variable in COMMERCIAL_VARIABLES:

        actual = ground_truth[
            variable
        ]


        estimated = (
            discovered_policy.get(
                variable
            )
        )


        error = (
            calculate_normalised_error(

                variable=variable,

                estimated=estimated,

                actual=actual

            )
        )


        if estimated is not None:

            discovered_count += 1

            total_error += error


        variable_results[
            variable
        ] = {

            "actual":
                actual,

            "estimated":
                estimated,

            "normalised_error":
                error

        }


    coverage = (

        discovered_count
        /
        len(
            COMMERCIAL_VARIABLES
        )

    )


    mean_normalised_error = (

        total_error
        /
        discovered_count

        if discovered_count

        else None

    )


    return {

        "coverage":
            coverage,

        "discovered_variables":
            discovered_count,

        "mean_normalised_error":
            mean_normalised_error,

        "variables":
            variable_results

    }


# ============================================================
# PRINT POLICY RESULTS
# ============================================================

def print_policy_results(
    title,
    evaluation
):

    print("\n" + "-" * 80)

    print(title)

    print("-" * 80)


    for variable, result in (
        evaluation["variables"].items()
    ):

        actual = result[
            "actual"
        ]

        estimated = result[
            "estimated"
        ]

        error = result[
            "normalised_error"
        ]


        error_text = (

            f"{error:.10f}"

            if error is not None

            else "N/A"

        )


        estimated_text = (

            f"{estimated:.10f}"

            if isinstance(
                estimated,
                (int, float)
            )

            else "N/A"

        )


        print(

            f"{variable:24} | "

            f"Actual: "
            f"{actual:12.6f} | "

            f"Estimated: "
            f"{estimated_text:>16} | "

            f"Norm Error: "
            f"{error_text}"

        )


    print(
        "\nCoverage:",
        f"{evaluation['coverage'] * 100:.2f}%"
    )


    print(
        "Mean Normalised Error:",
        evaluation[
            "mean_normalised_error"
        ]
    )


# ============================================================
# EXPERIMENT HEADER
# ============================================================

print("\n" + "=" * 80)

print(
    "MARS — EXPERIMENT 019"
)

print(
    "ADAPTIVE SEQUENTIAL EVIDENCE ACQUISITION"
)

print("=" * 80)


print(
    "\nBuyer Noise Strength:",
    NOISE_STRENGTH
)


print(
    "Buyer Boundary Width:",
    BOUNDARY_WIDTH
)


print(
    "Random Seed:",
    RANDOM_SEED
)


print(
    "\nFixed Evidence Observations:",
    FIXED_REPETITIONS
)


print(
    "Adaptive Minimum Observations:",
    ADAPTIVE_MINIMUM_OBSERVATIONS
)


print(
    "Adaptive Maximum Observations:",
    ADAPTIVE_MAXIMUM_OBSERVATIONS
)


print(
    "Adaptive Confidence Level:",
    ADAPTIVE_CONFIDENCE_LEVEL
)


# ============================================================
# GROUND TRUTH
# ============================================================

ground_truth = (
    ProbabilisticBuyerFactory
    .ground_truth()
)


# ============================================================
# METHOD A
# FIXED REPEATED EVIDENCE
# ============================================================

print("\n" + "=" * 80)

print(
    "METHOD A — FIXED REPEATED EVIDENCE"
)

print("=" * 80)


fixed_buyer = (
    ProbabilisticBuyerFactory
    .create_buyer(

        random_seed=RANDOM_SEED,

        noise_strength=NOISE_STRENGTH,

        boundary_width=BOUNDARY_WIDTH

    )
)


fixed_engine = (
    RepeatedEvidencePolicyDiscoveryEngine(

        buyer=fixed_buyer,

        reference_proposal=(
            REFERENCE_PROPOSAL
        ),

        repetitions_per_candidate=(
            FIXED_REPETITIONS
        ),

        acceptance_threshold=(
            ACCEPTANCE_THRESHOLD
        ),

        confidence_margin=0.20

    )
)


fixed_status = "SUCCESS"

fixed_failure_reason = None

fixed_policy = {}

fixed_queries = 0

fixed_candidate_experiments = 0


try:

    fixed_results = (
        fixed_engine.discover_policy()
    )


    fixed_policy = (
        fixed_results[
            "discovered_policy"
        ]
    )


    fixed_queries = (
        fixed_results[
            "total_queries"
        ]
    )


    fixed_candidate_experiments = (
        fixed_results[
            "candidate_experiments"
        ]
    )


except Exception as error:

    fixed_status = "FAILED"


    fixed_failure_reason = (

        f"{type(error).__name__}: "
        f"{str(error)}"

    )


    fixed_queries = getattr(

        fixed_engine,

        "query_count",

        0

    )


    fixed_candidate_experiments = getattr(

        fixed_engine,

        "candidate_count",

        0

    )


    print(
        "\nFIXED REPEATED-EVIDENCE FAILURE"
    )


    print(
        fixed_failure_reason
    )


fixed_diagnostics = (
    fixed_buyer.get_diagnostics()
)


fixed_evaluation = (
    evaluate_policy(

        fixed_policy,

        ground_truth

    )
)


# ============================================================
# METHOD B
# ADAPTIVE SEQUENTIAL EVIDENCE
# ============================================================

print("\n" + "=" * 80)

print(
    "METHOD B — ADAPTIVE SEQUENTIAL EVIDENCE"
)

print("=" * 80)


adaptive_buyer = (
    ProbabilisticBuyerFactory
    .create_buyer(

        random_seed=RANDOM_SEED,

        noise_strength=NOISE_STRENGTH,

        boundary_width=BOUNDARY_WIDTH

    )
)


adaptive_engine = (
    AdaptiveSequentialEvidenceEngine(

        buyer=adaptive_buyer,

        reference_proposal=(
            REFERENCE_PROPOSAL
        ),

        minimum_observations=(
            ADAPTIVE_MINIMUM_OBSERVATIONS
        ),

        maximum_observations=(
            ADAPTIVE_MAXIMUM_OBSERVATIONS
        ),

        confidence_level=(
            ADAPTIVE_CONFIDENCE_LEVEL
        ),

        acceptance_threshold=(
            ACCEPTANCE_THRESHOLD
        )

    )
)


adaptive_status = "SUCCESS"

adaptive_failure_reason = None

adaptive_policy = {}

adaptive_queries = 0

adaptive_candidate_experiments = 0

adaptive_average_observations = 0.0

adaptive_early_stops = 0

adaptive_maximum_samples = 0

adaptive_early_stop_rate = 0.0


try:

    adaptive_results = (
        adaptive_engine.discover_policy()
    )


    adaptive_policy = (
        adaptive_results[
            "discovered_policy"
        ]
    )


    adaptive_queries = (
        adaptive_results[
            "total_queries"
        ]
    )


    adaptive_candidate_experiments = (
        adaptive_results[
            "candidate_experiments"
        ]
    )


    adaptive_average_observations = (
        adaptive_results[
            "average_observations_per_candidate"
        ]
    )


    adaptive_early_stops = (
        adaptive_results[
            "early_stop_count"
        ]
    )


    adaptive_maximum_samples = (
        adaptive_results[
            "maximum_sample_count"
        ]
    )


    adaptive_early_stop_rate = (
        adaptive_results[
            "early_stop_rate"
        ]
    )


except Exception as error:

    adaptive_status = "FAILED"


    adaptive_failure_reason = (

        f"{type(error).__name__}: "
        f"{str(error)}"

    )


    adaptive_queries = getattr(

        adaptive_engine,

        "query_count",

        0

    )


    adaptive_candidate_experiments = getattr(

        adaptive_engine,

        "candidate_count",

        0

    )


    print(
        "\nADAPTIVE SEQUENTIAL "
        "EVIDENCE FAILURE"
    )


    print(
        adaptive_failure_reason
    )


adaptive_diagnostics = (
    adaptive_buyer.get_diagnostics()
)


adaptive_evaluation = (
    evaluate_policy(

        adaptive_policy,

        ground_truth

    )
)


# ============================================================
# POLICY DISCOVERY RESULTS
# ============================================================

print("\n" + "=" * 80)

print(
    "POLICY DISCOVERY COMPARISON"
)

print("=" * 80)


print_policy_results(

    "METHOD A — FIXED REPEATED EVIDENCE",

    fixed_evaluation

)


print_policy_results(

    "METHOD B — ADAPTIVE SEQUENTIAL EVIDENCE",

    adaptive_evaluation

)


# ============================================================
# QUERY EFFICIENCY
# ============================================================

print("\n" + "=" * 80)

print(
    "QUERY EFFICIENCY"
)

print("=" * 80)


print(
    "Fixed Status:",
    fixed_status
)


print(
    "Fixed Candidate Experiments:",
    fixed_candidate_experiments
)


print(
    "Fixed Buyer Queries:",
    fixed_queries
)


print(
    "\nAdaptive Status:",
    adaptive_status
)


print(
    "Adaptive Candidate Experiments:",
    adaptive_candidate_experiments
)


print(
    "Adaptive Buyer Queries:",
    adaptive_queries
)


print(
    "Adaptive Average Observations "
    "per Candidate:",
    round(
        adaptive_average_observations,
        4
    )
)


print(
    "Adaptive Early Stops:",
    adaptive_early_stops
)


print(
    "Adaptive Maximum-Sample Candidates:",
    adaptive_maximum_samples
)


print(
    "Adaptive Early Stop Rate:",
    f"{adaptive_early_stop_rate * 100:.2f}%"
)


# ============================================================
# QUERY SAVINGS
# ============================================================

print("\n" + "=" * 80)

print(
    "QUERY SAVINGS"
)

print("=" * 80)


query_savings = (

    fixed_queries
    -
    adaptive_queries

)


print(
    "Queries Saved:",
    query_savings
)


if fixed_queries > 0:

    query_savings_percentage = (

        query_savings
        /
        fixed_queries

        *
        100

    )


    print(
        "Query Reduction:",
        f"{query_savings_percentage:.2f}%"
    )


else:

    query_savings_percentage = None


# ============================================================
# STOCHASTIC BUYER DIAGNOSTICS
# ============================================================

print("\n" + "=" * 80)

print(
    "STOCHASTIC BUYER DIAGNOSTICS"
)

print("=" * 80)


print(
    "\nFixed Repeated-Evidence Buyer"
)


print(
    "Total Evaluations:",
    fixed_diagnostics[
        "total_evaluations"
    ]
)


print(
    "Noise Events:",
    fixed_diagnostics[
        "noise_events"
    ]
)


print(
    "Realised Noise Rate:",
    round(
        fixed_diagnostics[
            "realised_noise_rate"
        ],
        6
    )
)


print(
    "\nAdaptive Sequential Buyer"
)


print(
    "Total Evaluations:",
    adaptive_diagnostics[
        "total_evaluations"
    ]
)


print(
    "Noise Events:",
    adaptive_diagnostics[
        "noise_events"
    ]
)


print(
    "Realised Noise Rate:",
    round(
        adaptive_diagnostics[
            "realised_noise_rate"
        ],
        6
    )
)


# ============================================================
# ACCURACY COMPARISON
# ============================================================

print("\n" + "=" * 80)

print(
    "ACCURACY COMPARISON"
)

print("=" * 80)


fixed_error = (
    fixed_evaluation[
        "mean_normalised_error"
    ]
)


adaptive_error = (
    adaptive_evaluation[
        "mean_normalised_error"
    ]
)


print(
    "Fixed Coverage:",
    f"{fixed_evaluation['coverage'] * 100:.2f}%"
)


print(
    "Adaptive Coverage:",
    f"{adaptive_evaluation['coverage'] * 100:.2f}%"
)


print(
    "Fixed Mean Normalised Error:",
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

    error_change = (

        adaptive_error
        -
        fixed_error

    )


    print(
        "Adaptive Error Change:",
        error_change
    )


    if fixed_error > 0:

        relative_error_change = (

            error_change
            /
            fixed_error

            *
            100

        )


        print(
            "Relative Error Change:",
            f"{relative_error_change:.2f}%"
        )


# ============================================================
# EFFICIENCY-ROBUSTNESS TRADE-OFF
# ============================================================

print("\n" + "=" * 80)

print(
    "EFFICIENCY–ROBUSTNESS TRADE-OFF"
)

print("=" * 80)


if (
    fixed_error is not None
    and
    adaptive_error is not None
):

    if (
        adaptive_queries
        <
        fixed_queries
    ):

        print(
            "Adaptive sampling used fewer "
            "buyer queries."
        )

    elif (
        adaptive_queries
        ==
        fixed_queries
    ):

        print(
            "Adaptive and fixed sampling used "
            "the same number of buyer queries."
        )

    else:

        print(
            "Adaptive sampling used more "
            "buyer queries."
        )


    if (
        adaptive_error
        <
        fixed_error
    ):

        print(
            "Adaptive sampling produced lower "
            "policy-estimation error."
        )

    elif (
        adaptive_error
        ==
        fixed_error
    ):

        print(
            "Both methods produced equal "
            "policy-estimation error."
        )

    else:

        print(
            "Adaptive sampling produced higher "
            "policy-estimation error."
        )


# ============================================================
# METHOD FAILURE SUMMARY
# ============================================================

print("\n" + "=" * 80)

print(
    "METHOD FAILURE SUMMARY"
)

print("=" * 80)


print(
    "Fixed Repeated Evidence:",
    fixed_status
)


if fixed_failure_reason:

    print(
        "Reason:",
        fixed_failure_reason
    )


print(
    "Adaptive Sequential Evidence:",
    adaptive_status
)


if adaptive_failure_reason:

    print(
        "Reason:",
        adaptive_failure_reason
    )


# ============================================================
# FINAL EXPERIMENT RESULTS
# ============================================================

print("\n" + "=" * 80)

print(
    "MARS — EXPERIMENT 019 RESULTS"
)

print("=" * 80)


print(
    "Fixed Repeated-Evidence Queries:",
    fixed_queries
)


print(
    "Adaptive Sequential Queries:",
    adaptive_queries
)


print(
    "Queries Saved:",
    query_savings
)


if query_savings_percentage is not None:

    print(
        "Query Reduction:",
        f"{query_savings_percentage:.2f}%"
    )


print(
    "\nFixed Mean Normalised Error:",
    fixed_error
)


print(
    "Adaptive Mean Normalised Error:",
    adaptive_error
)


print(
    "\nAdaptive Early Stop Rate:",
    f"{adaptive_early_stop_rate * 100:.2f}%"
)


print(
    "Adaptive Average Observations "
    "per Candidate:",
    round(
        adaptive_average_observations,
        4
    )
)


print("\n" + "=" * 80)

print(
    "EXPERIMENT 019 COMPLETED"
)

print("=" * 80)
