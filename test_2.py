import json

from find_races_1 import get_links
from results_scraper import get_results

races = {}

links, race_names, race_locations = get_links(only_results=True)
N = len(links)

for i in range(0,N):
    races = races = get_results(url = links[i], 
                                races = races, 
                                race_name=race_names[i], 
                                race_location=race_locations[i]
                                )

with open("horse_racing_odds.json", "w") as f:
    json.dump(races, f, indent=4)