import disnake
import sqlite3
import datetime
from disnake.ext import commands
import random
from datetime import datetime, timedelta


conn = sqlite3.connect('bans.db')
c = conn.cursor()




class economy(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client


    @commands.slash_command(name="daily", description="Получить Poli-coins.")
    async def daily(ctx: disnake.ApplicationCommandInteraction):
        user_id = ctx.author.id
        username = ctx.author.name

        c.execute('SELECT balance, last_daily FROM economy WHERE user_id = ?', (user_id,))
        row = c.fetchone()

        if not row:
            c.execute('INSERT INTO economy (user_id, username, balance, last_daily) VALUES (?, ?, 0, 0)', (user_id, username))
            conn.commit()
            await ctx.send(f"{ctx.author.mention} Ваша карта создана! Используйте эту команду снова, чтобы получить свою ежедневную награду.", ephemeral=True)
        else:
            balance, last_daily = row
            last_daily_date = datetime.fromtimestamp(last_daily)

            if last_daily_date.date() == datetime.utcnow().date():
                await ctx.send(f"{ctx.author.mention} Вы уже получили Poli-coins сегодня! Попробуйте снова завтра.", ephemeral=True)
            else:
                new_balance = balance + random.randint(50, 150)
                c.execute('UPDATE economy SET balance = ?, last_daily = ? WHERE user_id = ?', (new_balance, int(datetime.utcnow().timestamp()), user_id))
                conn.commit()
                embed=disnake.Embed(color=0x9b59b6)
                embed.add_field(name="Poli-coins", value="Ежедневный бонус", inline=False)
                embed.add_field(name="Ты получил", value=f"{new_balance - balance} Poli-coins", inline=True)
                await ctx.send(embed=embed, ephemeral=True)



    @commands.slash_command(name="balance", description="Показать баланс.")
    async def balance(ctx: disnake.ApplicationCommandInteraction):
        user_id = ctx.author.id
        c.execute('SELECT balance FROM economy WHERE user_id = ?', (user_id,))
        row = c.fetchone()

        if not row:
            c.execute('INSERT INTO economy (user_id, username, balance, last_daily) VALUES (?, ?, 0, 0)', (user_id, ctx.author.name))
            conn.commit()
            embed = disnake.Embed(color=0x9b59b6)
            embed.add_field(name="Ваш баланс", value="На вашем счету: 0", inline=True)
            await ctx.send(embed=embed, ephemeral=True)
        else:
            balance = row[0]
            embed = disnake.Embed(color=0x9b59b6)
            embed.add_field(name="Ваш баланс", value=f"На вашем счету: {balance}", inline=True)
            await ctx.send(embed=embed, ephemeral=True) 



    @commands.slash_command(name="game", description="Играть в 'Орел и решка'.")
    async def heads_or_tails(ctx: disnake.ApplicationCommandInteraction, bet: int, guess: str):
        user_id = ctx.author.id

        c.execute('SELECT balance FROM economy WHERE user_id = ?', (user_id,))
        row = c.fetchone()
        if not row:
            await ctx.send("Вы не зарегистрированы в экономике. Используйте команду /daily для регистрации.", ephemeral=True)
            return
        balance = row[0]
        if balance < bet:
            await ctx.send("У вас недостаточно Poli-coins для игры.", ephemeral=True)
            return

        options = ["heads", "tails"]
        result = random.choice(options)

        if result == guess.lower():
            winnings = bet * 2
            c.execute('UPDATE economy SET balance = balance + ? WHERE user_id = ?', (winnings, user_id))
            conn.commit()
            message = f"{ctx.author.mention}, Вы выиграли {winnings} Poli-coins! Результат: {result}."
            color = 0x9b59b6  
        else:
            c.execute('UPDATE economy SET balance = balance - ? WHERE user_id = ?', (bet, user_id))
            conn.commit()
            message = f"{ctx.author.mention}, Вы проиграли {bet} Poli-coins! Результат: {result}."
            color = 0xe74c3c

        embed = disnake.Embed(color=color)
        embed.add_field(name="Орёл и решка", value=message, inline=False)
        await ctx.send(embed=embed, ephemeral=True)      



def setup(bot: commands.Bot):
    bot.add_cog(economy(bot))

   