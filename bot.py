# TOKEN = "MTEwODA0MTY1NDE1MTE1OTgzOA.GDgFCW.9VCIsi_0PRQ_-6y6YG8kUxSokc_d6rCKd5bQl8"
import discord
import arbBets
from datetime import datetime


async def send_message(message, bets):
    try:
        for bet in bets:

            # Parse the ISO 8601 datetime string and format it as a date and time
            commence_time = datetime.fromisoformat(bet.commence_time.replace("Z", "")).strftime('%Y-%m-%d %H:%M:%S')

            # Format the odds
            odds = bet.odds
            odds_str = f"Bet {list(odds.keys())[0]} on {odds[list(odds.keys())[0]]['bookmaker']} for a price of {odds[list(odds.keys())[0]]['price']}, and bet {list(odds.keys())[1]} on {odds[list(odds.keys())[1]]['bookmaker']} for a price of {odds[list(odds.keys())[1]]['price']}."

            embed = discord.Embed(
                title=f"Arbitrage Opportunities for {bet.sport}",
                description=f"Match: {bet.home_team} vs. {bet.away_team}\nCommence Time: {commence_time}\n{odds_str}\nProfit Percentage: {round(bet.profit_percentage, 2)}%",
                color=discord.Color.blue()
            )
            await message.channel.send(embed=embed)
    except Exception as e:
        print(e)



def runDiscordBot():
    TOKEN = "MTEwODA0MTY1NDE1MTE1OTgzOA.GDgFCW.9VCIsi_0PRQ_-6y6YG8kUxSokc_d6rCKd5bQl8"

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running")

    @client.event
    async def on_message(message):
        try:
            if message.content == '/arbbets':
                print('Received command')  # Debugging statement
                bets = arbBets.main_func()
                print('Arbitrage bets fetched')  # Debugging statement
                await send_message(message, bets)
        except Exception as e:
            print(e)

    client.run(TOKEN)

while True:
    runDiscordBot()