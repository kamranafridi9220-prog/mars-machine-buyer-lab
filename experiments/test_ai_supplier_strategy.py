"""
MARS — Machine-Agent Revenue Science

Experiment 011

Autonomous AI Supplier Strategy Experiment
Version 2 — Adaptive Strategy Memory

Author: Kamran Khan
"""

from buyer_lab.buyer_agent import (
    AutonomousBuyerAgent,
    CommercialProposal
)

from negotiation.ai_supplier_strategy_agent import (
    AISupplierStrategyAgent
)


# ==================================================
# INITIALISE AUTONOMOUS BUYER
# ==================================================

buyer = AutonomousBuyerAgent()


# ==================================================
# INITIAL COMMERCIAL PROPOSAL
# ==================================================

initial_proposal = CommercialProposal(

    annual_price=120000,

    contract_months=48,

    service_availability=95.0,

    payment_days=15,

    supplier_reliability=80.0

)


# ==================================================
# INITIALISE AI SUPPLIER
# ==================================================

supplier = AISupplierStrategyAgent(

    original_proposal=initial_proposal,

    maximum_intervention_cost=25000,

    minimum_annual_price=100000

)


# ==================================================
# EXPERIMENT CONFIGURATION
# ==================================================

MAX_ROUNDS = 5

agreement = False

buyer_evaluations = 0

accepted_strategies = 0

rejected_strategies = 0


print("\n" + "=" * 65)

print("MARS — EXPERIMENT 011")

print("ADAPTIVE AI SUPPLIER STRATEGY")

print("=" * 65)


# ==================================================
# INITIAL BUYER EVALUATION
# ==================================================

buyer_response = buyer.evaluate_proposal(

    supplier.current_proposal

)

buyer_evaluations += 1

supplier.record_buyer_feedback(

    supplier.current_proposal,

    buyer_response

)

print("\nINITIAL BUYER DECISION")

print(buyer_response["decision"])


if buyer_response["decision"] == "ACCEPTED":

    agreement = True


# ==================================================
# AUTONOMOUS AI NEGOTIATION
# ==================================================

for round_number in range(1, MAX_ROUNDS + 1):

    if agreement:

        break

    print(

        f"\nNEGOTIATION ROUND {round_number}"

    )

    print("-" * 65)

    print("\nCURRENT PROPOSAL")

    print(supplier.current_proposal)

    # ----------------------------------------------
    # GENERATE AI STRATEGY
    # ----------------------------------------------

    print("\nAI SUPPLIER GENERATING STRATEGY...")

    strategy = supplier.generate_strategy(

        buyer_feedback=buyer_response

    )

    print("\nAI STRATEGY REASONING")

    print(strategy["reasoning"])

    print("\nPROPOSED STRATEGY")

    print(strategy["candidate"])

    # ----------------------------------------------
    # COMMERCIAL VALIDATION
    # ----------------------------------------------

    validation = strategy["validation"]

    if not validation["valid"]:

        rejected_strategies += 1

        print("\nSTRATEGY REJECTED")

        print(validation["reason"])

        continue

    accepted_strategies += 1

    print("\nSTRATEGY COMMERCIALLY APPROVED")

    print(

        "Intervention Cost: £"

        f"{validation['cost']:,.2f}"

    )

    # ----------------------------------------------
    # BUYER EVALUATES AI PROPOSAL
    # ----------------------------------------------

    buyer_response = buyer.evaluate_proposal(

        supplier.current_proposal

    )

    buyer_evaluations += 1

    supplier.record_buyer_feedback(

        supplier.current_proposal,

        buyer_response

    )

    print("\nBUYER DECISION")

    print(buyer_response["decision"])

    # ----------------------------------------------
    # AGREEMENT REACHED
    # ----------------------------------------------

    if buyer_response["decision"] == "ACCEPTED":

        agreement = True

        print("\nCOMMERCIAL AGREEMENT REACHED")

        break


# ==================================================
# FINAL EXPERIMENT RESULTS
# ==================================================

print("\n" + "=" * 65)

print("EXPERIMENT 011 RESULTS")

print("=" * 65)

print("Agreement Reached:", agreement)

print(

    "Final Commercial Proposal:",

    supplier.current_proposal

)

print(

    "Total Intervention Cost: £"

    f"{supplier.calculate_cost(supplier.current_proposal):,.2f}"

)

print(

    "Remaining Intervention Budget: £"

    f"{supplier.remaining_budget():,.2f}"

)

print(

    "AI Strategies Generated:",

    len(supplier.strategy_history)

)

print(

    "Commercially Approved Strategies:",

    accepted_strategies

)

print(

    "Commercially Rejected Strategies:",

    rejected_strategies

)

print(

    "Buyer Evaluations:",

    buyer_evaluations

)

print(

    "Buyer Feedback Records:",

    len(supplier.buyer_feedback_history)

)

print("=" * 65)
