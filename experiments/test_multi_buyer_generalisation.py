"""
MARS — Machine-Agent Revenue Science

Experiment 017

Multi-Buyer Generalisation Benchmark

Author: Kamran Khan

Research Objective:
Evaluate whether MARS black-box policy-discovery
architectures generalise across heterogeneous
autonomous buyer configurations.

Methods evaluated:

A. Fixed Multi-Dimensional Inference
B. Uncertainty-Driven Autonomous Selection
C. Expected Information Gain Selection
D. Cost-Aware Information Selection

Evaluation dimensions:

1. Policy discovery coverage
2. Buyer-query efficiency
3. Threshold accuracy
4. Normalised threshold error
5. Generalisation across buyer archetypes
6. Generalisation failure handling
7. Modelled commercial experimentation cost

IMPORTANT:
Ground-truth policies are used only after discovery
has completed for evaluation.

The benchmark deliberately preserves the historical
Experiment 003 architecture. If its internal reference
proposal is rejected by a new buyer environment, that
failure is recorded rather than modifying the original
inference architecture.
"""

from buyer_lab.buyer_agent import (
    CommercialProposal
)

from buyer_lab.configurable_buyer_agent import (
    BuyerConfigurationFactory
)

from inference.multidimensional_inference import (
    MultiDimensionalInferenceEngine
)

from inference.autonomous_experiment_selector import (
    AutonomousExperimentSelector
)

from inference.expected_information_gain_engine import (
    ExpectedInformationGainEngine
)

from optimization.cost_aware_information_engine import (
    CostAwareInformationEngine
)


# ============================================================
# EXPERIMENT CONFIGURATION
# ============================================================

MAXIMUM_QUERIES = 150

COST_WEIGHT = 0.25

RISK_WEIGHT = 0.10


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
# SAFE REFERENCE PROPOSAL
# ============================================================
#
# This proposal lies inside the feasible region of every
# configurable buyer used in Experiment 017.
#
# It is supplied to the newer discovery architectures.
#
# Experiment 003 intentionally retains its original internal
# reference proposal so its historical architecture is not
# silently changed for this benchmark.
# ============================================================

