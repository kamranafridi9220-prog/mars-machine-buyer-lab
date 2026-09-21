"""
MARS — Machine-Agent Revenue Science

Experiment 001:
Testing Autonomous Buyer Decisions

Author: Kamran Khan
"""

from buyer_lab.buyer_agent import (
    AutonomousBuyerAgent,
    CommercialProposal
)


buyer = AutonomousBuyerAgent()


proposals = [

    CommercialProposal(
        annual_price=100000,
        contract_months=24,
        service_availability=95.0,
        payment_days=30,
        supplier_reliability=90.0
    ),

    CommercialProposal(
        annual_price=100000,
        contract_months=24,
        service_availability=99.0,
        payment_days=30,
        supplier_reliability=90.0
    ),

    CommercialProposal(
        annual_price=120000,
        contract_months=24,
        service_availability=99.0,
        payment_days=30,
        supplier_reliability=90.0
    )

]


print("\nMARS AUTONOMOUS BUYER LAB")
print("=" * 50)


for index, proposal in enumerate(proposals, start=1):

    result = buyer.evaluate_proposal(proposal)

    print(f"\nExperiment {index}")

    print(f"Annual Price: £{proposal.annual_price:,.2f}")

    print(f"Service Availability: {proposal.service_availability}%")

    print(f"Buyer Decision: {result['decision']}")

    print(f"Buyer Message: {result['message']}")


print("\nExperiment completed.")
