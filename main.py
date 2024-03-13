import requests
import json
from datetime import datetime, timedelta, timezone
import sports

sports = sports.sports_keys
base_url = 'https://api.the-odds-api.com/v4/sports/'
now = datetime.now(timezone.utc)
week_start = now
week_end = now + timedelta(days=7)
markets = ['h2h', 'totals']
key_counter = 0
api_key_list = ["8014cca5d68ccacc087b00e54828e849", "baf0e52de498993d4c820e644423443f", "7f18f002d1a3018115f2331cfed80f17", "93e76e385d8e2c73032779c41eefc92c" ,"a7798ac707f30384bc40eb426f2346d7", "f1fdc1f247ddacb2f14e2d17ca2fef91", "b90b1b2999fa25fc353132f8f86d8d1b","7c8339f73243b1522986717d10848c1d", "2acb1bc7fa18d9fddfc75acc1397cff8","ccae58c1e160f0d2c74eb48a8720c271", "4ce351a64bac4e3c93da7acb927cf082", "418a07372522e9addfd3e17319f793df"]
offshore_books = ['BetUS', 'Bovada']
def get_current_key():
    return api_key_list[key_counter]

def get_arbitrage_bets():
    profitable_bets = []
    global key_counter

    for sport in sports:
        for market in markets:
            url = f"{base_url}{sport}/odds/?regions=us&markets={market}&oddsFormat=decimal&apiKey={api_key_list[key_counter]}"
            response = requests.get(url)

            if response.status_code == 200:
                matches = json.loads(response.text)

                next_week_matches = [match for match in matches if week_start <= datetime.fromisoformat(
                    match['commence_time'].replace("Z", "+00:00")) < week_end]

                for match in next_week_matches:
                    highest_odds = {}

                    for bookmaker in match['bookmakers']:
                        for market in bookmaker['markets']:
                            for outcome in market['outcomes']:
                                if outcome['name'] not in highest_odds or outcome['price'] > highest_odds[outcome['name']]['price']:

                                    if market['key'] == 'totals':
                                        highest_odds[outcome['name']] = {'bookmaker': bookmaker['title'],
                                                                  'price': outcome['price'], 'point': outcome['point']}
                                    elif market['key'] == 'h2h':
                                        highest_odds[outcome['name']] = {'bookmaker': bookmaker['title'],
                                                                         'price': outcome['price']}


                    if len(highest_odds) == 2:
                        if market['key'] == 'h2h':
                            prices = [data['price'] for data in highest_odds.values()]
                            arbitrage = ((1 / prices[0]) * 100) + ((1 / prices[1]) * 100)
                            if arbitrage < 100:
                                profitable_bets.append({
                                    'sport': sport,
                                    'match_id': match['id'],
                                    'commence_time': match['commence_time'],
                                    'home_team': match['home_team'],
                                    'away_team': match['away_team'],
                                    'odds': highest_odds,
                                    'arbitrage': arbitrage,
                                    'profit_percentage': 100 - arbitrage
                                })

                        elif market['key'] == 'totals':
                            prices = [data['price'] for data in highest_odds.values()]
                            points = [data['point'] for data in highest_odds.values()]
                            arbitrage = ((1 / prices[0]) * 100) + ((1 / prices[1]) * 100)

                            if points[0] == points[1] and arbitrage < 100:

                                profitable_bets.append({
                                    'sport': sport,
                                    'match_id': match['id'],
                                    'commence_time': match['commence_time'],
                                    'home_team': match['home_team'],
                                    'away_team': match['away_team'],
                                    'odds': highest_odds,
                                    'arbitrage': arbitrage,
                                    'profit_percentage': 100 - arbitrage
                                })

            elif response.status_code != 422:
                if response.status_code == 401:
                    key_counter +=1
                else:
                    print(f'GET request for {sport} failed with status code {response.status_code}')

    return profitable_bets
