from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data"

def inspect_csv(file_path: Path) -> None:
    print("=" * 80)
    print(f"File: {file_path.name}")
    print("=" * 80)

    df = pd.read_csv(file_path)

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if missing.empty:
        print("No missing values.")
    else:
        print(missing)

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\n")


def main():
    csv_files = list(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        print(f"No CSV files found in {RAW_DATA_DIR}")
        return

    for file_path in csv_files:
        inspect_csv(file_path)


if __name__ == "__main__":
    main()