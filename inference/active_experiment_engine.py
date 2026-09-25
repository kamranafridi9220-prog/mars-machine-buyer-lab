"""
MARS — Machine-Agent Revenue Science

Experiment 012

Active Buyer Policy Discovery Engine

Author: Kamran Khan

Purpose:
Investigate hidden autonomous buyer policies
through controlled commercial experimentation.

The engine generates experimental proposals,
records buyer decisions, and maintains
observable experimental evidence.

The buyer's private decision policy is never
accessed by this engine.
"""

from dataclasses import asdict, replace


# ==================================================
# ACTIVE BUYER EXPERIMENT ENGINE
# ==================================================

class ActiveBuyerExperimentEngine:

    def __init__(

        self,

        buyer,

        initial_proposal

    ):

        self.buyer = buyer

        self.initial_proposal = initial_proposal

        self.experiment_history = []

        self.policy_beliefs = {}

        self.commercial_variables = [

            "annual_price",

            "contract_months",

            "service_availability",

            "payment_days",

            "supplier_reliability"

        ]


    # ==================================================
    # SUBMIT COMMERCIAL EXPERIMENT
    # ==================================================

    def submit_experiment(

        self,

        proposal,

        experiment_name

    ):

        response = self.buyer.evaluate_proposal(

            proposal

        )

        record = {

            "experiment": experiment_name,

            "proposal": asdict(proposal),

            "buyer_decision": response["decision"],

            "buyer_message": response["message"]

        }

        self.experiment_history.append(

            record

        )

        return record


    # ==================================================
    # GENERATE CONTROLLED EXPERIMENT
    # ==================================================

    def generate_controlled_experiment(

        self,

        variable,

        candidate_value,

        baseline_proposal=None

    ):

        if variable not in self.commercial_variables:

            raise ValueError(

                f"Unknown commercial variable: {variable}"

            )

        if baseline_proposal is None:

            baseline_proposal = (
                self.initial_proposal
            )

        experimental_proposal = replace(

            baseline_proposal,

            **{

                variable: candidate_value

            }

        )

        return experimental_proposal


    # ==================================================
    # RUN SINGLE-VARIABLE EXPERIMENT
    # ==================================================

    def run_variable_experiment(

        self,

        variable,

        candidate_value,

        baseline_proposal=None

    ):

        proposal = self.generate_controlled_experiment(

            variable=variable,

            candidate_value=candidate_value,

            baseline_proposal=baseline_proposal

        )

        experiment_name = (

            f"ACTIVE_POLICY_DISCOVERY_"

            f"{variable}_"

            f"{candidate_value}"

        )

        result = self.submit_experiment(

            proposal=proposal,

            experiment_name=experiment_name

        )

        return result


    # ==================================================
    # RECORD POLICY BELIEF
    # ==================================================

    def update_policy_belief(

        self,

        variable,

        estimated_value,

        confidence="EXPERIMENTAL"

    ):

        if variable not in self.commercial_variables:

            raise ValueError(

                f"Unknown commercial variable: {variable}"

            )

        self.policy_beliefs[variable] = {

            "estimated_value": estimated_value,

            "confidence": confidence

        }


    # ==================================================
    # RETRIEVE EXPERIMENTAL EVIDENCE
    # ==================================================

    def get_experimental_evidence(self):

        return {

            "initial_proposal": asdict(

                self.initial_proposal

            ),

            "experiments": (
                self.experiment_history
            ),

            "policy_beliefs": (
                self.policy_beliefs
            )

        }


    # ==================================================
    # EXPERIMENT SUMMARY
    # ==================================================

    def experiment_summary(self):

        accepted = sum(

            1

            for record in self.experiment_history

            if record["buyer_decision"] == "ACCEPTED"

        )

        rejected = sum(

            1

            for record in self.experiment_history

            if record["buyer_decision"] == "REJECTED"

        )

        return {

            "total_experiments": len(

                self.experiment_history

            ),

            "accepted_experiments": accepted,

            "rejected_experiments": rejected,

            "policy_beliefs": (
                self.policy_beliefs
            )

        }
