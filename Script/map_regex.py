import pandas as pd
import plotly.express as px

# Load data
counts = pd.read_csv("regex_counts.tsv", sep="\t")
coords = pd.read_csv("geonames_gaza_selection.tsv", sep="\t")

# Clean column names
counts.columns = counts.columns.str.strip()
coords.columns = coords.columns.str.strip()

# Rename for consistency
coords = coords.rename(columns={
    "asciiname": "placename",
    "latitude": "latitude",
    "longitude": "longitude"
})

# Merge
data = pd.merge(counts, coords, on="placename")

# Clean numeric values
data["count"] = pd.to_numeric(data["count"], errors="coerce")
data = data.dropna(subset=["count", "latitude", "longitude"])

# Create animated map using the new scatter_map (MapLibre backend)
fig = px.scatter_map(
    data,
    lat="latitude",
    lon="longitude",
    hover_name="placename",
    size="count",
    animation_frame="month",
    color="count",
    color_continuous_scale=px.colors.sequential.YlOrRd,
    title="Regex-Extracted Place Map",
    zoom=4,
    height=600
)

fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})

# Save outputs
fig.write_html("regex_map.html")

# Save the static image (requires kaleido)
try:
    fig.write_image("regex_map.png", engine="kaleido")
    print("regex_map.png successfully saved.")
except Exception as e:
    print(f"Error saving regex_map.png: {e}")

# Show the map
fig.show()
