"""
MARS — Machine-Agent Revenue Science

Experiment 002:
Black-Box Buyer Price Policy Inference

Author:
Kamran Khan
"""

from buyer_lab.buyer_agent import AutonomousBuyerAgent

from inference.buyer_policy_inference import (
    BuyerPolicyInferenceEngine
)


# Initialise autonomous buyer.

buyer = AutonomousBuyerAgent()


# Initialise inference engine.

inference_engine = BuyerPolicyInferenceEngine(buyer)


# Run black-box price discovery.

result = inference_engine.infer_maximum_price(

    minimum_price=50000,

    maximum_price=150000,

    tolerance=1

)


# Validate experimental result against the
# known ground truth in this controlled simulation.

actual_hidden_budget = 105000

estimated_budget = result["estimated_maximum_price"]

absolute_error = abs(
    actual_hidden_budget - estimated_budget
)


print("\nEXPERIMENTAL VALIDATION")

print("=" * 55)

print(f"Actual Hidden Budget: £{actual_hidden_budget:,.2f}")

print(f"Estimated Budget: £{estimated_budget:,.2f}")

print(f"Absolute Estimation Error: £{absolute_error:,.2f}")


assert absolute_error <= 1, (
    "Inference error exceeds the permitted tolerance."
)

print("\nEXPERIMENT 002 PASSED")
