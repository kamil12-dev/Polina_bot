import disnake
from disnake.ext import commands
import sqlite3


conn = sqlite3.connect('level.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS levels
             (user_id INTEGER PRIMARY KEY, xp INTEGER, level INTEGER)''')

class level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        author_id = str(message.author.id)
        c.execute("SELECT xp, level FROM levels WHERE user_id=?", (author_id,))
        result = c.fetchone()
        if result is None:
            c.execute("INSERT INTO levels (user_id, xp, level) VALUES (?, ?, ?)", (author_id, 1, 1))
            conn.commit()
            result = (1, 1)
        xp, level = result
        level_up = int((level ** 2) + (level * 5))
        xp += 1
        if xp >= level_up:
            level += 1
            xp = 0
            embed = disnake.Embed(color=0x7788ff)
            embed.description = f"{message.author.mention} повысил уровень до {level}!"
            await message.channel.send(embed=embed)
            c.execute("UPDATE levels SET level=?, xp=? WHERE user_id=?", (level, xp, author_id))
            conn.commit()
        else:
            c.execute("UPDATE levels SET xp=? WHERE user_id=?", (xp, author_id))
            conn.commit()


    @commands.slash_command(name="level", description="Узнать свой уровень")
    async def level(ctx):
        author_id = str(ctx.author.id)
        c.execute("SELECT xp, level FROM levels WHERE user_id=?", (author_id,))
        result = c.fetchone()
        if result is None:
            await ctx.send("Вы еще не получили свой 1 уровень!")
            return
        xp, level = result
        xp_needed = 5 * (level ** 2) + 50 * level + 100 
        embed = disnake.Embed(color=0x7788ff, title="Уровень и опыт")
        embed.add_field(name="Уровень", value=f":medal: `{level}`", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True) 
        embed.add_field(name="Опыт", value=f":bar_chart: `{xp}`/`{xp_needed}`", inline=True)
        embed.set_footer(text="Polina bot © 2023 Все права защищены")
        await ctx.send(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(level(bot))