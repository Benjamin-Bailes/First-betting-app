import json
import csv

JSON_filename = "horse_racing_odds_10-11-2025.json" # File that will be converted
CSV_filename = "all_horse_data.csv" # Export filename


with open(JSON_filename, "r", encoding="utf-8") as f:
    my_JSON = json.load(f)
if not my_JSON:
  print("Error, incorrect file provided")
  exit

# CSV heading
data = [["horse_name", "win_odds", "place_odds", "position", "race", "date"]]

# Keep track of race names as to not overlap. ie, we want to have flemington 1, flemignton 2, so that we can distiguish
race_names = []



# Get horses only, turns out there are doggies in here somehow
substring = "https://www.sportsbet.com.au/horse-racing/"
horsey_data = {k: v for k, v in my_JSON.items() if substring in k}


for url_KEY, stats_VALUE in horsey_data.items():
    race_name = str(stats_VALUE["race name"])
    # Make sure each race has a different name
    i = 1
    temp = race_name + " " + str(i)
    while temp in race_names:
        i = i + 1
        temp = race_name + " " + str(i)

    race_name = temp
    race_names.append(race_name)
    
    date =  stats_VALUE["date"]

    for horse in stats_VALUE["horses"]:
        horse_name = str(horse["name"])
        win_odds = horse["win odds"]
        place_odds = horse["place odds"]
        position = horse["position"]
        

        if position == None:
            position = 10 # Did not place

        if horse_name and win_odds and place_odds and position:
            new_row = [horse_name, win_odds, place_odds, position, race_name, date]
            data.append(new_row)





# Export. "a" for append
with open(CSV_filename, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(data)

# with open("/Users/benjaminbailes/Documents/UNI/2025 SEM 2/Comp Bayes/horses_testing/all_horse_data.csv", "a", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerows(data)



