import os, shutil
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up global visualization style
plt.rcParams["figure.dpi"] = 120
sns.set_style("whitegrid")

# File Paths – Update these for your local setup
FB_ADS_PATH   = r"C:\Users\leena\Downloads\2024_fb_ads_president_scored_anon.csv"
FB_POSTS_PATH = r"C:\Users\leena\Downloads\2024_fb_posts_president_scored_anon.csv"
TW_POSTS_PATH = r"C:\Users\leena\Downloads\2024_tw_posts_president_scored_anon.csv"


# Datasets and columns to visualize
DATASETS = {
    "fb_ads": (
        FB_ADS_PATH,
        ["estimated_spend", "estimated_impressions"],      # Numeric columns
        ["publisher_platforms", "currency"]                # Categorical columns
    ),
    "fb_posts": (
        FB_POSTS_PATH,
        ["Likes", "Overperforming Score"],
        ["Type", "Page Category"]
    ),
    "tw_posts": (
        TW_POSTS_PATH,
        ["likeCount", "retweetCount"],
        ["lang", "source"]
    ),
}


# Check if a series has usable data (not all NaNs or identical values)
def has_data(s):
    s = s.dropna()
    return len(s) > 0 and s.nunique() > 1

# Create a bar chart of top N most frequent values
def bar_top(ax, series, n=10, title=""):
    counts = series.value_counts().head(n)
    sns.barplot(x=counts.values, y=counts.index, ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Count")
    ax.set_ylabel("")

# Histogram with outlier clipping at 99th percentile
def plot_histogram(series, title, out_file):
    data = series.dropna()
    if len(data) == 0 or data.nunique() < 2:
        return
    upper_limit = data.quantile(0.99)
    clipped_data = data[data <= upper_limit]
    plt.figure()
    sns.histplot(clipped_data, bins=50)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_file)
    plt.close()


# Main Loop: Create plots for each dataset
BASE = "figures"
os.makedirs(BASE, exist_ok=True)

for name, (path, num_cols, cat_cols) in DATASETS.items():
    df = pd.read_csv(path)

    out_dir = os.path.join(BASE, name)
    shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(out_dir, exist_ok=True)

    # Numeric Column 1 – Histogram
    if has_data(df[num_cols[0]]):
        plot_histogram(
            df[num_cols[0]],
            f"{num_cols[0]} distribution",
            os.path.join(out_dir, f"{num_cols[0]}_hist.png")
        )

    # Numeric Column 2 – Boxplot
    if has_data(df[num_cols[1]]):
        plt.figure()
        sns.boxplot(x=df[num_cols[1]].dropna())
        plt.title(f"{num_cols[1]} boxplot")
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"{num_cols[1]}_box.png"))
        plt.close()

    # Categorical Column 1 – Top 10 Bar Chart
    if has_data(df[cat_cols[0]]):
        plt.figure()
        bar_top(plt.gca(), df[cat_cols[0]].dropna(), 10, f"Top 10 {cat_cols[0]}")
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"{cat_cols[0]}_bar.png"))
        plt.close()

    # Categorical Column 2 – Top 10 Bar Chart
    if has_data(df[cat_cols[1]]):
        plt.figure()
        bar_top(plt.gca(), df[cat_cols[1]].dropna(), 10, f"Top 10 {cat_cols[1]}")
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"{cat_cols[1]}_bar.png"))
        plt.close()

    print(f" Plots stored in figures/{name}")

print("\n All plots generated and saved.")