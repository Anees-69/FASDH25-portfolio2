import pandas as pd
import plotly.express as px

# Load the Data
counts_df = pd.read_csv("ner_counts.tsv", sep="\t")
gazetteer_df = pd.read_csv("NER_gazetteer.tsv", sep="\t")

# Combine the frequency and coordinates into one DataFrame
merged_df = pd.merge(counts_df, gazetteer_df, left_on="name", right_on="placename", how="left")

# Drop missing coordinates and convert lat/lon to numeric
merged_df = merged_df[merged_df["latitude"] != "NA"]
merged_df["latitude"] = pd.to_numeric(merged_df["latitude"])
merged_df["longitude"] = pd.to_numeric(merged_df["longitude"])

# Drop any rows with missing data in key columns
merged_df = merged_df.dropna(subset=["latitude", "longitude", "frequency"])

# Create and save the map as HTML and PNG
fig = px.scatter_geo(
    merged_df,
    lat="latitude",
    lon="longitude",
    text="name",
    size="frequency",
    color="frequency"
    height=600
    color_continuous_scale=px.colors.sequential.Y10rRd,
    projection="natural earth",
    title="NER-extracted Placename Mentions in January 2024"
)

fig.write_html("ner_map.html")
fig.write_image("ner_map.png")
