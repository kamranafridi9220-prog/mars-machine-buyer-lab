"""
MARS — Machine-Agent Revenue Science

Experiment 018

Probabilistic Buyer Policy Discovery Under Decision Noise

Author: Kamran Khan

Research Objective:
Evaluate the robustness of black-box buyer-policy
discovery when observable procurement decisions
become probabilistic near hidden policy boundaries.

Experiment 018 compares:

A. Single-observation uncertainty-driven discovery
B. Fixed repeated-evidence discovery

Both methods interact with independently instantiated
buyers generated from the same underlying hidden
commercial policy and stochastic decision model.

Ground truth is used only after discovery for
evaluation.
"""

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


# ============================================================
# EXPERIMENT CONFIGURATION
# ============================================================

RANDOM_SEED = 42

NOISE_STRENGTH = 0.15

BOUNDARY_WIDTH = 0.05

REPETITIONS_PER_CANDIDATE = 7

MAXIMUM_SINGLE_OBSERVATION_QUERIES = 150


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
# SAFE REFERENCE PROPOSAL
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

def evaluate_discovered_policy(
    discovered_policy,
    ground_truth
):

    variable_results = {}

    total_error = 0.0

    discovered_count = 0


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

                variable,

                estimated,

                actual

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
        len(COMMERCIAL_VARIABLES)

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

        "mean_normalised_error":
            mean_normalised_error,

        "variables":
            variable_results

    }


# ============================================================
# PRINT POLICY COMPARISON
# ============================================================

def print_policy_comparison(
    method_name,
    evaluation
):

    print("\n" + "-" * 80)

    print(
        method_name
    )

    print("-" * 80)


    for variable, result in (
        evaluation["variables"].items()
    ):

        estimated = result[
            "estimated"
        ]

        actual = result[
            "actual"
        ]

        error = result[
            "normalised_error"
        ]


        print(
            f"{variable:24} | "
            f"Actual: {actual:12.6f} | "
            f"Estimated: "
            f"{str(estimated):>14} | "
            f"Norm Error: "
            f"{error if error is not None else 'N/A'}"
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
    "MARS — EXPERIMENT 018"
)

print(
    "PROBABILISTIC BUYER POLICY DISCOVERY"
)

print("=" * 80)


print(
    "\nRandom Seed:",
    RANDOM_SEED
)


print(
    "Noise Strength:",
    NOISE_STRENGTH
)


print(
    "Boundary Width:",
    BOUNDARY_WIDTH
)


