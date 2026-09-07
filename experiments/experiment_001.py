import pandas as pd
import sys
import os

# Allow imports from project root
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from buyers.security_buyer import evaluate_vendor


DATA_PATH = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    ),
    "data",
    "vendors.csv"
)


def run_experiment():

    vendors = pd.read_csv(DATA_PATH)

    results = []

    for _, vendor in vendors.iterrows():

        vendor_data = vendor.to_dict()

        evaluation = evaluate_vendor(vendor_data)

        results.append({
            "vendor_id": vendor_data["vendor_id"],
            "decision": evaluation["decision"]
        })

    results_df = pd.DataFrame(results)

    print("\nMARS — Experiment 001")
    print("=" * 35)

    print(results_df.to_string(index=False))

    print("\nSummary")
    print("=" * 35)

    print(
        results_df["decision"]
        .value_counts()
        .to_string()
    )


if __name__ == "__main__":
    run_experiment()
