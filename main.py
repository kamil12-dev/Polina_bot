import disnake
from disnake.ext import commands
import os
import sqlite3
#import keep_alive


bot = commands.Bot(command_prefix='/', intents=disnake.Intents.all(), reload=True)

conn = sqlite3.connect('bans.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS bans
             (user_id INTEGER PRIMARY KEY, username TEXT, reason TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS economy
             (user_id INTEGER PRIMARY KEY, username TEXT, balance INTEGER, last_daily INTEGER)''')

c.execute('''CREATE TABLE IF NOT EXISTS oilrigs
             (oilrig_id INTEGER PRIMARY KEY, owner INTEGER, oilrig_lvl INTEGER, oilrig_oil INTEGER, oilrig_max INTEGER, oilrig_next_lvl_exp INTEGER, oilrig_exp INTEGER, condition INTEGER)''')

c.execute('''CREATE TABLE IF NOT EXISTS levels
             (user_id INTEGER PRIMARY KEY, xp INTEGER, level INTEGER)''')






for filename in os.listdir(f'./cogs/'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"\033[38;5;38m[Polina] \033[38;5;67m⌗ COGS: \033[38;5;105m{filename[:-3]}\033[0;0m has been loaded")
    else:
        if filename != '__pycache__':
            for file in os.listdir(f'cogs.{filename}/'):
                if file.endswith('.py'):
                    bot.load_extension(f'cogs.{filename}.{file[:-3]}')
                    print(
                        f"\033[38;5;38m[Polina] \033[38;5;67m⌗ COGS: \033[38;5;105m{filename}.{file[:-3]}\033[0;0m has been loaded")    





bot.event
async def on_disconnect():
   conn.close()





bot.run()