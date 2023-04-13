import disnake
from disnake.ext import commands
import os
import sqlite3
import keep_alive


bot = commands.Bot(command_prefix='/', intents=disnake.Intents.all(), reload=True)

conn = sqlite3.connect('bans.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS bans
             (user_id INTEGER PRIMARY KEY, username TEXT, reason TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS economy
             (user_id INTEGER PRIMARY KEY, username TEXT, balance INTEGER, last_daily INTEGER)''')


conn.commit()





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





keep_alive.keep_alive()

bot.run(os.environ.get('TOKEN'))

