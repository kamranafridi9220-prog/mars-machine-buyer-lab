"""
MARS — Machine-Agent Revenue Science

Experiment 014

Comparative Policy Discovery Benchmark

Author: Kamran Khan

Purpose:
Provide a common evaluation framework for comparing
alternative black-box buyer policy discovery methods.

The benchmark evaluates:

1. Policy threshold accuracy
2. Absolute threshold error
3. Normalised threshold error
4. Policy discovery coverage
5. Buyer-query efficiency
6. Residual policy uncertainty

The benchmark itself does not access the buyer during
policy discovery. Ground-truth policy values are supplied
only after discovery for experimental evaluation.
"""


class PolicyDiscoveryBenchmark:

    def __init__(
        self,
        ground_truth,
        search_space
    ):

        self.ground_truth = ground_truth

        self.search_space = search_space

        self.results = {}


    # ========================================================
    # EXTRACT ESTIMATED THRESHOLD
    # ========================================================

    def _extract_threshold(
        self,
        method_results,
        variable
    ):

        if variable not in method_results:

            return None


        result = method_results[variable]


        # Experiment 003 format
        if isinstance(result, dict):

            if "estimated_threshold" in result:

                return result[
                    "estimated_threshold"
                ]


        # Experiment 013 format
        if isinstance(
            result,
            (int, float)
        ):

            return result


        return None


    # ========================================================
    # ABSOLUTE ERROR
    # ========================================================

    def _absolute_error(
        self,
        estimated,
        actual
    ):

        if estimated is None:

            return None


        return abs(
            estimated - actual
        )


    # ========================================================
    # NORMALISED ERROR
    # ========================================================

    def _normalised_error(
        self,
        variable,
        absolute_error
    ):

        if absolute_error is None:

            return None


        configuration = (
            self.search_space[variable]
        )


        search_width = (

            configuration["upper"]
            -
            configuration["lower"]

        )


        if search_width == 0:

            return 0


        return (

            absolute_error
            /
            search_width

        )


    # ========================================================
    # RESIDUAL UNCERTAINTY
    # ========================================================

    def _extract_uncertainty(
        self,
        method_results,
        variable
    ):

        if variable not in method_results:

            return None


        result = method_results[variable]


        if isinstance(result, dict):

            if "uncertainty" in result:

                return result[
                    "uncertainty"
                ]


            if (
                "lower" in result
                and
                "upper" in result
            ):

                return (

                    result["upper"]
                    -
                    result["lower"]

                )


        return None


    # ========================================================
    # EVALUATE DISCOVERY METHOD
    # ========================================================

    def evaluate_method(
        self,
        method_name,
        discovered_policy,
        query_count,
        belief_state=None
    ):

        variable_results = {}

        total_absolute_error = 0

        total_normalised_error = 0

        discovered_variables = 0

        total_uncertainty = 0

        uncertainty_variables = 0


        for variable, actual_value in (

            self.ground_truth.items()

        ):

            estimated_value = (
                self._extract_threshold(
                    discovered_policy,
                    variable
                )
            )


            absolute_error = (
                self._absolute_error(
                    estimated_value,
                    actual_value
                )
            )


            normalised_error = (
                self._normalised_error(
                    variable,
                    absolute_error
                )
            )


            uncertainty_source = (

                belief_state

                if belief_state is not None

                else discovered_policy

            )


            residual_uncertainty = (
                self._extract_uncertainty(
                    uncertainty_source,
                    variable
                )
            )


            if estimated_value is not None:

                discovered_variables += 1

                total_absolute_error += (
                    absolute_error
                )

                total_normalised_error += (
                    normalised_error
                )


            if residual_uncertainty is not None:

                total_uncertainty += (
                    residual_uncertainty
                )

                uncertainty_variables += 1


            variable_results[variable] = {

                "ground_truth":
                    actual_value,

                "estimated_threshold":
                    estimated_value,

                "absolute_error":
                    absolute_error,

                "normalised_error":
                    normalised_error,

                "residual_uncertainty":
                    residual_uncertainty

            }


        total_variables = len(
            self.ground_truth
        )


        coverage = (

            discovered_variables
            /
            total_variables

            if total_variables

            else 0

        )


        mean_absolute_error = (

            total_absolute_error
            /
            discovered_variables

            if discovered_variables

            else None

        )


        mean_normalised_error = (

            total_normalised_error
            /
            discovered_variables

            if discovered_variables

            else None

        )


        mean_residual_uncertainty = (

            total_uncertainty
            /
            uncertainty_variables

            if uncertainty_variables

            else None

        )


        queries_per_discovered_policy = (

            query_count
            /
            discovered_variables

            if discovered_variables

            else None

        )


        result = {

            "method":
                method_name,

            "query_count":
                query_count,

            "discovered_variables":
                discovered_variables,

            "total_variables":
                total_variables,

            "coverage":
                coverage,

            "mean_absolute_error":
                mean_absolute_error,

            "mean_normalised_error":
                mean_normalised_error,

            "mean_residual_uncertainty":
                mean_residual_uncertainty,

            "queries_per_discovered_policy":
                queries_per_discovered_policy,

            "variables":
                variable_results

        }


        self.results[
            method_name
        ] = result


        return result


    # ========================================================
    # COMPARE TWO METHODS
    # ========================================================

    def compare_methods(
        self,
        method_a,
        method_b
    ):

        if method_a not in self.results:

            raise ValueError(
                f"Unknown benchmark method: "
                f"{method_a}"
            )


        if method_b not in self.results:

            raise ValueError(
                f"Unknown benchmark method: "
                f"{method_b}"
            )


        a = self.results[method_a]

        b = self.results[method_b]


        query_difference = (

            b["query_count"]
            -
            a["query_count"]

        )


        if a["query_count"] > 0:

            query_change_percentage = (

                query_difference
                /
                a["query_count"]
                *
                100

            )

        else:

            query_change_percentage = None


        comparison = {

            "method_a":
                method_a,

            "method_b":
                method_b,

            "query_difference":
                query_difference,

            "query_change_percentage":
                query_change_percentage,

            "coverage_difference":

                b["coverage"]
                -
                a["coverage"],

            "normalised_error_difference":

                (
                    b["mean_normalised_error"]
                    -
                    a["mean_normalised_error"]
                )

                if (
                    a["mean_normalised_error"]
                    is not None
                    and
                    b["mean_normalised_error"]
                    is not None
                )

                else None

        }


        return comparison


    # ========================================================
    # PRINT METHOD REPORT
    # ========================================================

    def print_method_report(
        self,
        method_name
    ):

        result = self.results[
            method_name
        ]


        print("\n" + "=" * 70)

        print(
            f"MARS BENCHMARK — "
            f"{method_name}"
        )

        print("=" * 70)


        print(
            "Buyer Queries:",
            result["query_count"]
        )


        print(
            "Policy Coverage:",
            f"{result['coverage'] * 100:.2f}%"
        )


        print(
            "Discovered Variables:",
            f"{result['discovered_variables']}/"
            f"{result['total_variables']}"
        )


        print(
            "Mean Absolute Error:",
            result["mean_absolute_error"]
        )


        print(
            "Mean Normalised Error:",
            result["mean_normalised_error"]
        )


        print(
            "Mean Residual Uncertainty:",
            result[
                "mean_residual_uncertainty"
            ]
        )


        print(
            "Queries per Discovered Policy:",
            result[
                "queries_per_discovered_policy"
            ]
        )


        print(
            "\nVARIABLE-LEVEL RESULTS"
        )


        for variable, data in (

            result["variables"].items()

        ):

            print("\n" + variable)

            print(
                "  Ground Truth:",
                data["ground_truth"]
            )

            print(
                "  Estimated:",
                data[
                    "estimated_threshold"
                ]
            )

            print(
                "  Absolute Error:",
                data["absolute_error"]
            )

            print(
                "  Normalised Error:",
                data["normalised_error"]
            )

            print(
                "  Residual Uncertainty:",
                data[
                    "residual_uncertainty"
                ]
            )


    # ========================================================
    # RETURN ALL RESULTS
    # ========================================================

    def get_results(self):

        return self.results
