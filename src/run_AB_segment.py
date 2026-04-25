from pathlib import Path
import pandas as pd

from AB_test import ab_test_from_summary_table


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"


def run_ab_tests_by_segment(
    summary: pd.DataFrame,
    segment_col: str,
    group_col: str = "experiment_group",
    control_group: str = "Control",
    n_col: str = "n",
    x_col: str = "conversions",
    min_n_per_group: int = 1000,
) -> pd.DataFrame:
    all_results = []

    for segment_value, seg_summary in summary.groupby(segment_col):
        # Require control group
        if control_group not in seg_summary[group_col].values:
            continue

        # Avoid tiny/noisy groups
        if seg_summary[n_col].min() < min_n_per_group:
            continue

        results = ab_test_from_summary_table(
            summary=seg_summary,
            control_group=control_group,
            group_col=group_col,
            n_col=n_col,
            x_col=x_col,
        )

        results.insert(0, segment_col, segment_value)
        all_results.append(results)

    if not all_results:
        return pd.DataFrame()

    return pd.concat(all_results, ignore_index=True)


def main():
    OUTPUT_TABLE_DIR.mkdir(parents=True, exist_ok=True)

    loyalty_summary = pd.read_csv(
        PROCESSED_DATA_DIR / "conversion_by_loyalty_and_experiment_group.csv"
    )

    acquisition_summary = pd.read_csv(
        PROCESSED_DATA_DIR / "conversion_by_acquisition_and_experiment_group.csv"
    )

    loyalty_results = run_ab_tests_by_segment(
        summary=loyalty_summary,
        segment_col="loyalty_tier",
        group_col="experiment_group",
        control_group="Control",
        n_col="n",
        x_col="conversions",
        min_n_per_group=1000,
    )

    acquisition_results = run_ab_tests_by_segment(
        summary=acquisition_summary,
        segment_col="acquisition_channel",
        group_col="experiment_group",
        control_group="Control",
        n_col="n",
        x_col="conversions",
        min_n_per_group=1000,
    )

    loyalty_output_path = OUTPUT_TABLE_DIR / "ab_test_by_loyalty_tier.csv"
    acquisition_output_path = OUTPUT_TABLE_DIR / "ab_test_by_acquisition_channel.csv"

    loyalty_results.to_csv(loyalty_output_path, index=False)
    acquisition_results.to_csv(acquisition_output_path, index=False)

    print("\nA/B test by loyalty tier:")
    print(loyalty_results.to_string(index=False))

    print("\nA/B test by acquisition channel:")
    print(acquisition_results.to_string(index=False))

    print(f"\nSaved: {loyalty_output_path}")
    print(f"Saved: {acquisition_output_path}")


if __name__ == "__main__":
    main()