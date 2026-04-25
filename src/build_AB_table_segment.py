import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def main():
    # Read data from CSV
    events = pd.read_csv(RAW_DATA_DIR / 'events.csv')
    customers = pd.read_csv(RAW_DATA_DIR / 'customers.csv')

    events["converted"] = (events["event_type"] == 'purchase').astype(int)

    #Define `converted` using `event_type` = `purchase` for each distinct pair of `session_id`, `experiment_group`. 

    #check if for each session_id, there is at most one 'customer_id' value. 
    #if events.groupby('session_id')['customer_id'].nunique().max() > 1:
    #    raise ValueError("Each session_id should have at most one 'customer_id' value.")

        # One row = one session
    session_df = (
        events.groupby(["session_id", "customer_id"])
        .agg(
            experiment_group=("experiment_group", "first"),
            converted=("converted", "max"),
        )
        .reset_index()
    )

    # Add customer attributes
    session_df = session_df.merge(
        customers[
            [
                "customer_id",
                "loyalty_tier",
                "acquisition_channel",
                "country",
                "age",
                "gender",
            ]
        ],
        on="customer_id",
        how="left",
    )

    # Overall conversion rate by loyalty tier
    loyalty_summary = (
        session_df.groupby("loyalty_tier")
        .agg(
            n=("converted", "count"),
            conversions=("converted", "sum"),
            conversion_rate=("converted", "mean"),
        )
        .reset_index()
        .sort_values("conversion_rate", ascending=False)
    )

    # Overall conversion rate by acquisition channel
    acquisition_summary = (
        session_df.groupby("acquisition_channel")
        .agg(
            n=("converted", "count"),
            conversions=("converted", "sum"),
            conversion_rate=("converted", "mean"),
        )
        .reset_index()
        .sort_values("conversion_rate", ascending=False)
    )

    # Conversion rate by loyalty tier and experiment group
    loyalty_by_group = (
        session_df.groupby(["loyalty_tier", "experiment_group"])
        .agg(
            n=("converted", "count"),
            conversions=("converted", "sum"),
            conversion_rate=("converted", "mean"),
        )
        .reset_index()
        .sort_values(["loyalty_tier", "experiment_group"])
    )

    # Conversion rate by acquisition channel and experiment group
    acquisition_by_group = (
        session_df.groupby(["acquisition_channel", "experiment_group"])
        .agg(
            n=("converted", "count"),
            conversions=("converted", "sum"),
            conversion_rate=("converted", "mean"),
        )
        .reset_index()
        .sort_values(["acquisition_channel", "experiment_group"])
    )

    # Save results
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    session_df.to_csv(
        PROCESSED_DATA_DIR / "session_customer_conversion_table.csv",
        index=False,
    )

    loyalty_summary.to_csv(
        PROCESSED_DATA_DIR / "conversion_by_loyalty_tier.csv",
        index=False,
    )

    acquisition_summary.to_csv(
        PROCESSED_DATA_DIR / "conversion_by_acquisition_channel.csv",
        index=False,
    )

    loyalty_by_group.to_csv(
        PROCESSED_DATA_DIR / "conversion_by_loyalty_and_experiment_group.csv",
        index=False,
    )

    acquisition_by_group.to_csv(
        PROCESSED_DATA_DIR / "conversion_by_acquisition_and_experiment_group.csv",
        index=False,
    )

    print("\nConversion by loyalty tier:")
    print(loyalty_summary.to_string(index=False))

    print("\nConversion by acquisition channel:")
    print(acquisition_summary.to_string(index=False))

    print("\nConversion by loyalty tier and experiment group:")
    print(loyalty_by_group.to_string(index=False))

    print("\nConversion by acquisition channel and experiment group:")
    print(acquisition_by_group.to_string(index=False))

if __name__ == "__main__":
    main()