from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

def main():
    # Read data from CSV
    events = pd.read_csv(RAW_DATA_DIR / 'events.csv')

    events["converted"] = (events["event_type"] == 'purchase').astype(int)

    #check if for each session_id, there is at most one 'experiment_group' value. 
    #if events.groupby('session_id')['experiment_group'].nunique().max() > 1:
    #    raise ValueError("Each session_id should have at most one 'experiment_group' value.")
    
    #print(events.groupby("session_id")["experiment_group"]
    #.unique()
    #.reset_index().head(10))

    #Define `converted` using `event_type` = `purchase` for each distinct pair of `session_id`, `experiment_group`. 
    events = events.groupby(['session_id']).agg(
        experiment_group=('experiment_group', 'first'),
        converted=('converted', 'max')
    ).reset_index()

    events = events.groupby(['experiment_group']).agg(
        total_events=('converted', 'count'),
        total_conversions=('converted', 'sum')
    ).reset_index().rename(columns={'total_events': 'n', 'total_conversions': 'conversions'})
    #save as csv in the processed data folder
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DATA_DIR / "AB_events_transactions_match_by_timestamp.csv"
    events.to_csv(output_path, index=False)

if __name__ == "__main__":
    main()