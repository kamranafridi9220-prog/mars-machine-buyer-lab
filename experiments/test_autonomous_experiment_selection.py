"""
MARS — Machine-Agent Revenue Science

Experiment 013

Autonomous Next-Best Commercial Experiment Selection

Author: Kamran Khan

Research Objective:
Investigate whether MARS can autonomously select
commercial experiments that progressively reduce
uncertainty about hidden black-box buyer policies.

The experiment-selection system does not access
the buyer's private policy variables.
"""

from buyer_lab.buyer_agent import (
    AutonomousBuyerAgent,
    CommercialProposal
)

from inference.autonomous_experiment_selector import (
    AutonomousExperimentSelector
)


# ============================================================
# EXPERIMENT CONFIGURATION
# ============================================================

MAXIMUM_QUERIES = 100


# ============================================================
# INITIALISE BLACK-BOX AUTONOMOUS BUYER
# ============================================================

buyer = AutonomousBuyerAgent()


# ============================================================
# CREATE ACCEPTED REFERENCE PROPOSAL
# ============================================================
#
# The reference proposal is intentionally configured
# to satisfy the simulated procurement environment.
#
# The experiment selector does NOT access the buyer's
# internal private policy variables.
#
# This accepted reference allows individual commercial
# dimensions to be experimentally isolated.
# ============================================================

reference_proposal = CommercialProposal(

    annual_price=100000,

    contract_months=24,

    service_availability=99.0,

    payment_days=30,

    supplier_reliability=90.0

)


# ============================================================
# VERIFY REFERENCE PROPOSAL
# ============================================================

reference_response = buyer.evaluate_proposal(

    reference_proposal

)


print("\n" + "=" * 70)

print("MARS — EXPERIMENT 013")

print("AUTONOMOUS NEXT-BEST COMMERCIAL EXPERIMENT SELECTION")

print("=" * 70)


print("\nREFERENCE PROPOSAL")

print(reference_proposal)


print("\nREFERENCE BUYER DECISION")

print(reference_response["decision"])


if reference_response["decision"] != "ACCEPTED":

    raise ValueError(

        "Reference proposal must be accepted before "
        "isolated policy discovery can begin."

    )


# ============================================================
# INITIALISE AUTONOMOUS EXPERIMENT SELECTOR
# ============================================================

selector = AutonomousExperimentSelector(

    buyer=buyer,

    reference_proposal=reference_proposal

)


# ============================================================
# RUN AUTONOMOUS POLICY DISCOVERY
# ============================================================

results = selector.discover_policy(

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
# CALCULATE RESOLUTION METRICS
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


total_information_gain = sum(

    record["information_gain"]

    for record in selection_history

)


average_information_gain = (

    total_information_gain /
    len(selection_history)

    if selection_history

    else 0

)


# ============================================================
# FINAL EXPERIMENT RESULTS
# ============================================================

print("\n" + "=" * 70)

print("MARS — EXPERIMENT 013 RESULTS")

print("=" * 70)


print(

    "\nTotal Autonomous Buyer Queries:",

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

    "Total Information Gain:",

    round(
        total_information_gain,
        6
    )

)


print(

    "Average Information Gain per Query:",

    round(
        average_information_gain,
        6
    )

)


# ============================================================
# DISCOVERED POLICY
# ============================================================

print("\nDISCOVERED BUYER POLICY")

print("-" * 70)


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

print("-" * 70)


for variable, belief in (

    policy_beliefs.items()

):

    print(

        f"\n{variable}"

    )

    print(

        "Lower Boundary:",

        belief["lower"]

    )

    print(

        "Upper Boundary:",

        belief["upper"]

    )

    print(

        "Resolved:",

        belief["resolved"]

    )

    print(

        "Estimated Threshold:",

        belief["estimated_threshold"]

    )


# ============================================================
# AUTONOMOUS SELECTION TRACE
# ============================================================

print("\nAUTONOMOUS EXPERIMENT SELECTION TRACE")

print("-" * 70)


for record in selection_history:

    print(

        f"Query {record['query']} | "

        f"{record['selected_variable']} | "

        f"Candidate: {record['candidate_value']} | "

        f"{record['buyer_decision']} | "

        f"Information Gain: "
        f"{record['information_gain']:.6f}"

    )


# ============================================================
# EXPERIMENT COMPLETION
# ============================================================

print("\n" + "=" * 70)

print("EXPERIMENT 013 COMPLETED")

print("=" * 70)
