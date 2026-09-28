"""
MARS — Machine-Agent Revenue Science

Experiment 015

Expected Information Gain Policy Discovery

Author: Kamran Khan

Research Objective:
Investigate whether an active-learning commercial
experiment selector can discover hidden autonomous
buyer procurement thresholds by selecting probes
according to expected information gain.

The discovery engine does not access the buyer's
private procurement-policy variables.
"""

from buyer_lab.buyer_agent import (
    AutonomousBuyerAgent,
    CommercialProposal
)

from inference.expected_information_gain_engine import (
    ExpectedInformationGainEngine
)


# ============================================================
# EXPERIMENT CONFIGURATION
# ============================================================

MAXIMUM_QUERIES = 100


# ============================================================
# INITIALISE BLACK-BOX BUYER
# ============================================================

buyer = AutonomousBuyerAgent()


# ============================================================
# REFERENCE COMMERCIAL PROPOSAL
# ============================================================
#
# The proposal provides an accepted baseline from which
# individual commercial dimensions can be isolated.
#
# The discovery engine itself does not inspect the buyer's
# private policy thresholds.
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

print("MARS — EXPERIMENT 015")

print("EXPECTED INFORMATION GAIN POLICY DISCOVERY")

print("=" * 75)


# ============================================================
# VERIFY REFERENCE PROPOSAL
# ============================================================

reference_response = buyer.evaluate_proposal(

    reference_proposal

)


print("\nREFERENCE PROPOSAL")

print(reference_proposal)


print("\nREFERENCE BUYER DECISION")

print(reference_response["decision"])


if reference_response["decision"] != "ACCEPTED":

    raise ValueError(

        "Reference proposal must be accepted before "
        "policy discovery can begin."

    )


# ============================================================
# INITIALISE EXPECTED INFORMATION GAIN ENGINE
# ============================================================

engine = ExpectedInformationGainEngine(

    buyer=buyer,

    reference_proposal=reference_proposal

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
# RESOLUTION METRICS
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


# ============================================================
# INFORMATION-GAIN METRICS
# ============================================================

total_expected_information_gain = sum(

    record[
        "expected_information_gain"
    ]

    for record in selection_history

)


total_realised_information_gain = sum(

    record[
        "realised_information_gain"
    ]

    for record in selection_history

)


average_expected_information_gain = (

    total_expected_information_gain
    /
    len(selection_history)

    if selection_history

    else 0

)


average_realised_information_gain = (

    total_realised_information_gain
    /
    len(selection_history)

    if selection_history

    else 0

)


# ============================================================
# POLICY COVERAGE
# ============================================================

total_variables = len(
    discovered_policy
)


policy_coverage = (

    len(resolved_variables)
    /
    total_variables

    if total_variables

    else 0

)


# ============================================================
# QUERY COST
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

print("MARS — EXPERIMENT 015 RESULTS")

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
    f"{policy_coverage * 100:.2f}%"
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
# INFORMATION-GAIN RESULTS
# ============================================================

print("\nINFORMATION GAIN")

print("-" * 75)


print(
    "Total Expected Information Gain:",
    round(
        total_expected_information_gain,
        6
    )
)


print(
    "Average Expected Information Gain:",
    round(
        average_expected_information_gain,
        6
    )
)


print(
    "Total Realised Information Gain:",
    round(
        total_realised_information_gain,
        6
    )
)


print(
    "Average Realised Information Gain:",
    round(
        average_realised_information_gain,
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
# FINAL POLICY BELIEF INTERVALS
# ============================================================

print("\nFINAL POLICY BELIEF INTERVALS")

print("-" * 75)


for variable, belief in (

    policy_beliefs.items()

):

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
        (
            belief["upper"]
            -
            belief["lower"]
        )
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
# EXPERIMENT SELECTION TRACE
# ============================================================

print("\nEXPECTED INFORMATION GAIN SELECTION TRACE")

print("-" * 75)


for record in selection_history:

    print(

        f"Query {record['query']} | "

        f"{record['selected_variable']} | "

        f"Candidate: "
        f"{record['candidate_value']} | "

        f"P(Accept): "
        f"{record['acceptance_probability']:.4f} | "

        f"Expected IG: "
        f"{record['expected_information_gain']:.6f} | "

        f"{record['buyer_decision']} | "

        f"Realised IG: "
        f"{record['realised_information_gain']:.6f}"

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
# COMPLETION
# ============================================================

print("\n" + "=" * 75)

print("EXPERIMENT 015 COMPLETED")

print("=" * 75)
