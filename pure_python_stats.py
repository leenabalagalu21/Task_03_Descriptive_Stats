import csv
import json
import math
from collections import defaultdict, Counter
from typing import Any, Dict, List, Tuple


# File Paths 
FB_ADS_PATH = "/Users/leena/Downloads/2024_fb_ads_president_scored_anon.csv"
FB_POSTS_PATH = "/Users/leena/Downloads/2024_fb_posts_president_scored_anon.csv"
TW_POSTS_PATH = "/Users/leena/Downloads/2024_tw_posts_president_scored_anon.csv"


# Load CSV and return headers + row dictionaries
def load_csv(filepath: str) -> Tuple[List[str], List[Dict[str, Any]]]:
    with open(filepath, newline="", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        headers = [h.strip().lower() for h in reader.fieldnames]
        rows = [{h.strip().lower(): v for h, v in row.items()} for row in reader]
    return headers, rows

# Try to convert values to float, else keep them as strings
def try_float(v: str) -> Any:
    try:
        return float(v)
    except ValueError:
        return v.strip()

# Compute descriptive statistics for a column
def col_stats(values: List[Any]) -> Dict[str, Any]:
    nums = [x for x in values if isinstance(x, float)]
    cats = [x for x in values if not isinstance(x, float)]
    stats = {'count': len(values)}
    
    if nums:
        mean = sum(nums) / len(nums)
        stats.update(
            mean=mean,
            min=min(nums),
            max=max(nums),
            stddev=math.sqrt(sum((x - mean) ** 2 for x in nums) / (len(nums) - 1)) if len(nums) > 1 else 0.0,
        )
    if cats:
        counter = Counter(cats)
        top, freq = counter.most_common(1)[0]
        stats.update(unique=len(counter), most_common=top, most_common_count=freq)
    
    return stats

# Run col_stats for all columns
def analyse(headers: List[str], rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    columns = defaultdict(list)
    for row in rows:
        for h in headers:
            val = try_float(row[h])
            columns[h].append(val)
    return {col: col_stats(vals) for col, vals in columns.items()}

# Group rows by key(s)
def group_rows(rows: List[Dict[str, Any]], keys: List[str]) -> Dict[Tuple, List[Dict[str, Any]]]:
    g = defaultdict(list)
    for r in rows:
        try:
            key = tuple(r[k] for k in keys)
            g[key].append(r)
        except KeyError:
            continue
    return g

# Analyze each group separately
def analyse_groups(headers: List[str], rows: List[Dict[str, Any]], keys: List[str]) -> Dict:
    grouped = group_rows(rows, keys)
    return {k: analyse(headers, rs) for k, rs in grouped.items()}

# Print a few group-level stats for preview and collect limited output
def print_stats(title: str, stats_dict: Dict, max_groups: int = 3) -> Dict[str, Any]:
    print(f"\n--- {title} ---")
    limited_output = {}
    for i, (grp_key, col_stats_dict) in enumerate(stats_dict.items()):
        if i >= max_groups:
            break
        print(f"\nGroup: {grp_key}")
        for col, stats in col_stats_dict.items():
            print(f"  {col}")
            for k, v in stats.items():
                print(f"    {k:<18}: {v}")
        print("-" * 60)
        limited_output[str(grp_key)] = col_stats_dict
    return limited_output


def process_file(path: str, group_keys_1: List[str], group_keys_2: List[str], label: str) -> Dict[str, Any]:
    headers, rows = load_csv(path)
    
    # Overall stats for the full dataset
    overall = analyse(headers, rows)
    
    # Grouped summaries
    group1 = analyse_groups(headers, rows, group_keys_1)
    group2 = analyse_groups(headers, rows, group_keys_2)
    
    # Preview limited group stats
    sample_group1 = print_stats(f"{label} – Grouped by {group_keys_1}", group1)
    sample_group2 = print_stats(f"{label} – Grouped by {group_keys_2}", group2)

    return {
        "overall": overall,
        f"grouped_by_{'_'.join(group_keys_1)}": sample_group1,
        f"grouped_by_{'_'.join(group_keys_2)}": sample_group2,
    }

# main function

if __name__ == "__main__":
    result = {}

    # Facebook Ads
    result["fb_ads"] = process_file(
        FB_ADS_PATH,
        ["page_id"],
        ["page_id", "ad_id"],
        "Facebook Ads"
    )

    # Facebook Posts
    result["fb_posts"] = process_file(
        FB_POSTS_PATH,
        ["facebook_id"],
        ["facebook_id", "post_id"],
        "Facebook Posts"
    )

    # Twitter Posts
    result["tw_posts"] = process_file(
        TW_POSTS_PATH,
        ["twitter_handle"],
        ["twitter_handle", "post_id"],
        "Twitter Posts"
    )

    # Save final stats to JSON
    with open("python_stats_output.json", "w", encoding="utf-8") as jf:
        json.dump(result, jf, indent=2)

    print("\n Statistics saved to 'python_stats_output.json'")