print(
    "Repeated Observations per Candidate:",
    REPETITIONS_PER_CANDIDATE
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
# SINGLE-OBSERVATION DISCOVERY
# ============================================================

print("\n" + "=" * 80)

print(
    "METHOD A — SINGLE-OBSERVATION DISCOVERY"
)

print("=" * 80)


single_buyer = (
    ProbabilisticBuyerFactory
    .create_buyer(

        random_seed=RANDOM_SEED,

        noise_strength=NOISE_STRENGTH,

        boundary_width=BOUNDARY_WIDTH

    )
)


single_engine = (
    AutonomousExperimentSelector(

        buyer=single_buyer,

        reference_proposal=(
            REFERENCE_PROPOSAL
        )

    )
)


single_status = "SUCCESS"

single_failure_reason = None

single_policy = {}

single_queries = 0


try:

    single_results = (
        single_engine.discover_policy(

            maximum_queries=(
                MAXIMUM_SINGLE_OBSERVATION_QUERIES
            )

        )
    )


    single_policy = (
        single_results[
            "discovered_policy"
        ]
    )


    single_queries = (
        single_results[
            "total_queries"
        ]
    )


except Exception as error:

    single_status = "FAILED"

    single_failure_reason = (

        f"{type(error).__name__}: "
        f"{str(error)}"

    )


    single_queries = getattr(

        single_engine,

        "query_count",

        0

    )


    print(
        "\nSINGLE-OBSERVATION METHOD FAILURE"
    )


    print(
        single_failure_reason
    )


single_diagnostics = (
    single_buyer.get_diagnostics()
)


single_evaluation = (
    evaluate_discovered_policy(

        single_policy,

        ground_truth

    )
)


# ============================================================
# METHOD B
# REPEATED-EVIDENCE DISCOVERY
# ============================================================

print("\n" + "=" * 80)

print(
    "METHOD B — REPEATED-EVIDENCE DISCOVERY"
)

print("=" * 80)


repeated_buyer = (
    ProbabilisticBuyerFactory
    .create_buyer(

        random_seed=RANDOM_SEED,

        noise_strength=NOISE_STRENGTH,

        boundary_width=BOUNDARY_WIDTH

    )
)


repeated_engine = (
    RepeatedEvidencePolicyDiscoveryEngine(

        buyer=repeated_buyer,

        reference_proposal=(
            REFERENCE_PROPOSAL
        ),

        repetitions_per_candidate=(
            REPETITIONS_PER_CANDIDATE
        ),

        acceptance_threshold=0.50,

        confidence_margin=0.20

    )
)


repeated_status = "SUCCESS"

repeated_failure_reason = None

repeated_policy = {}

repeated_queries = 0

candidate_experiments = 0


try:

    repeated_results = (
        repeated_engine.discover_policy()
    )


    repeated_policy = (
        repeated_results[
            "discovered_policy"
        ]
    )


    repeated_queries = (
        repeated_results[
            "total_queries"
        ]
    )


    candidate_experiments = (
        repeated_results[
            "candidate_experiments"
        ]
    )


except Exception as error:

    repeated_status = "FAILED"

    repeated_failure_reason = (

        f"{type(error).__name__}: "
        f"{str(error)}"

    )


    repeated_queries = getattr(

        repeated_engine,

        "query_count",

        0

    )


    candidate_experiments = getattr(

        repeated_engine,

        "candidate_count",

        0

    )


    print(
        "\nREPEATED-EVIDENCE METHOD FAILURE"
    )


    print(
        repeated_failure_reason
    )


repeated_diagnostics = (
    repeated_buyer.get_diagnostics()
)


repeated_evaluation = (
    evaluate_discovered_policy(

        repeated_policy,

        ground_truth

    )
)


# ============================================================
# POLICY COMPARISON
# ============================================================

print("\n" + "=" * 80)

print(
    "POLICY DISCOVERY COMPARISON"
)

print("=" * 80)


print_policy_comparison(

    "METHOD A — SINGLE OBSERVATION",

    single_evaluation

)


print_policy_comparison(

    "METHOD B — REPEATED EVIDENCE",

    repeated_evaluation

)


# ============================================================
# QUERY COMPARISON
# ============================================================

print("\n" + "=" * 80)

print(
    "QUERY EFFICIENCY"
)

print("=" * 80)


print(
    "Single-Observation Status:",
    single_status
)


print(
    "Single-Observation Queries:",
    single_queries
)


print(
    "Repeated-Evidence Status:",
    repeated_status
)


print(
    "Repeated-Evidence Candidate Experiments:",
    candidate_experiments
)


print(
    "Repeated-Evidence Buyer Queries:",
    repeated_queries
)


query_difference = (

    repeated_queries
    -
    single_queries

)


print(
    "Additional Queries Required "
    "by Repeated Evidence:",
    query_difference
)


if single_queries > 0:

    query_increase_percentage = (

        query_difference
        /
        single_queries

        *
        100

    )


    print(
        "Query Increase:",
        f"{query_increase_percentage:.2f}%"
    )


# ============================================================
# STOCHASTIC BUYER DIAGNOSTICS
# ============================================================

print("\n" + "=" * 80)

print(
    "STOCHASTIC BUYER DIAGNOSTICS"
)

print("=" * 80)


print(
    "\nSingle-Observation Buyer"
)


print(
    "Total Evaluations:",
    single_diagnostics[
        "total_evaluations"
    ]
)


print(
    "Noise Events:",
    single_diagnostics[
        "noise_events"
    ]
)


print(
    "Realised Noise Rate:",
    round(
        single_diagnostics[
            "realised_noise_rate"
        ],
        6
    )
)


print(
    "\nRepeated-Evidence Buyer"
)


print(
    "Total Evaluations:",
    repeated_diagnostics[
        "total_evaluations"
    ]
)


print(
    "Noise Events:",
    repeated_diagnostics[
        "noise_events"
    ]
)


print(
    "Realised Noise Rate:",
    round(
        repeated_diagnostics[
            "realised_noise_rate"
        ],
        6
    )
)


# ============================================================
# ROBUSTNESS COMPARISON
# ============================================================

print("\n" + "=" * 80)

print(
    "ROBUSTNESS COMPARISON"
)

print("=" * 80)


single_error = (
    single_evaluation[
        "mean_normalised_error"
    ]
)


repeated_error = (
    repeated_evaluation[
        "mean_normalised_error"
    ]
)


print(
    "Single-Observation Coverage:",
    f"{single_evaluation['coverage'] * 100:.2f}%"
)


print(
    "Repeated-Evidence Coverage:",
    f"{repeated_evaluation['coverage'] * 100:.2f}%"
)


print(
    "Single-Observation Mean "
    "Normalised Error:",
    single_error
)


print(
    "Repeated-Evidence Mean "
    "Normalised Error:",
    repeated_error
)


if (
    single_error is not None
    and
    repeated_error is not None
):

    error_difference = (

        single_error
        -
        repeated_error

    )


    print(
        "Normalised Error Reduction:",
        error_difference
    )


    if single_error > 0:

        error_reduction_percentage = (

            error_difference
            /
            single_error

            *
            100

        )


        print(
            "Relative Error Reduction:",
            f"{error_reduction_percentage:.2f}%"
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
    "Single Observation:",
    single_status
)


if single_failure_reason:

    print(
        "Reason:",
        single_failure_reason
    )


print(
    "Repeated Evidence:",
    repeated_status
)


if repeated_failure_reason:

    print(
        "Reason:",
        repeated_failure_reason
    )


# ============================================================
# EXPERIMENT COMPLETION
# ============================================================

print("\n" + "=" * 80)

print(
    "EXPERIMENT 018 COMPLETED"
)

print("=" * 80)
