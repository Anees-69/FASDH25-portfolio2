import pandas as pd
import plotly.express as px

#
counts_df = pd.read_csv("ner_counts.tsv", sep="\t")
gazetteer_df = pd.read_csv("NER_gazetteer.tsv", sep="\t")
