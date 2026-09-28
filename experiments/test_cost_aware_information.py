"""
MARS — Machine-Agent Revenue Science

Experiment 016

Cost-Aware Information Gain Policy Discovery

Author: Kamran Khan

Research Objective:
Investigate whether MARS can discover hidden autonomous
buyer procurement policies while jointly considering:

1. Information value
2. Commercial experimentation cost
3. Commercial risk
4. Policy uncertainty

The buyer's private procurement-policy variables are
never accessed by the discovery engine.
"""

from buyer_lab.buyer_agent import (
    AutonomousBuyerAgent,
    CommercialProposal
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
# INITIALISE BLACK-BOX BUYER
# ============================================================

buyer = AutonomousBuyerAgent()


# ============================================================
# REFERENCE COMMERCIAL PROPOSAL
# ============================================================

reference_proposal = CommercialProposal(

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

print("MARS — EXPERIMENT 016")

print("COST-AWARE INFORMATION GAIN POLICY DISCOVERY")

print("=" * 75)


print(
    "\nCost Weight:",
    COST_WEIGHT
)

print(
    "Risk Weight:",
    RISK_WEIGHT
)


# ============================================================
# VERIFY REFERENCE PROPOSAL
# ============================================================

reference_response = (
    buyer.evaluate_proposal(
        reference_proposal
    )
)


print("\nREFERENCE BUYER DECISION")

print(
    reference_response["decision"]
)


if reference_response["decision"] != "ACCEPTED":

    raise ValueError(

        "Reference proposal must be accepted before "
        "cost-aware policy discovery can begin."

    )


# ============================================================
# INITIALISE COST-AWARE ENGINE
# ============================================================

engine = CostAwareInformationEngine(

    buyer=buyer,

    reference_proposal=reference_proposal,

    cost_weight=COST_WEIGHT,

    risk_weight=RISK_WEIGHT

)


# ============================================================
# RUN POLICY DISCOVERY
# ============================================================

results = engine.discover_policy(

    maximum_queries=MAXIMUM_QUERIES

)


# ============================================================
# EXTRACT RESULTS
# ============================================================

discovered_policy = results[
    "discovered_policy"
]

policy_beliefs = results[
    "policy_beliefs"
]

selection_history = results[
    "selection_history"
]


# ============================================================
# POLICY RESOLUTION
# ============================================================

resolved_variables = [

    variable

    for variable, threshold
    in discovered_policy.items()

    if threshold is not None

]


unresolved_variables = [

    variable

    for variable, threshold
    in discovered_policy.items()

    if threshold is None

]


total_variables = len(
    discovered_policy
)


coverage = (

    len(resolved_variables)
    /
    total_variables

    if total_variables

    else 0

)


# ============================================================
# COMMERCIAL EXPERIMENTATION METRICS
# ============================================================

total_probe_cost = sum(

    record[
        "commercial_cost"
    ]

    for record in selection_history

)


average_probe_cost = (

    total_probe_cost
    /
    len(selection_history)

    if selection_history

    else 0

)


maximum_probe_cost = max(

    (
        record[
            "commercial_cost"
        ]

        for record in selection_history
    ),

    default=0

)


total_commercial_risk = sum(

    record[
        "commercial_risk"
    ]

    for record in selection_history

)


average_commercial_risk = (

    total_commercial_risk
    /
    len(selection_history)

    if selection_history

    else 0

)


# ============================================================
# INFORMATION METRICS
# ============================================================

total_information_value = sum(

    record[
        "information_value"
    ]

    for record in selection_history

)


average_information_value = (

    total_information_value
    /
    len(selection_history)

    if selection_history

    else 0

)


total_utility = sum(

    record[
        "utility_score"
    ]

    for record in selection_history

)


average_utility = (

    total_utility
    /
    len(selection_history)

    if selection_history

    else 0

)


total_uncertainty_reduction = sum(

    record[
        "realised_uncertainty_reduction"
    ]

    for record in selection_history

)


# ============================================================
# QUERY EFFICIENCY
# ============================================================

queries_per_discovered_policy = (

    results["total_queries"]
    /
    len(resolved_variables)

    if resolved_variables

    else None

)


# ============================================================
# FINAL RESULTS
# ============================================================

print("\n" + "=" * 75)

print("MARS — EXPERIMENT 016 RESULTS")

print("=" * 75)


print(
    "\nTotal Buyer Queries:",
    results["total_queries"]
)


print(
    "Resolved Commercial Variables:",
    len(resolved_variables)
)


print(
    "Unresolved Commercial Variables:",
    len(unresolved_variables)
)


print(
    "Policy Discovery Coverage:",
    f"{coverage * 100:.2f}%"
)


if queries_per_discovered_policy is not None:

    print(
        "Queries per Discovered Policy:",
        round(
            queries_per_discovered_policy,
            4
        )
    )


# ============================================================
# ECONOMIC RESULTS
# ============================================================

print("\nCOMMERCIAL EXPERIMENTATION COST")

print("-" * 75)


print(
    "Total Modelled Probe Cost: £"
    f"{total_probe_cost:,.2f}"
)


print(
    "Average Modelled Probe Cost: £"
    f"{average_probe_cost:,.2f}"
)


print(
    "Maximum Single Probe Cost: £"
    f"{maximum_probe_cost:,.2f}"
)


print(
    "Average Commercial Risk:",
    round(
        average_commercial_risk,
        6
    )
)


# ============================================================
# INFORMATION RESULTS
# ============================================================

print("\nINFORMATION VALUE")

print("-" * 75)


print(
    "Total Information Value:",
    round(
        total_information_value,
        6
    )
)


print(
    "Average Information Value:",
    round(
        average_information_value,
        6
    )
)


print(
    "Total Cost-Aware Utility:",
    round(
        total_utility,
        6
    )
)


print(
    "Average Cost-Aware Utility:",
    round(
        average_utility,
        6
    )
)


print(
    "Total Realised Uncertainty Reduction:",
    round(
        total_uncertainty_reduction,
        6
    )
)


# ============================================================
# DISCOVERED BUYER POLICY
# ============================================================

print("\nDISCOVERED BUYER POLICY")

print("-" * 75)


for variable, threshold in (

    discovered_policy.items()

):

    print(
        f"{variable}: {threshold}"
    )


# ============================================================
# FINAL BELIEF INTERVALS
# ============================================================

print("\nFINAL POLICY BELIEF INTERVALS")

print("-" * 75)


for variable, belief in (

    policy_beliefs.items()

):

    interval_width = (

        belief["upper"]
        -
        belief["lower"]

    )


    print(
        f"\n{variable}"
    )


    print(
        "  Lower Boundary:",
        belief["lower"]
    )


    print(
        "  Upper Boundary:",
        belief["upper"]
    )


    print(
        "  Interval Width:",
        interval_width
    )


    print(
        "  Resolved:",
        belief["resolved"]
    )


    print(
        "  Estimated Threshold:",
        belief[
            "estimated_threshold"
        ]
    )


# ============================================================
# COST-AWARE SELECTION TRACE
# ============================================================

print("\nCOST-AWARE EXPERIMENT SELECTION TRACE")

print("-" * 75)


for record in selection_history:

    print(

        f"Query {record['query']} | "

        f"{record['selected_variable']} | "

        f"Candidate: "
        f"{record['candidate_value']} | "

        f"Info: "
        f"{record['information_value']:.6f} | "

        f"Cost: "
        f"£{record['commercial_cost']:,.2f} | "

        f"Risk: "
        f"{record['commercial_risk']:.6f} | "

        f"Utility: "
        f"{record['utility_score']:.6f} | "

        f"{record['buyer_decision']}"

    )


# ============================================================
# VARIABLE EXPERIMENT COUNTS
# ============================================================

print("\nEXPERIMENT DISTRIBUTION")

print("-" * 75)


for variable in discovered_policy:

    variable_queries = sum(

        1

        for record in selection_history

        if record[
            "selected_variable"
        ] == variable

    )


    print(
        f"{variable}: "
        f"{variable_queries} queries"
    )


# ============================================================
# SANITY CHECK
# ============================================================

print("\nEXPERIMENT SANITY CHECK")

print("-" * 75)


if len(resolved_variables) == total_variables:

    print(
        "All commercial policy dimensions resolved."
    )

else:

    print(
        "WARNING:",
        len(unresolved_variables),
        "commercial policy dimensions remain unresolved."
    )


    print(
        "Unresolved Variables:",
        unresolved_variables
    )


# ============================================================
# EXPERIMENT COMPLETION
# ============================================================

print("\n" + "=" * 75)

print("EXPERIMENT 016 COMPLETED")

print("=" * 75)
