# import requests

# API_KEY = "ac87703d784e00d7dcc5c4eccd1e275e"
# SPORT = "basketball_nba"  # Example sports key
# REGION = "au"              # Markets: us, uk, eu, au
# MARKETS = "h2h"            # h2h = Moneyline | spreads | totals

# url = "https://api.the-odds-api.com/v4/sports/{}/odds".format(SPORT)

# params = {
#     "apiKey": API_KEY,
#     "regions": REGION,
#     "markets": MARKETS,
#     "oddsFormat": "american"  # american or decimal
# }

# response = requests.get(url, params=params)
# data = response.json()

# print(data)