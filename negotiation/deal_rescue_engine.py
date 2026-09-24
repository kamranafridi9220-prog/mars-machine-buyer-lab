"""
MARS — Machine-Agent Revenue Science

Experiment 008

Autonomous Commercial Deal Rescue

Author: Kamran Khan

Research Objective:

Investigate whether alternative commercial
delivery packages can rescue buyer-acceptable
but financially infeasible B2B agreements.

The system must protect supplier financial
constraints and verify buyer acceptance.
"""

from dataclasses import dataclass


# ==================================================
# COMMERCIAL PACKAGE
# ==================================================

@dataclass(frozen=True)

class CommercialPackage:

    name: str

    operational_saving: float

    implementation_cost: float

    description: str


# ==================================================
# COMMERCIAL DEAL RESCUE ENGINE
# ==================================================

class CommercialDealRescueEngine:

    def __init__(
        self,
        buyer,
        supplier,
        concession_budget=25000
    ):

        self.buyer = buyer

        self.supplier = supplier

        self.concession_budget = concession_budget

        self.evaluated_packages = []

        self.buyer_queries = 0

    # --------------------------------------------------
    # BUYER EVALUATION
    # --------------------------------------------------

    def evaluate_buyer(
        self,
        proposal
    ):

        self.buyer_queries += 1

        return self.buyer.evaluate_proposal(
            proposal
        )

    # --------------------------------------------------
    # CALCULATE NET COMMERCIAL COST
    # --------------------------------------------------

    def calculate_net_cost(
        self,
        proposal,
        package
    ):

        original_cost = (
            self.supplier.calculate_cost(
                proposal
            )
        )

        net_cost = (

            original_cost

            - package.operational_saving

            + package.implementation_cost

        )

        return max(
            0,
            net_cost
        )

    # --------------------------------------------------
    # EVALUATE COMMERCIAL PACKAGE
    # --------------------------------------------------

    def evaluate_package(
        self,
        proposal,
        package,
        buyer_accepts_package
    ):

        buyer_response = self.evaluate_buyer(
            proposal
        )

        buyer_accepts_terms = (

            buyer_response["decision"]
            == "ACCEPTED"

        )

        original_cost = (
            self.supplier.calculate_cost(
                proposal
            )
        )

        net_cost = self.calculate_net_cost(

            proposal,

            package

        )

        within_budget = (

            net_cost <=
            self.concession_budget

        )

        price_acceptable = (

            proposal.annual_price >=
            self.supplier.minimum_annual_price

        )

        commercially_feasible = (

            buyer_accepts_terms

            and buyer_accepts_package

            and within_budget

            and price_acceptable

        )

        result = {

            "package":
                package.name,

            "description":
                package.description,

            "original_cost":
                original_cost,

            "operational_saving":
                package.operational_saving,

            "implementation_cost":
                package.implementation_cost,

            "net_cost":
                net_cost,

            "buyer_accepts_terms":
                buyer_accepts_terms,

            "buyer_accepts_package":
                buyer_accepts_package,

            "within_budget":
                within_budget,

            "price_acceptable":
                price_acceptable,

            "commercially_feasible":
                commercially_feasible

        }

        self.evaluated_packages.append(
            result
        )

        return result

    # --------------------------------------------------
    # SEARCH FOR FEASIBLE AGREEMENTS
    # --------------------------------------------------

    def rescue_deal(
        self,
        proposal,
        packages,
        package_acceptance
    ):

        print("\n" + "=" * 60)

        print("MARS COMMERCIAL DEAL RESCUE")

        print("=" * 60)

        self.evaluated_packages = []

        self.buyer_queries = 0

        feasible_packages = []

        for package in packages:

            print(
                f"\nEvaluating package: "
                f"{package.name}"
            )

            buyer_accepts_package = (
                package_acceptance.get(
                    package.name,
                    False
                )
            )

            result = self.evaluate_package(

                proposal,

                package,

                buyer_accepts_package

            )

            print(

                f"Original concession cost: "
                f"£{result['original_cost']:,.2f}"

            )

            print(

                f"Operational saving: "
                f"£{result['operational_saving']:,.2f}"

            )

            print(

                f"Implementation cost: "
                f"£{result['implementation_cost']:,.2f}"

            )

            print(

                f"Net concession cost: "
                f"£{result['net_cost']:,.2f}"

            )

            print(

                f"Buyer accepts terms: "
                f"{result['buyer_accepts_terms']}"

            )

            print(

                f"Buyer accepts package: "
                f"{result['buyer_accepts_package']}"

            )

            print(

                f"Commercially feasible: "
                f"{result['commercially_feasible']}"

            )

            if result[
                "commercially_feasible"
            ]:

                feasible_packages.append(
                    result
                )

        # --------------------------------------------------
        # SELECT LOWEST-COST FEASIBLE PACKAGE
        # --------------------------------------------------

        if not feasible_packages:

            print(
                "\nNO COMMERCIALLY FEASIBLE "
                "AGREEMENT FOUND"
            )

            return None

        best_package = min(

            feasible_packages,

            key=lambda result:
                result["net_cost"]

        )

        print("\n" + "=" * 60)

        print("COMMERCIAL DEAL RESCUE SUCCESSFUL")

        print("=" * 60)

        print(

            f"Selected package: "
            f"{best_package['package']}"

        )

        print(

            f"Net concession cost: "
            f"£{best_package['net_cost']:,.2f}"

        )

        print(

            f"Remaining budget: "
            f"£{self.concession_budget - best_package['net_cost']:,.2f}"

        )

        return best_package
