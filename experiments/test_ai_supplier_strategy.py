"""
MARS — Machine-Agent Revenue Science

Experiment 011

Autonomous AI Supplier Strategy Experiment

Author: Kamran Khan

Purpose:
Evaluate whether an AI supplier can improve
commercial proposals using observable buyer
feedback while respecting supplier constraints.
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


print("\n" + "=" * 65)

print("MARS — EXPERIMENT 011")

print("AUTONOMOUS AI SUPPLIER STRATEGY")

print("=" * 65)


# ==================================================
# AUTONOMOUS COMMERCIAL NEGOTIATION
# ==================================================

for round_number in range(1, MAX_ROUNDS + 1):

    print(

        f"\nNEGOTIATION ROUND {round_number}"

    )

    print("-" * 65)

    current_proposal = supplier.current_proposal

    print("\nCURRENT COMMERCIAL PROPOSAL")

    print(current_proposal)

    # ----------------------------------------------
    # BUYER EVALUATES PROPOSAL
    # ----------------------------------------------

    buyer_response = buyer.evaluate_proposal(

        current_proposal

    )

    print("\nBUYER DECISION")

    print(buyer_response["decision"])

    # ----------------------------------------------
    # AGREEMENT REACHED
    # ----------------------------------------------

    if buyer_response["decision"] == "ACCEPTED":

        agreement = True

        print("\nCOMMERCIAL AGREEMENT REACHED")

        print(

            "Final Annual Price: £"

            f"{current_proposal.annual_price:,.2f}"

        )

        print(

            "Total Intervention Cost: £"

            f"{supplier.calculate_cost(current_proposal):,.2f}"

        )

        break

    # ----------------------------------------------
    # AI SUPPLIER GENERATES NEW STRATEGY
    # ----------------------------------------------

    print("\nAI SUPPLIER GENERATING STRATEGY...")

    strategy = supplier.generate_strategy(

        buyer_feedback=buyer_response

    )

    print("\nAI STRATEGY REASONING")

    print(strategy["reasoning"])

    print("\nPROPOSED COMMERCIAL STRATEGY")

    print(strategy["candidate"])

    # ----------------------------------------------
    # VALIDATE COMMERCIAL STRATEGY
    # ----------------------------------------------

    validation = strategy["validation"]

    if validation["valid"]:

        print("\nSTRATEGY APPROVED")

        print(

            "Estimated Intervention Cost: £"

            f"{validation['cost']:,.2f}"

        )

    else:

        print("\nSTRATEGY REJECTED")

        print(validation["reason"])

        print(

            "\nAI supplier will attempt "

            "another strategy."

        )


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

    "AI Strategies Generated:",

    len(supplier.strategy_history)

)

print("=" * 65)
