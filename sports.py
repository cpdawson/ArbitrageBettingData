import requests
import json
api_key_list = ["8014cca5d68ccacc087b00e54828e849", "baf0e52de498993d4c820e644423443f", "7f18f002d1a3018115f2331cfed80f17", "93e76e385d8e2c73032779c41eefc92c" ,"a7798ac707f30384bc40eb426f2346d7", "f1fdc1f247ddacb2f14e2d17ca2fef91", "b90b1b2999fa25fc353132f8f86d8d1b","7c8339f73243b1522986717d10848c1d", "2acb1bc7fa18d9fddfc75acc1397cff8","ccae58c1e160f0d2c74eb48a8720c271"]
count = 0
api_key = api_key_list[count]
url = f'https://api.the-odds-api.com/v4/sports/?apiKey={api_key}'

# https://api.the-odds-api.com/v4/sports/?apiKey=8014cca5d68ccacc087b00e54828e849
while requests.get(url).status_code == 401:
    count +=1
    api_key = api_key_list[count]
    url = f'https://api.the-odds-api.com/v4/sports/?apiKey={api_key}'

# Send a GET request to the URL
response = requests.get(url)
american_sports = ['baseball_mlb', 'soccer_usa_mls', 'icehockey_nhl', 'americanfootball_ncaaf', 'americanfootball_nfl', 'basketball_nba']
# Make sure the request was successful
if response.status_code == 200:
    # Parse the JSON data from the response
    sports = json.loads(response.text)
    sports_keys = []
    # Get the 'key' of each sport and add it to a list

    for sport in sports:
        # if sport['key'] in american_sports:
        sports_keys.append(sport['key'])

    # Print the list of sports keys
    # print(sports_keys)
else:
    print(f'GET request failed with status code {response.status_code}')
