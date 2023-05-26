import os
from raffleBot import RaffleBot

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    token = os.getenv('RaffleBotToken')
    bot = RaffleBot(token)
    bot.run()

