import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import json



def get_results(url = "https://www.sportsbet.com.au/horse-racing/australia-nz/flemington/race-1-9810572", 
                races = None, 
                race_name="Flemingggggton",
                race_location="Viccctoria",
                date = "00/00/0000"):
        
        # JSON
        if races is None:
            races = {}
        race_id = url
        races[race_id] = {
            "race name": race_name,
            "race location": race_location,
            "date": date,
            "horses": [
            ]
        }


        # Get the Soup
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
        else:
            print(f"Error: Status code {response.status_code}")
        soup = BeautifulSoup(html, "html.parser")

        # 1) Find the race card container
        racecard = soup.select_one('div[data-automation-id="racecard-body"]') or soup

        rows = []
        # 2) For each horse on the racecard
        for card in racecard.select('div[data-automation-id^="racecard-outcome-"]'): #.outcomeCard_f7jc198
            # Horse name
            name_el = card.select_one('[data-automation-id="racecard-outcome-name"]')
            if not name_el:
                continue
            raw = name_el.get_text(" ", strip=True)              # e.g. "1. Storm Runner (1)"
            name = re.sub(r'^\s*\d+\.\s*', '', raw)              # drop leading "1. "
            name = re.sub(r'\s+\(\d+\)\s*$', '', name)           # drop trailing draw "(1)"
            
            # We look through all elements in correct div util we find the data we want   
            # Odds: look for the first numeric odds value on the card
            win_odds = None
            for el in card.select('[data-automation-id="racecard-outcome-0-L-price"]'): #span[data-automation-id$="-odds-button-text"]
                t = el.get_text(strip=True)
                # check if decimals or simple fractions to be accpeted
                if re.fullmatch(r'\d+(?:\.\d+)?(?:/\d+)?', t):
                    win_odds = float(t)
                    break   
            place_odds = None
            for el in card.select('[data-automation-id="racecard-outcome-1-L-price"]'):
                t = el.get_text(strip=True)
                if re.fullmatch(r'\d+(?:\.\d+)?(?:/\d+)?', t):
                    place_odds = float(t)
                    break

            # TO FUCKING HARD   
            # price_flucs = []
            # t = card.select_one('[data-automation-id="racecard-price-fluc-0"]')
            # print(t)
            # # for ell in card.select('[class="containerRowDesktopNotFutures_flckaih"][data-automation-id="racecard-price-flucs"]'):
            # #     print('hi')
            # #     t = ell.get_text(strip=True)
            # #     print(repr(ell.get_text(strip=True)))
            # #     if re.fullmatch(r'\d+(?:\.\d+)?(?:/\d+)?', t):
            # #         price_flucs.append(float(t))
            # #         break
            

            if name:
                races[race_id]["horses"].append({
                    "name": name,
                    "win odds": win_odds,
                    "place odds": place_odds,
                    "position": None
                })
            # if win_odds:
            #     races[race_id]["horses"].append({
            #         "win odds": win_odds,
            #     })
            # if place_odds:
            #     races[race_id]["horses"].append({
            #         "place odds": place_odds,
            #     })
                



        # Assign horses their postions because for some reason they are in a different fucking div
        resultscard = soup.select_one('div[data-automation-id="racecard-frame"]') or soup
        resultscard = resultscard.select_one('div[class^="container_"]')
            
        # First, Second, Thrid, Fourth
        for el in resultscard.select('[class^="resultContainerRowWithBottomMargin_"]'):
            position = None
            pos_el = el.select_one('[data-automation-id="racecard-podium-ordinal"]')
            if pos_el:
                position = pos_el.get_text()
                position = int(position[:-2]) # remove st,nd,rd,th

            name2 = None
            name_el = el.select_one('[data-automation-id="racecard-outcome-name"]')
            if name_el:
                name2 = name_el.get_text()
                name2 = re.sub(r'^\s*\d+\.\s*', '', name2)
                name2 = re.sub(r'\s+\(\d+\)\s*$', '', name2) 


            # Update JSON with position
            if name2 and position:
                for horse in races[race_id]["horses"]:           
                    if horse.get("name") == name2:
                        horse["position"] =  position                 
                        break


        # OTHER POSITIONS ARE HIDDEN BEHIND AN ACCORDIAN, HTML DOESNT SHOW UNTIL PRESSED ON
        #  
        # resultscard = resultscard.select_one('div[class^="fullFieldAccordion_"]')  
        # for el in resultscard.select('[class="resultContainerRow_f1issel"]'):
        #     pos_el = el.select_one('[data-automation-id="racecard-podium-ordinal"]')
        #     print(1)
        #     if pos_el:
        #       t = pos_el.get_text()
        #       t = int(t[:-2]) # remove st,nd,rd,th
        #       print(t)
            

        #     name_el = el.select_one('[data-automation-id="racecard-outcome-name"]')
        #     if pos_el:
        #       t = name_el.get_text()
        #       t = re.sub(r'^\s*\d+\.\s*', '', t)
        #       t = re.sub(r'\s+\(\d+\)\s*$', '', t) 
        #       print(t)

        
        # # # Export JSON
        # with open("horse_racing_odds.json", "w") as f:
        #     json.dump(races, f, indent=4)
        
        return races






