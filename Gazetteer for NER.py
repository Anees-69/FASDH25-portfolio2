import pandas as pd

ner_df = pd.read_csv("ner_counts.tsv", sep="\t")
placenames = ner_df["placename"].tolist()


from geopy.geocoders import Nominatim
from time import sleep

geolocator = Nominatim(user_agent="geoapiExercises")
place_coords = []

for place in placenames:
    try:
        location = geolocator.geocode(place)
        if location:
            lat = location.latitude
            lon = location.longitude
        else:
            lat = "NA"
            lon = "NA"
    except:
        lat = "NA"
        lon = "NA"
    
    place_coords.append((place, lat, lon))
    sleep(1)  # Be polite to the geocoding API

output_df = pd.DataFrame(place_coords, columns=["placename", "latitude", "longitude"])
output_df.to_csv("gazetteers/NER_gazetteer.tsv", sep="\t", index=False)
