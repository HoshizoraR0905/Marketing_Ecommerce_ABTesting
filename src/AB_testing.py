from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

def main():
    # Read data from CSV
    df = pd.read_csv(PROCESSED_DATA_DIR / 'customer_campaign_analysis.csv')

    #check for each customer_id, experiment_group pair, is there a different in converted value?
    print("Converted value counts by customer and experiment group:")
    print(df.groupby(['customer_id', 'experiment_group', 'converted']).size().unstack(fill_value=0))
    
    print("Experiment group value counts:")
    print(df['experiment_group'].value_counts())
    
    # Preprocess data: handle missing values, duplicates, etc.
    #df = df.dropna()  # Remove rows with missing values
    #df = df.drop_duplicates()  # Remove duplicate rows

    # Additional preprocessing steps can be added here, e.g., encoding categorical variables, scaling numerical features
    


    #print(df.columns)  # Display column names for verification

if __name__ == "__main__":
    main()