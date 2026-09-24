"""
MARS — Machine-Agent Revenue Science

Experiment 005

Autonomous Buyer-Supplier Negotiation

Author: Kamran Khan
"""

from buyer_lab.buyer_agent import (

    AutonomousBuyerAgent,

    CommercialProposal

)

from negotiation.negotiation_lab import (

    BuyerNegotiationAgent,

    SupplierNegotiationAgent,

    AutonomousNegotiationEnvironment

)


# ==================================================
# INITIALISE AUTONOMOUS BUYER
# ==================================================

buyer = AutonomousBuyerAgent()


# ==================================================
# BUYER NEGOTIATION REQUIREMENTS
# ==================================================

# These requirements are held by the buyer-side
# negotiation interface, not the supplier agent.
#
# They match the controlled buyer simulator used
# in Experiments 001–004.

buyer_requirements = {

    "annual_price": 105000,

    "service_availability": 98.0,

    "supplier_reliability": 85.0,

    "contract_months": 36,

    "payment_days": 30

}


buyer_negotiator = BuyerNegotiationAgent(

    buyer,

    buyer_requirements

)


# ==================================================
# INITIAL SUPPLIER PROPOSAL
# ==================================================

original_proposal = CommercialProposal(

    annual_price=120000,

    contract_months=48,

    service_availability=95.0,

    payment_days=14,

    supplier_reliability=90.0

)


# ==================================================
# INITIALISE SUPPLIER NEGOTIATOR
# ==================================================

supplier_negotiator = SupplierNegotiationAgent(

    original_proposal,

    maximum_intervention_cost=25000,

    minimum_annual_price=100000

)


# ==================================================
# CREATE NEGOTIATION ENVIRONMENT
# ==================================================

environment = AutonomousNegotiationEnvironment(

    buyer_negotiator,

    supplier_negotiator,

    maximum_rounds=10

)


# ==================================================
# RUN NEGOTIATION
# ==================================================

result = environment.negotiate()


# ==================================================
# EXPERIMENTAL VALIDATION
# ==================================================

print("\n" + "=" * 60)

print("EXPERIMENTAL VALIDATION")

print("=" * 60)


assert result["agreement"], (

    "Buyer and supplier failed to reach agreement."

)


assert result["rounds"] == 5, (

    "Expected agreement in five rounds."

)


assert len(result["history"]) == 4, (

    "Expected four commercial counteroffers."

)


assert result["total_cost"] <= 25000, (

    "Supplier intervention budget exceeded."

)


assert (

    result["final_proposal"].annual_price >=
    100000

), (

    "Supplier minimum price violated."

)


assert (

    buyer.evaluate_proposal(
        result["final_proposal"]
    )["decision"] == "ACCEPTED"

), (

    "Final agreement rejected by underlying buyer."

)


assert abs(

    result["total_cost"] - 24100

) < 0.01, (

    "Unexpected commercial concession cost."

)


print("\nBuyer-Supplier Agreement: SUCCESS")

print(

    f"Negotiation Rounds: "
    f"{result['rounds']}"

)

print(

    f"Commercial Counteroffers: "
    f"{len(result['history'])}"

)

print(

    f"Final Annual Contract Price: "
    f"£{result['final_proposal'].annual_price:,.2f}"

)

print(

    f"Total Commercial Concession Cost: "
    f"£{result['total_cost']:,.2f}"

)

print("\nMARS EXPERIMENT 005 PASSED")
