import pandas as pd
import json


# Function to compute summary stats for all columns
def analyze_with_pandas(df: pd.DataFrame) -> dict:
    summary = {}

    # Describe includes both numeric and object/categorical columns
    describe_all = df.describe(include='all').T

    for col in df.columns:
        col_summary = {}

        # Add standard describe statistics
        if col in describe_all.index:
            desc = describe_all.loc[col]
            col_summary["count"] = int(desc.get("count", 0))
            if "mean" in desc:
                col_summary["mean"] = desc["mean"]
            if "std" in desc:
                col_summary["stddev"] = desc["std"]
            if "min" in desc:
                col_summary["min"] = desc["min"]
            if "max" in desc:
                col_summary["max"] = desc["max"]

        # Handle categorical or object-type columns separately
        if df[col].dtype == object or df[col].dtype.name == "category":
            value_counts = df[col].value_counts(dropna=True)
            if not value_counts.empty:
                col_summary["unique"] = int(df[col].nunique(dropna=True))
                col_summary["most_common"] = value_counts.idxmax()
                col_summary["most_common_count"] = int(value_counts.max())

        summary[col] = col_summary

    return summary


# Load CSV and generate stats for a single file
def load_and_analyze(filepath: str, label: str) -> dict:
    print(f"\n=== Analyzing: {label} ===")
    df = pd.read_csv(filepath, encoding="utf-8")
    stats = analyze_with_pandas(df)

    # Print results in a readable format
    for col, col_stats in stats.items():
        print(f"\nColumn: {col}")
        for k, v in col_stats.items():
            print(f"  {k:<20}: {v}")
        print("-" * 50)

    return stats

# Main function
if __name__ == "__main__":
    result = {}

    # Load and analyze Facebook Ads
    result["fb_ads"] = load_and_analyze(
        r"C:\Users\leena\Downloads\2024_fb_ads_president_scored_anon.csv",
        "Facebook Ads"
    )

    # Load and analyze Facebook Posts
    result["fb_posts"] = load_and_analyze(
        r"C:\Users\leena\Downloads\2024_fb_posts_president_scored_anon.csv",
        "Facebook Posts"
    )

    # Load and analyze Twitter Posts
    result["tw_posts"] = load_and_analyze(
        r"C:\Users\leena\Downloads\2024_tw_posts_president_scored_anon.csv",
        "Twitter Posts"
    )

    # Helper to serialize complex types to JSON-safe format
    def serialize(data):
        if isinstance(data, dict):
            return {k: serialize(v) for k, v in data.items()}
        elif isinstance(data, pd.Series):
            return data.to_dict()
        elif isinstance(data, pd.DataFrame):
            return data.to_dict(orient="records")
        elif isinstance(data, pd.Timestamp):
            return str(data)
        else:
            return data

    # Save all summary stats to a JSON file
    with open("pandas_stats_output.json", "w", encoding="utf-8") as f:
        json.dump(serialize(result), f, indent=2)

    print("\n Statistics saved to 'pandas_stats_output.json'")
