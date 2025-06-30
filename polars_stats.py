import polars as pl
import json


# Analyze a single column for stats (numeric or categorical)
def analyze_column(df: pl.DataFrame, col: str) -> dict:
    series = df[col].drop_nulls()
    result = {"count": series.len()}

    # Try numeric stats first
    try:
        mean = series.mean()
        if mean is not None:
            result.update({
                "mean": float(mean),
                "stddev": float(series.std()),
                "min": float(series.min()),
                "max": float(series.max())
            })
            return result
    except:
        pass  # If numeric conversion fails, try as categorical

    # If not numeric, treat as categorical
    result["unique"] = series.n_unique()
    try:
        vc_df = series.value_counts().sort(by="counts", descending=True)
        result["most_common"] = str(vc_df[0, col])
        result["most_common_count"] = int(vc_df[0, "counts"])
    except:
        pass  # If value_counts fails

    return result


# Print stats for a column in readable format
def print_column_stats(col: str, stats: dict):
    print(f"\nColumn: {col}")
    for k in ["count", "mean", "stddev", "min", "max", "unique", "most_common", "most_common_count"]:
        if k in stats:
            print(f"{k:<24}: {stats[k]}")
    print("-" * 60)


# Load CSV and analyze each column in a dataset
def load_and_analyze(filepath: str, label: str) -> dict:
    print(f"\n=== Analyzing: {label} ===")
    df = pl.read_csv(filepath)
    result = {}

    for col in df.columns:
        if df[col].drop_nulls().len() == 0:
            continue  # Skip columns that are entirely null
        stats = analyze_column(df, col)
        print_column_stats(col, stats)
        result[col] = stats

    return result


# Main script: analyze 3 datasets and save results to JSON
if __name__ == "__main__":
    result = {}

    # Facebook Ads dataset
    result["fb_ads"] = load_and_analyze(
        r"C:\Users\leena\Downloads\2024_fb_ads_president_scored_anon.csv",
        "Facebook Ads"
    )

    # Facebook Posts dataset
    result["fb_posts"] = load_and_analyze(
        r"C:\Users\leena\Downloads\2024_fb_posts_president_scored_anon.csv",
        "Facebook Posts"
    )

    # Twitter Posts dataset
    result["tw_posts"] = load_and_analyze(
        r"C:\Users\leena\Downloads\2024_tw_posts_president_scored_anon.csv",
        "Twitter Posts"
    )

    # Save all results to a JSON file
    with open("polars_stats_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=str)

    print("\n Statistics saved to 'polars_stats_output.json'")
