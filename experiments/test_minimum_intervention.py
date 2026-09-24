"""
MARS — Machine-Agent Revenue Science

Experiment 004

Minimum Winning Intervention Validation

Author: Kamran Khan
"""

from buyer_lab.buyer_agent import (
    AutonomousBuyerAgent,
    CommercialProposal
)

from inference.multidimensional_inference import (
    MultiDimensionalInferenceEngine
)

from optimization.minimum_winning_intervention import (
    MinimumWinningInterventionEngine
)


# --------------------------------------------------
# INITIALISE BUYER
# --------------------------------------------------

buyer = AutonomousBuyerAgent()


# --------------------------------------------------
# DISCOVER BUYER REQUIREMENTS
# --------------------------------------------------

inference_engine = MultiDimensionalInferenceEngine(
    buyer
)

discovered_policies = (
    inference_engine.discover_all_policies()
)


# --------------------------------------------------
# CREATE REJECTED SUPPLIER PROPOSAL
# --------------------------------------------------

original_proposal = CommercialProposal(

    annual_price=120000,

    contract_months=48,

    service_availability=95.0,

    payment_days=14,

    supplier_reliability=90.0

)


# --------------------------------------------------
# CONFIRM ORIGINAL REJECTION
# --------------------------------------------------

original_response = buyer.evaluate_proposal(
    original_proposal
)

assert original_response["decision"] == "REJECTED"

print("\nORIGINAL PROPOSAL REJECTED")


# --------------------------------------------------
# INITIALISE INTERVENTION ENGINE
# --------------------------------------------------

intervention_engine = (
    MinimumWinningInterventionEngine(

        buyer,

        discovered_policies

    )
)


# --------------------------------------------------
# FIND MINIMUM WINNING INTERVENTION
# --------------------------------------------------

result = intervention_engine.optimise(
    original_proposal
)


# --------------------------------------------------
# VALIDATE FINAL BUYER ACCEPTANCE
# --------------------------------------------------

assert result["accepted"], (
    "Modified proposal was not accepted."
)


# --------------------------------------------------
# VALIDATE COMMERCIAL INTERVENTIONS
# --------------------------------------------------

assert len(result["interventions"]) == 4, (
    "Expected four commercial interventions."
)


assert result["total_cost"] > 0, (
    "Intervention cost must be positive."
)


# --------------------------------------------------
# DISPLAY FINAL RESULT
# --------------------------------------------------

print("\n" + "=" * 60)

print("EXPERIMENTAL VALIDATION")

print("=" * 60)

print("\nOriginal Proposal: REJECTED")

print("Modified Proposal: ACCEPTED")

print(

    f"Commercial Interventions: "
    f"{len(result['interventions'])}"

)

print(

    f"Estimated Intervention Cost: "
    f"£{result['total_cost']:,.2f}"

)

print("\nMARS EXPERIMENT 004 PASSED")
