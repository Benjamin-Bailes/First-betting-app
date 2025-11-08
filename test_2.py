import json

from find_races_1 import get_links
from results_scraper import get_results

races = {}

links = get_links(only_results=True)

# i = 1
# for link in links:
#     # print(link)
#     races = get_results(link, races, race_name=i)
#     i = i + 1
#     print(1)


print(links[0])
races = get_results(url = links[0], races = races)
# races = get_results(races = races)

with open("horse_racing_odds.json", "w") as f:
    json.dump(races, f, indent=4)