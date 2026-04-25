from pathlib import Path
import pandas as pd

from AB_test import summarize_binary_outcome, ab_test_from_summary_table


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"


def main():
    df = pd.read_csv(PROCESSED_DATA_DIR / "AB_events_transactions_match_by_timestamp.csv")

    results = ab_test_from_summary_table(
        summary=df,
        control_group="Control",
        group_col="experiment_group",
        n_col="n",
        x_col="conversions",
    )

    OUTPUT_TABLE_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_TABLE_DIR / "ab_test_summary.csv", index=False)
    results.to_csv(OUTPUT_TABLE_DIR / "ab_test_results.csv", index=False)

    print("A/B test summary:")
    print(df.to_string(index=False))

    print("\nA/B test results:")
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()