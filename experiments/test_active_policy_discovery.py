"""
MARS — Machine-Agent Revenue Science

Experiment 012

Active Buyer Policy Discovery and
Evidence-Based AI Supplier Negotiation

Author: Kamran Khan

Purpose:
Integrate black-box buyer policy inference,
experimental evidence, structured policy beliefs,
and generative AI supplier strategy generation.

The supplier does not access the buyer's
private procurement policy variables.
"""

from dataclasses import asdict

from buyer_lab.buyer_agent import (
    AutonomousBuyerAgent,
    CommercialProposal
)

from inference.active_experiment_engine import (
    ActiveBuyerExperimentEngine
)

from inference.multidimensional_inference import (
    MultiDimensionalInferenceEngine
)

from inference.buyer_policy_belief_model import (
    BuyerPolicyBeliefModel
)

from negotiation.ai_supplier_strategy_agent import (
    AISupplierStrategyAgent
)


# ==================================================
# EXPERIMENT CONFIGURATION
# ==================================================

MAXIMUM_INTERVENTION_COST = 35000

MINIMUM_ANNUAL_PRICE = 100000

MAX_AI_ATTEMPTS = 5


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


print("\n" + "=" * 70)

print("MARS — EXPERIMENT 012")

print("ACTIVE BUYER POLICY DISCOVERY")

print("=" * 70)


# ==================================================
# INITIALISE AUTONOMOUS BUYER
# ==================================================

buyer = AutonomousBuyerAgent()


# ==================================================
# INITIALISE ACTIVE EXPERIMENT ENGINE
# ==================================================

active_engine = ActiveBuyerExperimentEngine(

    buyer=buyer,

    initial_proposal=initial_proposal

)


# ==================================================
# INITIAL BUYER EVALUATION
# ==================================================

print("\nINITIAL BUYER EVALUATION")

initial_result = active_engine.submit_experiment(

    proposal=initial_proposal,

    experiment_name="INITIAL_COMMERCIAL_PROPOSAL"

)

print(

    "Buyer Decision:",

    initial_result["buyer_decision"]

)


# ==================================================
# MULTI-DIMENSIONAL POLICY DISCOVERY
# ==================================================

print("\nSTARTING BLACK-BOX POLICY INFERENCE")

inference_engine = MultiDimensionalInferenceEngine(

    buyer=buyer

)

discovered_policies = (
    inference_engine.discover_all_policies()
)


# ==================================================
# INITIALISE BUYER POLICY BELIEF MODEL
# ==================================================

belief_model = BuyerPolicyBeliefModel()

belief_model.update_from_inference(

    discovered_policies

)

estimated_policy = (
    belief_model.generate_belief_report()
)


# ==================================================
# STORE DISCOVERED POLICY BELIEFS
# ==================================================

for variable, threshold in (
    estimated_policy.items()
):

    active_engine.update_policy_belief(

        variable=variable,

        estimated_value=threshold,

        confidence="EXPERIMENTAL"

    )


# ==================================================
# INITIALISE AI SUPPLIER
# ==================================================

supplier = AISupplierStrategyAgent(

    original_proposal=initial_proposal,

    maximum_intervention_cost=(
        MAXIMUM_INTERVENTION_COST
    ),

    minimum_annual_price=(
        MINIMUM_ANNUAL_PRICE
    )

)


# ==================================================
# CONSTRUCT EXPERIMENTAL INTELLIGENCE
# ==================================================

experimental_intelligence = {

    "buyer_decision": (
        initial_result["buyer_decision"]
    ),

    "estimated_buyer_policy": (
        estimated_policy
    ),

    "policy_uncertainty": (
        belief_model.get_policy_uncertainty()
    ),

    "total_inference_queries": (
        inference_engine.query_count
    ),

    "research_context": (
        "Policy estimates were obtained through "
        "controlled black-box experiments."
    )

}


# ==================================================
# RECORD INITIAL BUYER FEEDBACK
# ==================================================

supplier.record_buyer_feedback(

    initial_proposal,

    experimental_intelligence

)


# ==================================================
# AI SUPPLIER NEGOTIATION
# ==================================================

agreement = False

approved_strategies = 0

rejected_strategies = 0

buyer_evaluations = 1


for attempt in range(

    1,

    MAX_AI_ATTEMPTS + 1

):

    print("\n" + "-" * 70)

    print(

        f"AI STRATEGY ATTEMPT {attempt}"

    )

    print("-" * 70)

    print("\nAI SUPPLIER GENERATING STRATEGY...")

    strategy = supplier.generate_strategy(

        buyer_feedback=experimental_intelligence

    )

    candidate = strategy["candidate"]

    validation = strategy["validation"]

    print("\nAI STRATEGY REASONING")

    print(strategy["reasoning"])

    print("\nPROPOSED COMMERCIAL STRATEGY")

    print(candidate)

    # ----------------------------------------------
    # COMMERCIAL VALIDATION
    # ----------------------------------------------

    if not validation["valid"]:

        rejected_strategies += 1

        print("\nSTRATEGY COMMERCIALLY REJECTED")

        print(validation["reason"])

        continue

    approved_strategies += 1

    print("\nSTRATEGY COMMERCIALLY APPROVED")

    print(

        "Estimated Intervention Cost: £"

        f"{validation['cost']:,.2f}"

    )

    # ----------------------------------------------
    # EVALUATE AGAINST POLICY BELIEFS
    # ----------------------------------------------

    belief_evaluation = (
        belief_model.evaluate_against_beliefs(
            candidate
        )
    )

    print("\nPOLICY BELIEF EVALUATION")

    print(belief_evaluation)

    # ----------------------------------------------
    # SUBMIT PROPOSAL TO AUTONOMOUS BUYER
    # ----------------------------------------------

    buyer_response = buyer.evaluate_proposal(

        candidate

    )

    buyer_evaluations += 1

    supplier.record_buyer_feedback(

        candidate,

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

    # ----------------------------------------------
    # UPDATE AI INTELLIGENCE
    # ----------------------------------------------

    experimental_intelligence = {

        "buyer_decision": (
            buyer_response["decision"]
        ),

        "estimated_buyer_policy": (
            estimated_policy
        ),

        "policy_uncertainty": (
            belief_model.get_policy_uncertainty()
        ),

        "estimated_violations": (
            belief_evaluation[
                "estimated_violations"
            ]
        ),

        "research_context": (
            "Revise the commercial proposal "
            "using inferred purchasing constraints."
        )

    }


# ==================================================
# FINAL EXPERIMENT RESULTS
# ==================================================

print("\n" + "=" * 70)

print("MARS — EXPERIMENT 012 RESULTS")

print("=" * 70)

print(

    "Agreement Reached:",

    agreement

)

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

print(

    "Commercially Approved Strategies:",

    approved_strategies

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

    "Policy Discovery Queries:",

    inference_engine.query_count

)

print(

    "Total Buyer Queries:",

    buyer_evaluations + inference_engine.query_count

)

print("\nESTIMATED BUYER POLICY")

for variable, threshold in (
    estimated_policy.items()
):

    print(

        f"{variable}: {threshold}"

    )

print("=" * 70)
