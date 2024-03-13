import main

class ArbBet:
    def __init__(self, bet):
        self.sport = bet['sport']
        self.match_id = bet['match_id']
        self.commence_time = bet['commence_time']
        self.home_team = bet['home_team']
        self.away_team = bet['away_team']
        self.odds = bet['odds']
        self.arbitrage = bet['arbitrage']
        self.profit_percentage = bet['profit_percentage']

def main_func():
    raw_bets = main.get_arbitrage_bets()
    arb_bets = [ArbBet(bet) for bet in raw_bets]

    # Sort bets by arbitrage percentage
    arb_bets.sort(key=lambda x: x.arbitrage)

    # Print the sorted list
    for bet in arb_bets:
        print(f"Sport: {bet.sport}")
        print(f"Match ID: {bet.match_id}")
        print(f"Commence Time: {bet.commence_time}")
        print(f"Home Team: {bet.home_team}")
        print(f"Away Team: {bet.away_team}")
        print(f"Odds: {bet.odds}")
        print(f"Arbitrage %: {bet.arbitrage}")
        print(f"Profit Percentage: {bet.profit_percentage}")
        print("\n" + "-" * 50 + "\n")
    return arb_bets
if __name__ == "__main__":
    main_func()
