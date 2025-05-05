import re
import os
import pandas as pd
from datetime import datetime

def write_tsv(data, column_list, path):
    """This function converts a nested dictionary to a TSV file with 3 columns."""
    rows = []
    for placename, months in data.items():
        for month, count in months.items():
            rows.append((placename, month, count))
    df = pd.DataFrame(rows, columns=column_list)
    df.to_csv(path, sep="\t", index=False)

# Open folder with Al Jazeera articles
folder = "../articles" 

# OPen gazetteer file
gazetteer_path = "../gazetteers/geonames_gaza_selection.tsv"

# Load the gazetteer
df = pd.read_csv(gazetteer_path, sep="\t")

# Build dictionary of compiled regex patterns
place_patterns = {}
for _, row in df.iterrows():
    all_names = [str(row['asciiname'])] + str(row.get('alternatenames', '')).split(',')
    name_pattern = '|'.join([re.escape(name.strip()) for name in all_names if name.strip()])
    if name_pattern:
        place_patterns[row['asciiname']] = re.compile(rf"\b({name_pattern})\b", re.IGNORECASE)

# Create a nested dictionary for place counts per month
mentions_per_month = {}

# Only count articles from the current war (Oct 7, 2023 onward)
start_date = datetime(2023, 10, 7)

for filename in os.listdir(folder):
    if not filename.endswith(".txt"):
        continue

    # Extract date from filename (format: YYYY-MM-DD_*)
    match = re.match(r"(\d{4}-\d{2}-\d{2})_", filename)
    if not match:
        continue

    file_date = datetime.strptime(match.group(1), "%Y-%m-%d")
    if file_date < start_date:
        continue

    # Load article text
    file_path = os.path.join(folder, filename)
    with open(file_path, encoding="utf-8") as f:
        text = f.read()

    # Get year-month string for grouping
    month_str = file_date.strftime("%Y-%m")

    # Search for place names
    for placename, regex in place_patterns.items():
        count = len(regex.findall(text))
        if count > 0:
            if placename not in mentions_per_month:
                mentions_per_month[placename] = {}
            if month_str not in mentions_per_month[placename]:
                mentions_per_month[placename][month_str] = 0
            mentions_per_month[placename][month_str] += count

# Print results for sanity check
for placename, months in mentions_per_month.items():
    for month, count in months.items():
        print(f"{placename} in {month}: {count} mentions")

# Write output to TSV file
columns = ["placename", "month", "count"]
output_path = "regex_counts.tsv"
write_tsv(mentions_per_month, columns, output_path)
