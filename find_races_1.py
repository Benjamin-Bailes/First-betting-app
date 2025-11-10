import requests 

from bs4 import BeautifulSoup
import re
import pandas as pd



def get_links(only_results = True, url = "https://www.sportsbet.com.au/racing-schedule/horse/today"):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
    else:
        print(f"Error: Status code {response.status_code}")


    # Should all have the same index, cbf making it into one array with 3 cols
    links = []
    race_names = []
    race_locations = []


    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("tbody tr")
    
    for row in rows:
        # Get names and locations of each race, each row has the same
        race_name_el = row.select_one('td[data-automation-id*="-meeting-cell"]')
        t = race_name_el.get_text(",")
        race_name, race_location = t.split(",", 1) # Split based on comma                     

        # Get links - VERY INEFFICIENT ATM, Searching for NOT, maybe if I changed the logic it would be better.
        if only_results:
            # event_cells are the small little boxes in each row
            event_cells = row.find_all("td", attrs={
                "data-automation-id": lambda v: v and "event-cell" in v,
                "class": lambda c: (
                    c                                               # class exists
                    and (                                          # AND
                        isinstance(c, str) and not c.startswith("notResultedEventCell")   # string case
                        or isinstance(c, list) and not any(cls.startswith("notResultedEventCell") for cls in c)  # list case
                    )
                )
            })
        else:
            event_cells = row.find_all("td", attrs={
                "data-automation-id": lambda v: v and "event-cell" in v
            })


        
        for cell in event_cells:
            link_tag = cell.find("a")    # find the <a> link inside this cell
            if link_tag and link_tag.get("href"): 
                # print(cell.get("class"), link_tag["href"]) # Debug
                links.append("https://www.sportsbet.com.au" + link_tag["href"])
                
                if race_name and race_location:
                    race_names.append(race_name)
                    race_locations.append(race_location)



    # links = [
    # a["href"]
    # for a in soup.select(
    #     'tbody tr td[data-automation-id*="event-cell"]:not([class*="notResultedEventCell"]):not([data-automation-id*="notResultedEventCell"]) a[href]'
    # )
    # ]


    return links, race_names, race_locations



