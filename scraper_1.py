import requests

url = "https://www.sportsbet.com.au/horse-racing/international/fontainebleau/race-2-9811886"   # Replace with the site you want to fetch

# Begin at homepage.


response = requests.get(url)
if response.status_code == 200:
    html = response.text
    # Save to a file
    # with open("page.html", "w", encoding="utf-8") as file:
    #     file.write(html)
    # print("HTML saved to page.html")
else:
    print(f"Error: Status code {response.status_code}")




# ----- scrape ------


from bs4 import BeautifulSoup
import re
import pandas as pd


import json
races = {}
races["race_1"] = {
    # "time": "14:30",
    "horses": [
    ]
}

# Open the saved HTML file
# with open("page.html", "r", encoding="utf-8", errors="ignore") as f:
#     soup = BeautifulSoup(f.read(), "html.parser")

soup = BeautifulSoup(html, "html.parser")
# 1) Find the race card container
racecard = soup.select_one('div[data-automation-id="racecard-body"]') or soup

rows = []
# 2) For each runner/outcome on the card…
for card in racecard.select('div[data-automation-id^="racecard-outcome-"].outcomeCard_f7jc198'):
    # Horse name
    name_el = card.select_one('[data-automation-id="racecard-outcome-name"]')
    if not name_el:
        continue
    raw = name_el.get_text(" ", strip=True)              # e.g. "1. Storm Runner (1)"
    name = re.sub(r'^\s*\d+\.\s*', '', raw)              # drop leading "1. "
    name = re.sub(r'\s+\(\d+\)\s*$', '', name)           # drop trailing draw "(1)"
    
    # Odds: look for the first numeric odds value on the card (ignore "EW")
    odds = None
    for span in card.select('span[data-automation-id$="-odds-button-text"]'):
        t = span.get_text(strip=True)
        # Accept decimals or simple fractions (e.g., 11/4)
        if re.fullmatch(r'\d+(?:\.\d+)?(?:/\d+)?', t):
            odds = t
            break
    
    if name and odds:
        # rows.append({"Name": name, "Odds": odds})
        races["race_1"]["horses"].append({
            "name": name,
            "odds": odds
    })
        


# Use the data
# df = pd.DataFrame(rows)
# print(df)
# Optionally save:
# df.to_csv("race1_odds.csv", index=False)



# Export JSON
with open("horse_racing_odds.json", "w") as f:
    json.dump(races, f, indent=4)

