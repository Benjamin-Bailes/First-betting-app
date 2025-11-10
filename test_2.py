import json
from datetime import date

from find_races_1 import get_links
from results_scraper import get_results


# home_page = "https://www.sportsbet.com.au/racing-schedule/results/2025-11-09"
# date = "9-11-2025"
home_page = "https://www.sportsbet.com.au/racing-schedule/horse/today"
date = str(date.today().strftime("%d-%m-%Y"))


races = {}

links, race_names, race_locations = get_links(url = home_page, only_results=True)
N = len(links)

for i in range(0,N):
    races = get_results(url = links[i], 
                        races = races, 
                        race_name=race_names[i], 
                        race_location=race_locations[i],
                        date = date
                        )

file_name = "horse_racing_odds_" + date + ".json"
with open(file_name, "w") as f:
    json.dump(races, f, indent=4)