SAFE_REFERENCE_PROPOSAL = CommercialProposal(

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
# EXTRACT EXPERIMENT 003 POLICY
# ============================================================

def extract_fixed_policy(
    results
):

    extracted = {}


    for variable, data in results.items():

        extracted[variable] = (
            data["estimated_threshold"]
        )


    return extracted


# ============================================================
# EMPTY POLICY
# ============================================================

def create_empty_policy():

    return {

        "annual_price":
            None,

        "contract_months":
            None,

        "service_availability":
            None,

        "payment_days":
            None,

        "supplier_reliability":
            None

    }


# ============================================================
# EVALUATE DISCOVERED POLICY
# ============================================================

def evaluate_policy(
    discovered_policy,
    ground_truth
):

    variable_results = {}

    discovered_count = 0

    total_normalised_error = 0.0


    for variable, actual in (
        ground_truth.items()
    ):

        estimated = (
            discovered_policy.get(
                variable
            )
        )


        error = calculate_normalised_error(

            variable,

            estimated,

            actual

        )


        if estimated is not None:

            discovered_count += 1

            total_normalised_error += error


        variable_results[variable] = {

            "actual":
                actual,

            "estimated":
                estimated,

            "normalised_error":
                error

        }


    total_variables = len(
        ground_truth
    )


    coverage = (

        discovered_count
        /
        total_variables

        if total_variables

        else 0.0

    )


    mean_normalised_error = (

        total_normalised_error
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

        "discovered_variables":
            discovered_count,

        "total_variables":
            total_variables,

        "variables":
            variable_results

    }


# ============================================================
# METHOD A
# FIXED MULTI-DIMENSIONAL INFERENCE
# ============================================================

def run_fixed_method(
    buyer
):

    engine = MultiDimensionalInferenceEngine(

        buyer=buyer

    )


    try:

        results = (
            engine.discover_all_policies()
        )


        policy = extract_fixed_policy(
            results
        )


        return {

            "policy":
                policy,

            "queries":
                engine.query_count,

            "status":
                "SUCCESS",

            "failure_reason":
                None

        }


    except ValueError as error:

        print("\n" + "!" * 80)

        print(
            "FIXED INFERENCE GENERALISATION FAILURE"
        )

        print("!" * 80)


        print(
            "Reason:",
            str(error)
        )


        print(
            "Buyer Queries Before Failure:",
            engine.query_count
        )


        print(
            "Failure recorded. "
            "Experiment 017 will continue."
        )


        return {

            "policy":
                create_empty_policy(),

            "queries":
                engine.query_count,

            "status":
                "FAILED",

            "failure_reason":
                str(error)

        }


# ============================================================
# METHOD B
# UNCERTAINTY-DRIVEN AUTONOMOUS SELECTION
# ============================================================

def run_uncertainty_method(
    buyer
):

    engine = AutonomousExperimentSelector(

        buyer=buyer,

        reference_proposal=(
            SAFE_REFERENCE_PROPOSAL
        )

    )


    try:

        results = engine.discover_policy(

            maximum_queries=MAXIMUM_QUERIES

        )


        return {

            "policy":
                results[
                    "discovered_policy"
                ],

            "queries":
                results[
                    "total_queries"
                ],

            "status":
                "SUCCESS",

            "failure_reason":
                None

        }


    except Exception as error:

        print("\n" + "!" * 80)

        print(
            "UNCERTAINTY METHOD FAILURE"
        )

        print("!" * 80)


        print(
            "Reason:",
            str(error)
        )


        return {

            "policy":
                create_empty_policy(),

            "queries":
                engine.query_count,

            "status":
                "FAILED",

            "failure_reason":
                str(error)

        }


# ============================================================
# METHOD C
# EXPECTED INFORMATION GAIN
# ============================================================

def run_information_gain_method(
    buyer
):

    engine = ExpectedInformationGainEngine(

        buyer=buyer,

        reference_proposal=(
            SAFE_REFERENCE_PROPOSAL
        )

    )


    try:

        results = engine.discover_policy(

            maximum_queries=MAXIMUM_QUERIES

        )


        return {

            "policy":
                results[
                    "discovered_policy"
                ],

            "queries":
                results[
                    "total_queries"
                ],

            "status":
                "SUCCESS",

            "failure_reason":
                None

        }


    except Exception as error:

        print("\n" + "!" * 80)

        print(
            "EXPECTED INFORMATION GAIN METHOD FAILURE"
        )

        print("!" * 80)


        print(
            "Reason:",
            str(error)
        )


        return {

            "policy":
                create_empty_policy(),

            "queries":
                engine.query_count,

            "status":
                "FAILED",

            "failure_reason":
                str(error)

        }


# ============================================================
# METHOD D
# COST-AWARE INFORMATION SELECTION
# ============================================================

def run_cost_aware_method(
    buyer
):

    engine = CostAwareInformationEngine(

        buyer=buyer,

        reference_proposal=(
            SAFE_REFERENCE_PROPOSAL
        ),

        cost_weight=COST_WEIGHT,

        risk_weight=RISK_WEIGHT

    )


    try:

        results = engine.discover_policy(

            maximum_queries=MAXIMUM_QUERIES

        )


        total_probe_cost = sum(

            record[
                "commercial_cost"
            ]

            for record in results[
                "selection_history"
            ]

        )


        average_risk = (

            sum(

                record[
                    "commercial_risk"
                ]

                for record in results[
                    "selection_history"
                ]

            )
            /
            len(
                results[
                    "selection_history"
                ]
            )

            if results[
                "selection_history"
            ]

            else 0.0

        )


        return {

            "policy":
                results[
                    "discovered_policy"
                ],

            "queries":
                results[
                    "total_queries"
                ],

            "modelled_probe_cost":
                total_probe_cost,

            "average_risk":
                average_risk,

            "status":
                "SUCCESS",

            "failure_reason":
                None

        }


    except Exception as error:

        print("\n" + "!" * 80)

        print(
            "COST-AWARE METHOD FAILURE"
        )

        print("!" * 80)


        print(
            "Reason:",
            str(error)
        )


        return {

            "policy":
                create_empty_policy(),

            "queries":
                engine.query_count,

            "modelled_probe_cost":
                0.0,

            "average_risk":
                0.0,

            "status":
                "FAILED",

            "failure_reason":
                str(error)

        }


# ============================================================
# EXPERIMENT HEADER
# ============================================================

print("\n" + "=" * 80)

print("MARS — EXPERIMENT 017")

print("MULTI-BUYER GENERALISATION BENCHMARK")

print("=" * 80)


print(
    "\nDiscovery Architectures: 4"
)

print(
    "Buyer Environments: 5"
)

print(
    "Maximum Discovery Trials: 20"
)


# ============================================================
# LOAD GROUND TRUTH
# ============================================================

ground_truth = (
    BuyerConfigurationFactory.ground_truth()
)


buyer_names = list(
    ground_truth.keys()
)


# ============================================================
# VERIFY SAFE REFERENCE
# ============================================================

print("\nVERIFYING COMMON REFERENCE PROPOSAL")

print("-" * 80)


verification_buyers = (
    BuyerConfigurationFactory.create_buyers()
)


for buyer_name, buyer in (
    verification_buyers.items()
):

    response = buyer.evaluate_proposal(

        SAFE_REFERENCE_PROPOSAL

    )


    print(

        buyer_name,

        "→",

        response["decision"]

    )


    if response["decision"] != "ACCEPTED":

        raise ValueError(

            f"Safe reference proposal rejected "
            f"by {buyer_name}."

        )


# ============================================================
# BENCHMARK STORAGE
# ============================================================

benchmark_results = {

    "fixed":
        [],

    "uncertainty":
        [],

    "expected_information_gain":
        [],

    "cost_aware":
        []

}


# ============================================================
# RUN ALL BUYER ENVIRONMENTS
# ============================================================

for buyer_name in buyer_names:

    print("\n" + "#" * 80)

    print(
        "BUYER ENVIRONMENT:",
        buyer_name.upper()
    )

    print("#" * 80)


    truth = ground_truth[
        buyer_name
    ]


    # ========================================================
    # METHOD A
    # ========================================================

    print(
        "\nMETHOD A — "
        "FIXED MULTI-DIMENSIONAL INFERENCE"
    )


    fixed_buyer = (
        BuyerConfigurationFactory
        .create_buyers()[
            buyer_name
        ]
    )


    fixed_result = run_fixed_method(

        fixed_buyer

    )


    fixed_evaluation = evaluate_policy(

        fixed_result["policy"],

        truth

    )


    fixed_record = {

        "buyer":
            buyer_name,

        "queries":
            fixed_result[
                "queries"
            ],

        "status":
            fixed_result[
                "status"
            ],

        "failure_reason":
            fixed_result[
                "failure_reason"
            ],

        **fixed_evaluation

    }


    benchmark_results[
        "fixed"
    ].append(
        fixed_record
    )


    # ========================================================
    # METHOD B
    # ========================================================

    print(
        "\nMETHOD B — "
        "UNCERTAINTY-DRIVEN SELECTION"
    )


    uncertainty_buyer = (
        BuyerConfigurationFactory
        .create_buyers()[
            buyer_name
        ]
    )


    uncertainty_result = (
        run_uncertainty_method(

            uncertainty_buyer

        )
    )


    uncertainty_evaluation = (
        evaluate_policy(

            uncertainty_result[
                "policy"
            ],

            truth

        )
    )


    uncertainty_record = {

        "buyer":
            buyer_name,

        "queries":
            uncertainty_result[
                "queries"
            ],

        "status":
            uncertainty_result[
                "status"
            ],

        "failure_reason":
            uncertainty_result[
                "failure_reason"
            ],

        **uncertainty_evaluation

    }


    benchmark_results[
        "uncertainty"
    ].append(
        uncertainty_record
    )


    # ========================================================
    # METHOD C
    # ========================================================

    print(
        "\nMETHOD C — "
        "EXPECTED INFORMATION GAIN"
    )


    ig_buyer = (
        BuyerConfigurationFactory
        .create_buyers()[
            buyer_name
        ]
    )


    ig_result = (
        run_information_gain_method(

            ig_buyer

        )
    )


    ig_evaluation = evaluate_policy(

        ig_result["policy"],

        truth

    )


    ig_record = {

        "buyer":
            buyer_name,

        "queries":
            ig_result[
                "queries"
            ],

        "status":
            ig_result[
                "status"
            ],

        "failure_reason":
            ig_result[
                "failure_reason"
            ],

        **ig_evaluation

    }


    benchmark_results[
        "expected_information_gain"
    ].append(
        ig_record
    )


    # ========================================================
    # METHOD D
    # ========================================================

    print(
        "\nMETHOD D — "
        "COST-AWARE INFORMATION"
    )


    cost_buyer = (
        BuyerConfigurationFactory
        .create_buyers()[
            buyer_name
        ]
    )


    cost_result = (
        run_cost_aware_method(

            cost_buyer

        )
    )


    cost_evaluation = evaluate_policy(

        cost_result["policy"],

        truth

    )


    cost_record = {

        "buyer":
            buyer_name,

        "queries":
            cost_result[
                "queries"
            ],

        "modelled_probe_cost":
            cost_result[
                "modelled_probe_cost"
            ],

        "average_risk":
            cost_result[
                "average_risk"
            ],

        "status":
            cost_result[
                "status"
            ],

        "failure_reason":
            cost_result[
                "failure_reason"
            ],

        **cost_evaluation

    }


    benchmark_results[
        "cost_aware"
    ].append(
        cost_record
    )


# ============================================================
# AGGREGATE METHOD RESULTS
# ============================================================

def aggregate_method(
    records
):

    buyer_count = len(
        records
    )


    successful_runs = [

        record

        for record in records

        if record["status"] == "SUCCESS"

    ]


    failed_runs = [

        record

        for record in records

        if record["status"] == "FAILED"

    ]


    total_queries = sum(

        record["queries"]

        for record in records

    )


    average_queries = (

        total_queries
        /
        buyer_count

        if buyer_count

        else 0.0

    )


    average_coverage = (

        sum(

            record["coverage"]

            for record in records

        )
        /
        buyer_count

        if buyer_count

        else 0.0

    )


    valid_errors = [

        record[
            "mean_normalised_error"
        ]

        for record in records

        if record[
            "mean_normalised_error"
        ] is not None

    ]


    average_error = (

        sum(valid_errors)
        /
        len(valid_errors)

        if valid_errors

        else None

    )


    complete_buyers = sum(

        1

        for record in records

        if record["coverage"] == 1.0

    )


    return {

        "buyer_count":
            buyer_count,

        "successful_runs":
            len(successful_runs),

        "failed_runs":
            len(failed_runs),

        "total_queries":
            total_queries,

        "average_queries":
            average_queries,

        "average_coverage":
            average_coverage,

        "average_normalised_error":
            average_error,

        "complete_buyer_discoveries":
            complete_buyers

    }


aggregates = {

    method:
        aggregate_method(records)

    for method, records in (
        benchmark_results.items()
    )

}


# ============================================================
# PER-BUYER RESULTS
# ============================================================

print("\n" + "=" * 80)

print("PER-BUYER GENERALISATION RESULTS")

print("=" * 80)


for buyer_name in buyer_names:

    print(
        f"\nBUYER: {buyer_name}"
    )

    print("-" * 80)


    for method, records in (
        benchmark_results.items()
    ):

        record = next(

            item

            for item in records

            if item["buyer"] == buyer_name

        )


        error = record[
            "mean_normalised_error"
        ]


        error_text = (

            f"{error:.8f}"

            if error is not None

            else "N/A"

        )


        print(

            f"{method:30} | "

            f"Status: "
            f"{record['status']:7} | "

            f"Queries: "
            f"{record['queries']:3} | "

            f"Coverage: "
            f"{record['coverage'] * 100:6.2f}% | "

            f"Mean Normalised Error: "
            f"{error_text}"

        )


        if record["failure_reason"]:

            print(

                "  Failure Reason:",

                record[
                    "failure_reason"
                ]

            )


# ============================================================
# AGGREGATE RESULTS
# ============================================================

print("\n" + "=" * 80)

print("MARS — EXPERIMENT 017 AGGREGATE RESULTS")

print("=" * 80)


for method, result in (
    aggregates.items()
):

    print(
        f"\nMETHOD: {method}"
    )


    print(
        "  Buyer Environments:",
        result[
            "buyer_count"
        ]
    )


    print(
        "  Successful Runs:",
        result[
            "successful_runs"
        ]
    )


    print(
        "  Failed Runs:",
        result[
            "failed_runs"
        ]
    )


    print(
        "  Total Buyer Queries:",
        result[
            "total_queries"
        ]
    )


    print(
        "  Average Queries per Buyer:",
        round(
            result[
                "average_queries"
            ],
            4
        )
    )


    print(
        "  Average Policy Coverage:",
        f"{result['average_coverage'] * 100:.2f}%"
    )


    print(
        "  Complete Buyer Discoveries:",
        (
            f"{result['complete_buyer_discoveries']}"
            f"/{result['buyer_count']}"
        )
    )


    print(
        "  Average Normalised Error:",
        result[
            "average_normalised_error"
        ]
    )


# ============================================================
# COST-AWARE ECONOMIC SUMMARY
# ============================================================

cost_records = benchmark_results[
    "cost_aware"
]


successful_cost_records = [

    record

    for record in cost_records

    if record["status"] == "SUCCESS"

]


total_modelled_cost = sum(

    record[
        "modelled_probe_cost"
    ]

    for record in successful_cost_records

)


average_modelled_cost = (

    total_modelled_cost
    /
    len(successful_cost_records)

    if successful_cost_records

    else 0.0

)


average_cost_aware_risk = (

    sum(

        record[
            "average_risk"
        ]

        for record in successful_cost_records

    )
    /
    len(successful_cost_records)

    if successful_cost_records

    else 0.0

)


print("\n" + "=" * 80)

print("COST-AWARE ECONOMIC SUMMARY")

print("=" * 80)


print(
    "Successful Cost-Aware Runs:",
    len(
        successful_cost_records
    )
)


print(
    "Total Modelled Probe Cost: £"
    f"{total_modelled_cost:,.2f}"
)


print(
    "Average Modelled Cost per "
    "Successful Buyer: £"
    f"{average_modelled_cost:,.2f}"
)


print(
    "Average Commercial Risk:",
    round(
        average_cost_aware_risk,
        6
    )
)


# ============================================================
# GENERALISATION CHECK
# ============================================================

print("\n" + "=" * 80)

print("GENERALISATION CHECK")

print("=" * 80)


for method, result in (
    aggregates.items()
):

    if (
        result["failed_runs"] == 0
        and
        result[
            "complete_buyer_discoveries"
        ]
        ==
        result[
            "buyer_count"
        ]
    ):

        status = (
            "COMPLETE ACROSS ALL BUYERS"
        )


    elif result["successful_runs"] == 0:

        status = (
            "FAILED ACROSS ALL BUYERS"
        )


    else:

        status = (
            "INCOMPLETE GENERALISATION"
        )


    print(

        method,

        "→",

        status

    )


# ============================================================
# EXPERIMENT COMPLETION
# ============================================================

print("\n" + "=" * 80)

print("EXPERIMENT 017 COMPLETED")

print("=" * 80)
