"""
MARS — Machine-Agent Revenue Science

Experiment 022

Adaptive Diagnostic Probe Generator

Author: Kamran Khan

Purpose:
Generate controlled commercial proposals for estimating
the behavioural uncertainty of an unknown autonomous buyer.

The generator does not access:

- hidden buyer thresholds
- simulator noise parameters
- private buyer decision rules

Instead, it constructs a diversified set of commercial
probes around an estimated buyer policy obtained through
previous black-box inference.

The probes intentionally include:

1. estimated boundary probes
2. slightly favourable probes
3. slightly unfavourable probes
4. joint-boundary probes

This allows MARS to observe decision stability close to
commercial decision boundaries.
"""

from dataclasses import replace


class DiagnosticProbeGenerator:

    def __init__(
        self,
        reference_proposal,
        estimated_policy
    ):

        self.reference_proposal = (
            reference_proposal
        )

        self.estimated_policy = (
            estimated_policy
        )

        self.directions = {

            "annual_price":
                "maximum",

            "contract_months":
                "maximum",

            "service_availability":
                "minimum",

            "payment_days":
                "minimum",

            "supplier_reliability":
                "minimum"
        }

        self.perturbations = {

            "annual_price":
                1000.0,

            "contract_months":
                2,

            "service_availability":
                0.20,

            "payment_days":
                2,

            "supplier_reliability":
                1.0
        }


    # ========================================================
    # VALIDATE POLICY
    # ========================================================

    def validate_policy(
        self
    ):

        missing = [

            variable

            for variable in self.directions

            if variable not in self.estimated_policy

        ]

        if missing:

            raise ValueError(
                "Estimated policy is missing variables: "
                +
                ", ".join(
                    missing
                )
            )


    # ========================================================
    # NORMALISE VALUE
    # ========================================================

    @staticmethod
    def _normalise_value(
        variable,
        value
    ):

        if variable in [
            "contract_months",
            "payment_days"
        ]:

            return int(
                round(
                    value
                )
            )

        return float(
            value
        )


    # ========================================================
    # CREATE SAFE REFERENCE
    # ========================================================

    def create_policy_reference(
        self
    ):

        """
        Construct a proposal predicted to satisfy the
        estimated buyer policy.

        This is based only on inferred thresholds.
        """

        self.validate_policy()

        values = {}

        for variable, threshold in (
            self.estimated_policy.items()
        ):

            values[
                variable
            ] = (
                self._normalise_value(
                    variable,
                    threshold
                )
            )

        return replace(
            self.reference_proposal,
            **values
        )


    # ========================================================
    # CREATE EXACT BOUNDARY PROBE
    # ========================================================

    def create_boundary_probe(
        self,
        variable
    ):

        if variable not in self.directions:

            raise ValueError(
                f"Unknown commercial variable: "
                f"{variable}"
            )

        baseline = (
            self.create_policy_reference()
        )

        threshold = (
            self.estimated_policy[
                variable
            ]
        )

        threshold = (
            self._normalise_value(
                variable,
                threshold
            )
        )

        return replace(
            baseline,
            **{
                variable:
                    threshold
            }
        )


    # ========================================================
    # CREATE FAVOURABLE PROBE
    # ========================================================

    def create_favourable_probe(
        self,
        variable
    ):

        """
        Move slightly toward the buyer-favourable side
        of the estimated threshold.
        """

        baseline = (
            self.create_policy_reference()
        )

        threshold = (
            self.estimated_policy[
                variable
            ]
        )

        step = (
            self.perturbations[
                variable
            ]
        )

        direction = (
            self.directions[
                variable
            ]
        )

        if direction == "maximum":

            value = (
                threshold
                -
                step
            )

        else:

            value = (
                threshold
                +
                step
            )

        value = (
            self._normalise_value(
                variable,
                value
            )
        )

        return replace(
            baseline,
            **{
                variable:
                    value
            }
        )


    # ========================================================
    # CREATE UNFAVOURABLE PROBE
    # ========================================================

    def create_unfavourable_probe(
        self,
        variable
    ):

        """
        Move slightly toward the buyer-unfavourable side
        of the estimated threshold.
        """

        baseline = (
            self.create_policy_reference()
        )

        threshold = (
            self.estimated_policy[
                variable
            ]
        )

        step = (
            self.perturbations[
                variable
            ]
        )

        direction = (
            self.directions[
                variable
            ]
        )

        if direction == "maximum":

            value = (
                threshold
                +
                step
            )

        else:

            value = (
                threshold
                -
                step
            )

        value = (
            self._normalise_value(
                variable,
                value
            )
        )

        return replace(
            baseline,
            **{
                variable:
                    value
            }
        )


    # ========================================================
    # GENERATE VARIABLE PROBE SET
    # ========================================================

    def generate_variable_probe_set(
        self,
        variable
    ):

        return [

            self.create_boundary_probe(
                variable
            ),

            self.create_favourable_probe(
                variable
            ),

            self.create_unfavourable_probe(
                variable
            )

        ]


    # ========================================================
    # GENERATE JOINT BOUNDARY PROBE
    # ========================================================

    def create_joint_boundary_probe(
        self
    ):

        """
        Place every commercial variable at its
        currently estimated threshold.

        This is deliberately difficult for a stochastic
        buyer and can reveal decision instability when
        several constraints are simultaneously marginal.
        """

        return (
            self.create_policy_reference()
        )


    # ========================================================
    # GENERATE ALL DIAGNOSTIC PROBES
    # ========================================================

    def generate_all_probes(
        self
    ):

        self.validate_policy()

        probes = []

        for variable in self.directions:

            variable_probes = (
                self.generate_variable_probe_set(
                    variable
                )
            )

            probes.extend(
                variable_probes
            )

        probes.append(
            self.create_joint_boundary_probe()
        )

        return probes


    # ========================================================
    # GENERATE NAMED PROBES
    # ========================================================

    def generate_named_probes(
        self
    ):

        """
        Returns probe metadata as well as the proposal.

        This is useful for later analysis because MARS
        can distinguish exact-boundary, favourable,
        unfavourable, and joint-boundary observations.
        """

        self.validate_policy()

        probes = []

        for variable in self.directions:

            probes.append(
                {
                    "name":
                        (
                            f"{variable}_boundary"
                        ),

                    "variable":
                        variable,

                    "probe_type":
                        "BOUNDARY",

                    "proposal":
                        self.create_boundary_probe(
                            variable
                        )
                }
            )

            probes.append(
                {
                    "name":
                        (
                            f"{variable}_favourable"
                        ),

                    "variable":
                        variable,

                    "probe_type":
                        "FAVOURABLE",

                    "proposal":
                        self.create_favourable_probe(
                            variable
                        )
                }
            )

            probes.append(
                {
                    "name":
                        (
                            f"{variable}_unfavourable"
                        ),

                    "variable":
                        variable,

                    "probe_type":
                        "UNFAVOURABLE",

                    "proposal":
                        self.create_unfavourable_probe(
                            variable
                        )
                }
            )

        probes.append(
            {
                "name":
                    "joint_policy_boundary",

                "variable":
                    "MULTI_VARIABLE",

                "probe_type":
                    "JOINT_BOUNDARY",

                "proposal":
                    self.create_joint_boundary_probe()
            }
        )

        return probes


    # ========================================================
    # SUMMARY
    # ========================================================

    def generate_summary(
        self
    ):

        probes = (
            self.generate_named_probes()
        )

        boundary_count = sum(
            1
            for probe in probes
            if probe[
                "probe_type"
            ] == "BOUNDARY"
        )

        favourable_count = sum(
            1
            for probe in probes
            if probe[
                "probe_type"
            ] == "FAVOURABLE"
        )

        unfavourable_count = sum(
            1
            for probe in probes
            if probe[
                "probe_type"
            ] == "UNFAVOURABLE"
        )

        joint_count = sum(
            1
            for probe in probes
            if probe[
                "probe_type"
            ] == "JOINT_BOUNDARY"
        )

        return {

            "total_probes":
                len(
                    probes
                ),

            "boundary_probes":
                boundary_count,

            "favourable_probes":
                favourable_count,

            "unfavourable_probes":
                unfavourable_count,

            "joint_boundary_probes":
                joint_count
        }
