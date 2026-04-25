from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

def main():
    customers = pd.read_csv(RAW_DATA_DIR / "customers.csv")
    events = pd.read_csv(RAW_DATA_DIR / "events.csv")
    transactions = pd.read_csv(RAW_DATA_DIR / "transactions.csv")
    campaigns = pd.read_csv(RAW_DATA_DIR / "campaigns.csv")

    events["timestamp"] = pd.to_datetime(events["timestamp"])
    transactions["timestamp"] = pd.to_datetime(transactions["timestamp"])

    # Ignore campaign_id = 0 for campaign-level analysis
    campaign_events = events[events["campaign_id"] != 0].copy()

    # Aggregate event behavior by customer-campaign
    event_agg = (
        campaign_events
        .groupby(["customer_id", "campaign_id"])
        .agg(
            first_event_time=("timestamp", "min"),
            last_event_time=("timestamp", "max"),
            total_events=("event_id", "count"),
            unique_sessions=("session_id", "nunique"),
            avg_session_duration=("session_duration_sec", "mean"),
            experiment_group=("experiment_group", lambda x: x.mode().iloc[0])
        )
        .reset_index()
    )

    event_type_counts = (
        campaign_events
        .pivot_table(
            index=["customer_id", "campaign_id"],
            columns="event_type",
            values="event_id",
            aggfunc="count",
            fill_value=0
        )
        .add_prefix("event_")
        .reset_index()
    )

    #print(event_agg.head(5), event_type_counts.head(5))

    event_agg = event_agg.merge(event_type_counts, on = ['customer_id', 'campaign_id'], how = 'left')

    transactions = transactions.dropna(subset=["product_id", "gross_revenue"])
    campaign_transactions = transactions[transactions["campaign_id"] != 0].copy()

    tx_agg = (
        campaign_transactions
        .groupby(["customer_id", "campaign_id"])
        .agg(
            num_transactions=("transaction_id", "count"),
            total_revenue=("gross_revenue", "sum"),
            avg_order_value=("gross_revenue", "mean"),
            avg_discount=("discount_applied", "mean"),
            num_refunds=("refund_flag", "sum")
        )
        .reset_index()
    )

    # Merge features and outcomes
    df = event_agg.merge(
        tx_agg,
        on=["customer_id", "campaign_id"],
        how="left"
    )

    # Fill no-transaction outcomes
    outcome_cols = [
        "num_transactions",
        "total_revenue",
        "avg_order_value",
        "avg_discount",
        "num_refunds"
    ]

    for col in outcome_cols:
        df[col] = df[col].fillna(0)

    df["converted"] = (df["num_transactions"] > 0).astype(int)

    # Add campaign metadata
    df = df.merge(campaigns, on="campaign_id", how="left")

    # Add customer attributes
    df = df.merge(customers, on="customer_id", how="left")

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DATA_DIR / "customer_campaign_analysis.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")
    print("Shape:", df.shape)
    print(df.head())


if __name__ == "__main__":
    main()