from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def main():
    df = pd.read_csv(PROCESSED_DATA_DIR / "customer_campaign_analysis.csv")

    print("Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nOverall conversion rate:")
    print(df["converted"].mean())

    print("\nRevenue summary:")
    print(df["total_revenue"].describe())

    print("\nConversion rate by experiment group:")
    print(df.groupby("experiment_group")["converted"].mean().sort_values(ascending=False))

    print("\nConversion rate by channel:")
    print(df.groupby("channel")["converted"].mean().sort_values(ascending=False))

    print("\nAverage revenue by channel:")
    print(df.groupby("channel")["total_revenue"].mean().sort_values(ascending=False))

    print("\nConversion rate by loyalty tier:")
    print(df.groupby("loyalty_tier")["converted"].mean().sort_values(ascending=False))

    print("\nMissing values:")
    missing = df.isna().sum()
    print(missing[missing > 0].sort_values(ascending=False))


if __name__ == "__main__":
    main()