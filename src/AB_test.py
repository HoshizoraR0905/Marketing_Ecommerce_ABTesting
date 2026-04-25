import pandas as pd
from dataclasses import dataclass
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep
import math


@dataclass
class ABTestResult:
    comparison: str
    n_control: int
    n_treatment: int
    x_control: int
    x_treatment: int
    p_control: float
    p_treatment: float
    absolute_lift: float
    relative_lift: float
    z_stat: float
    p_value: float
    ci_low: float
    ci_high: float


def two_proportion_ab_test(
    n_control: int,
    x_control: int,
    n_treatment: int,
    x_treatment: int,
    treatment_name: str = "Treatment",
    control_name: str = "Control",
    alpha: float = 0.05,
) -> ABTestResult:
    
    if n_control <= 0 or n_treatment <= 0:
        raise ValueError("Sample sizes must be positive.")

    if not (0 <= x_control <= n_control):
        raise ValueError("x_control must be between 0 and n_control.")

    if not (0 <= x_treatment <= n_treatment):
        raise ValueError("x_treatment must be between 0 and n_treatment.")

    p_control = x_control / n_control
    p_treatment = x_treatment / n_treatment

    absolute_lift = p_treatment - p_control

    if p_control == 0:
        relative_lift = math.nan
    else:
        relative_lift = absolute_lift / p_control

    z_stat, p_value = proportions_ztest(
        count=[x_treatment, x_control],
        nobs=[n_treatment, n_control],
        alternative="two-sided",
    )

    ci_low, ci_high = confint_proportions_2indep(
        count1=x_treatment,
        nobs1=n_treatment,
        count2=x_control,
        nobs2=n_control,
        method="wald",
        compare="diff",
        alpha=alpha,
    )

    return ABTestResult(
        comparison=f"{treatment_name} vs {control_name}",
        n_control=n_control,
        n_treatment=n_treatment,
        x_control=x_control,
        x_treatment=x_treatment,
        p_control=p_control,
        p_treatment=p_treatment,
        absolute_lift=absolute_lift,
        relative_lift=relative_lift,
        z_stat=z_stat,
        p_value=p_value,
        ci_low=ci_low,
        ci_high=ci_high,
    )


def ab_test_from_summary_table(
    summary: pd.DataFrame,
    control_group: str = "Control",
    group_col: str = "experiment_group",
    n_col: str = "n",
    x_col: str = "conversions",
) -> pd.DataFrame:
    """
    Run pairwise A/B tests comparing every non-control group against control.

    Expected summary table format:

    experiment_group | n | conversions
    Control          | ... | ...
    Variant_A        | ... | ...
    Variant_B        | ... | ...
    """

    if control_group not in summary[group_col].values:
        raise ValueError(f"Control group '{control_group}' not found.")

    control_row = summary.loc[summary[group_col] == control_group].iloc[0]

    results = []

    for _, row in summary.iterrows():
        group = row[group_col]

        if group == control_group:
            continue

        result = two_proportion_ab_test(
            n_control=int(control_row[n_col]),
            x_control=int(control_row[x_col]),
            n_treatment=int(row[n_col]),
            x_treatment=int(row[x_col]),
            treatment_name=str(group),
            control_name=control_group,
        )

        results.append(result.__dict__)

    return pd.DataFrame(results)

def summarize_binary_outcome(
    df: pd.DataFrame,
    group_col: str,
    outcome_col: str,
    n_col_name: str = "n",
    x_col_name: str = "conversions",
) -> pd.DataFrame:
    """
    Summarize binary outcome by group.

    Example:
    group_col = "experiment_group"
    outcome_col = "converted"
    """

    summary = (
        df.groupby(group_col)
        .agg(
            n=(outcome_col, "count"),
            conversions=(outcome_col, "sum"),
            conversion_rate=(outcome_col, "mean"),
        )
        .reset_index()
    )

    summary = summary.rename(
        columns={
            "n": n_col_name,
            "conversions": x_col_name,
        }
    )

    return summary
