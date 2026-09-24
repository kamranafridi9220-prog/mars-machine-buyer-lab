"""
MARS — Machine-Agent Revenue Science

Experiment 003

Multi-Dimensional Buyer Policy Discovery

Author: Kamran Khan
"""

from buyer_lab.buyer_agent import (
    AutonomousBuyerAgent
)

from inference.multidimensional_inference import (
    MultiDimensionalInferenceEngine
)


# --------------------------------------------------
# INITIALISE AUTONOMOUS BUYER
# --------------------------------------------------

buyer = AutonomousBuyerAgent()


# --------------------------------------------------
# INITIALISE MULTI-DIMENSIONAL INFERENCE
# --------------------------------------------------

engine = MultiDimensionalInferenceEngine(

    buyer

)


# --------------------------------------------------
# DISCOVER HIDDEN BUYER POLICIES
# --------------------------------------------------

discovered = engine.discover_all_policies()


# --------------------------------------------------
# EXPERIMENTAL GROUND TRUTH
# --------------------------------------------------

# These values are used only for validation.
# They are not supplied to the inference engine.

ground_truth = {

    "annual_price": 105000,

    "service_availability": 98.0,

    "supplier_reliability": 85.0,

    "contract_months": 36,

    "payment_days": 30

}


# --------------------------------------------------
# VALIDATE EXPERIMENTAL RESULTS
# --------------------------------------------------

print("\n" + "=" * 60)

print("EXPERIMENTAL VALIDATION")

print("=" * 60)


for variable, actual_value in ground_truth.items():

    estimated_value = discovered[variable][
        "estimated_threshold"
    ]

    error = abs(

        actual_value - estimated_value

    )

    print(f"\nVariable: {variable}")

    print(f"Actual threshold: {actual_value}")

    print(f"Estimated threshold: {estimated_value:.4f}")

    print(f"Absolute error: {error:.4f}")

    # Allow a tolerance of 1 for the price
    # and discrete contract/payment variables.

    if variable in [

        "annual_price",

        "contract_months",

        "payment_days"

    ]:

        allowed_error = 1

    else:

        allowed_error = 0.001

    assert error <= allowed_error, (

        f"Inference validation failed for {variable}"

    )

    print("VALIDATION PASSED")


print("\n" + "=" * 60)

print("ALL FIVE BUYER POLICIES DISCOVERED")

print("=" * 60)

print(

    f"\nTotal experimental buyer queries: "
    f"{engine.query_count}"

)

print("\nMARS EXPERIMENT 003 PASSED")
