from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

def main():
    # Read data from CSV
    events = pd.read_csv(RAW_DATA_DIR / 'events.csv')
    transactions = pd.read_csv(RAW_DATA_DIR / 'transactions.csv')
    tx = transactions.fillna({'gross_revenue': 0, 'product_id': 'unknown'})

    # Merge events and transactions on:
    #  customer_id, and timestamp of event and transaction are within a reasonable time window (e.g., 1 day after the event)
    # to create a combined dataset
    events["timestamp"] = pd.to_datetime(events["timestamp"])
    transactions["timestamp"] = pd.to_datetime(transactions["timestamp"])

    combined = pd.merge_asof(
        events.sort_values("timestamp"),
        transactions.sort_values("timestamp"),
        on="timestamp",
        by="customer_id",
        direction="backward",
        tolerance=pd.Timedelta("2D")
    )

    combined["converted"] = (combined["gross_revenue"] > 0).astype(int)
    combined = combined[['experiment_group', 'converted']].groupby('experiment_group').agg(
        total_events=('converted', 'count'),
        total_conversions=('converted', 'sum')
    ).reset_index().rename(columns={'total_events': 'n', 'total_conversions': 'conversions'})
    #save as csv in the processed data folder
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DATA_DIR / "AB_events_transactions_match_by_timestamp.csv"
    combined.to_csv(output_path, index=False)

if __name__ == "__main__":
    main()