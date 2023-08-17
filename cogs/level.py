import disnake
from disnake.ext import commands
import sqlite3
import datetime
from io import BytesIO
import aiohttp

conn = sqlite3.connect('level.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS levels
             (user_id INTEGER PRIMARY KEY, xp INTEGER, level INTEGER, last_active TEXT)''')


class level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel:
            await self.update_user(member)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        author_id = str(message.author.id)
        c.execute("SELECT xp, level FROM levels WHERE user_id=?", (author_id,))
        result = c.fetchone()
        if result is None:
            c.execute("INSERT INTO levels (user_id, xp, level, last_active) VALUES (?, ?, ?, ?)",
                      (author_id, 1, 1, datetime.datetime.utcnow()))
            conn.commit()
            result = (1, 1)
        xp, level = result
        level_up = int((level ** 2) + (level * 5))
        xp += 2
        if xp >= level_up:
            level += 2
            xp = 0
            embed = disnake.Embed(color=0xCD853F)
            embed.description = f"{message.author.mention} повысил уровень до {level}!"
            await message.channel.send(embed=embed)
            c.execute("UPDATE levels SET level=?, xp=? WHERE user_id=?", (level, xp, author_id))
            conn.commit()
        else:
            c.execute("UPDATE levels SET xp=? WHERE user_id=?", (xp, author_id))
            conn.commit()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel:
            author_id = str(member.id)
            conn = sqlite3.connect('level.db')
            c = conn.cursor()

            c.execute("SELECT last_active FROM levels WHERE user_id=?", (author_id,))
            result = c.fetchone()

            if result:
                last_active = datetime.datetime.strptime(result[0], "%Y-%m-%d")
                if datetime.datetime.utcnow() - last_active >= datetime.timedelta(minutes=10):
                    c.execute("UPDATE levels SET last_active=? WHERE user_id=?", 
                              (datetime.datetime.utcnow(), author_id))
                    conn.commit()

            conn.close() 



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
            embed = disnake.Embed(color=0xCD853F)
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
        embed = disnake.Embed(color=0xCD853F, title="Уровень и опыт")
        embed.add_field(name="Уровень", value=f":medal: `{level}`", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True) 
        embed.add_field(name="Опыт", value=f":bar_chart: `{xp}`/`{xp_needed}`", inline=True)
        embed.set_footer(text="Polina bot © 2023 Все права защищены")
        await ctx.send(embed=embed, ephemeral=True)



    @commands.slash_command(name="leaderboard", description="Показать лидеров по уровням.")
    async def leaderboard(self, ctx):
        c.execute("SELECT user_id, level FROM levels ORDER BY level DESC LIMIT 10")
        results = c.fetchall()

        if not results:
            await ctx.send("Лидерборд пуст.")
            return
        
        leaderboard_text = "Топ 10 игроков по уровням:\n"
        for i, (user_id, level) in enumerate(results, start=1):
            user = await self.bot.fetch_user(int(user_id))
            leaderboard_text += f"{i}. {user.mention} - Уровень {level}\n"

        embed = disnake.Embed(title="Топы по уровням", description=leaderboard_text, color=0xCD853F)
        await ctx.send(embed=embed, ephemeral=True)


    @commands.slash_command(name="reset", description="Сбросить уровни и опыт всех пользователей.")
    @commands.has_permissions(administrator=True)
    async def reset_levels(self, ctx):
        c.execute("DELETE FROM levels")
        conn.commit()

        embed = disnake.Embed(title="Сброс уровней и опыта", description="Уровни и опыт всех пользователей были сброшены.", color=0xCD853F)
        await ctx.send(embed=embed, ephemeral=True)


    @commands.slash_command(name="addxp", description="Добавить опыт пользователю.")
    @commands.has_permissions(administrator=True)
    async def add_xp(self, ctx, member: disnake.Member, xp: int):
        author_id = str(member.id)
        c.execute("SELECT xp, level FROM levels WHERE user_id=?", (author_id,))
        result = c.fetchone()

        if result is None:
            await ctx.send("Этот пользователь ещё не получил 1 уровень.")
            return
        
        xp_before, level = result
        xp_after = xp_before + xp

        c.execute("UPDATE levels SET xp=? WHERE user_id=?", (xp_after, author_id))
        conn.commit()

        embed = disnake.Embed(title="Добавление опыта", description=f"Пользователь {member.mention} получил {xp} опыта.", color=0xCD853F)
        await ctx.send(embed=embed, ephemeral=True)

    @commands.slash_command(name="setlevel", description="Установить уровень пользователю.")
    @commands.has_permissions(administrator=True)
    async def set_level(self, ctx, member: disnake.Member, level: int):
        author_id = str(member.id)
        c.execute("UPDATE levels SET level=?, xp=? WHERE user_id=?", (level, 0, author_id))
        conn.commit()

        embed = disnake.Embed(title="Установка уровня", description=f"Пользователь {member.mention} теперь на {level} уровне.", color=0xCD853F)
        await ctx.send(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(level(bot))