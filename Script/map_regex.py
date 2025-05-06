import pandas as pd
import plotly.express as px

# Load data
counts = pd.read_csv("regex_counts.tsv", sep="\t")
coords = pd.read_csv("ner_gazetteer.tsv", sep="\t")

# Check column names and adjust if needed
print("Counts columns:", counts.columns)
print("Coords columns:", coords.columns)

# Merge on place name
merged = pd.merge(counts, coords, on="name", how="inner")

# Create the animated map
fig = px.scatter_geo(
    merged,
    lat="latitude",
    lon="longitude",
    size="count",
    color="name",
    hover_name="name",
    animation_frame="month",
    projection="natural earth",
    title="Regex-Extracted Place Names Over Time"
)

# Save the interactive map as HTML
fig.write_html("regex_map.html")

# Save the map as PNG (requires kaleido)
fig.write_image("regex_map.png", scale=2)

# Show the map in browser
fig.show()
