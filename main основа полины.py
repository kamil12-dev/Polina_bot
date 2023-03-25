#Основной файл бота куда всё добавляется
import disnake
from disnake.ext import commands
from disnake import Embed
import asyncio
import random
import os
import sqlite3
from datetime import datetime, timedelta
import keep_alive


bot = commands.Bot(command_prefix='/', intents=disnake.Intents.all(), reload=True)

conn = sqlite3.connect('bans.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS bans
             (user_id INTEGER PRIMARY KEY, username TEXT, reason TEXT)''')


c.execute('''CREATE TABLE IF NOT EXISTS economy
             (user_id INTEGER PRIMARY KEY, username TEXT, balance INTEGER, last_daily INTEGER)''')

conn.commit()



@bot.event
async def on_ready():
    await bot.change_presence(status=disnake.Status.idle, activity=disnake.Activity(type=disnake.ActivityType.listening, name="Yandex Music"))



@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, disnake.errors.MissingPermissions):
        await ctx.response.send_message("У вас недостаточно прав для использования этой команды.", ephemeral=True)
    else:
        await ctx.response.send_message("Произошла какая-то ошибка. Обратитесь к администратору.", ephemeral=True)
    print(f"Error: {error}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await ctx.send(embed = disnake.Embed(description = f'** {ctx.author.name}, Данной команды нет, но скоро будет.**', color=0x9b59b6))



@bot.event
async def on_member_join(member):
    emb = disnake.Embed(title="Привет кисунь😊 добро пожаловать на сервер...", color=0x9b59b6)
    emb.add_field(name="Мои команды😊", value="Чтобы узнать подробнее команды зай напиши - /help")
    await member.send(embed=emb)

    


@bot.slash_command(name="kick", description="Выгнать пользователя с сервера.")
@commands.has_permissions(kick_members=True)
async def kick_user(ctx: disnake.ApplicationCommandInteraction, user: disnake.Member, reason: str = None):
    await user.kick(reason=reason)
    embed=disnake.Embed(color=0x9b59b6)
    embed.add_field(name="Kick", value=f"{ctx.author.mention} кикнула {user.mention} из {ctx.guild} сервера")
    await ctx.send(embed=embed)



@bot.slash_command(name='clear', description='Очистить чат')
async def clear(ctx: disnake.ApplicationCommandInteraction, amount: int):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send('Не получилось кисунь 😳')
        return
    if amount > 1000:
        await ctx.send('Кисуняя больше 1000 сообщений нельзя')
        return
    deleted = await ctx.channel.purge(limit=amount)
    
    embed=disnake.Embed(color=0x9b59b6)
    embed.add_field(name="Очистила чат", value=f"Удалила {len(deleted)} сообщений 😊", inline=False)
    await ctx.send(embed=embed)



@bot.slash_command(name="ban", description="Забанить пользователя.")
@commands.has_permissions(ban_members=True)
async def ban_user(ctx: disnake.ApplicationCommandInteraction, user: disnake.Member, reason: str = None):
    c.execute("SELECT user_id FROM bans WHERE user_id=?", (user.id,))
    banned_user = c.fetchone()

    if banned_user:
        embed = disnake.Embed(title="API Status", description=f"{user.mention} Этот пользователь уже забанен.", color=0x9b59b6)
    else:
        await user.ban(reason=reason)
        c.execute("INSERT INTO bans (user_id, username, reason) VALUES (?, ?, ?)", (user.id, user.name, reason))
        conn.commit()
        embed = disnake.Embed(title="API Status", description=f"{user.mention} Я забанила эту хамку.😤", color=0x9b59b6)

    await ctx.send(embed=embed)



@bot.slash_command(name="message_bot", description="Отправить сообщение от имени Полины.")
@commands.has_permissions(administrator=True)
async def echo(ctx: disnake.ApplicationCommandInteraction, *, message: str):
    message = message.replace("-", "\n")
    embed=disnake.Embed(color=0x9b59b6)
    embed.add_field(name="", value=message, inline=False)
    await ctx.response.send_message(message)
    await ctx.send(embed=embed)






@bot.slash_command(name="daily", description="Получить Poli-coins.")
async def daily(ctx: disnake.ApplicationCommandInteraction):
    user_id = ctx.author.id
    username = ctx.author.name

    c.execute('SELECT balance, last_daily FROM economy WHERE user_id = ?', (user_id,))
    row = c.fetchone()

    if not row:
        c.execute('INSERT INTO economy (user_id, username, balance, last_daily) VALUES (?, ?, 0, 0)', (user_id, username))
        conn.commit()
        await ctx.send(f"{ctx.author.mention} Ваша карта создана! Используйте эту команду снова, чтобы получить свою ежедневную награду.")
    else:
        balance, last_daily = row
        last_daily_date = datetime.fromtimestamp(last_daily)

        if last_daily_date.date() == datetime.utcnow().date():
            await ctx.send(f"{ctx.author.mention} Вы уже получили Poli-coins сегодня! Попробуйте снова завтра.")
        else:
            new_balance = balance + random.randint(50, 150)
            c.execute('UPDATE economy SET balance = ?, last_daily = ? WHERE user_id = ?', (new_balance, int(datetime.utcnow().timestamp()), user_id))
            conn.commit()
            embed=disnake.Embed(color=0x9b59b6)
            embed.add_field(name="Poli-coins", value="Ежедневный бонус", inline=False)
            embed.add_field(name="Ты получил", value=f"{new_balance - balance} Poli-coins", inline=True)
            await ctx.send(embed=embed)





@bot.slash_command(name="balance", description="Показать баланс.")
async def balance(ctx: disnake.ApplicationCommandInteraction):
    user_id = ctx.author.id
    c.execute('SELECT balance FROM economy WHERE user_id = ?', (user_id,))
    row = c.fetchone()

    if not row:
        c.execute('INSERT INTO economy (user_id, username, balance, last_daily) VALUES (?, ?, 0, 0)', (user_id, ctx.author.name))
        conn.commit()
        embed = disnake.Embed(color=0x9b59b6)
        embed.add_field(name="Ваш баланс", value="На вашем счету: 0", inline=True)
        await ctx.send(embed=embed)
    else:
        balance = row[0]
        embed = disnake.Embed(color=0x9b59b6)
        embed.add_field(name="Ваш баланс", value=f"На вашем счету: {balance}", inline=True)
        await ctx.send(embed=embed)






@bot.slash_command(name="game", description="Играть в 'Орел и решка'.")
async def heads_or_tails(ctx: disnake.ApplicationCommandInteraction, bet: int, guess: str):
    user_id = ctx.author.id

    c.execute('SELECT balance FROM economy WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    if not row:
        await ctx.send("Вы не зарегистрированы в экономике. Используйте команду /daily для регистрации.")
        return
    balance = row[0]
    if balance < bet:
        await ctx.send("У вас недостаточно Poli-coins для игры.")
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
        color = 0x9b59b6 
    
    embed = disnake.Embed(color=color)
    embed.add_field(name="Орёл и решка", value=message, inline=False)
    await ctx.send(embed=embed)




@bot.slash_command(name='help', description='Посмотреть все команды')
async def help(ctx):
    embed = disnake.Embed(
        title="Все мои команды Кисунь 😊",
        color=0x9b59b6
    )
    
    commands_list = ["/kick", "/clear", "/ban", "/join", "/leave", "/help","/echo", "/daily", "/balance", "/game"]
    descriptions_for_commands = [
        "Выгнать пользователя с сервера",
        "Очистить чат",
        "Забанить пользователя на сервере",
        "Зайти в голосовой канал",
        "Выйти в голосовой канал",
        "Посмотреть все команды",
        "Отправить сообщение от имени Полины",
        "Получить ежедневные Poli-coins",
        "Показать баланс",
        "Играть в игры на Poli-coins"
    ]

    for command_name, description_command in zip(commands_list, descriptions_for_commands):
        embed.add_field(
            name=command_name,
            value=description_command,
            inline=False 
        )

    await ctx.send(embed=embed)




@bot.slash_command(name='join', description='Зайти в голосовой канал')
async def join(ctx: disnake.ApplicationCommandInteraction):
    if not ctx.author.voice:
        await ctx.send('Ты должен находиться в голосовом канале для использования этой команды')
        return
    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()
    await ctx.send(f'Подключился к голосовому каналу "{voice_channel.name}".')



@bot.slash_command(name='leave', description='Выйти из голосового канала')
async def leave(ctx: disnake.ApplicationCommandInteraction):
    if not ctx.guild.voice_client:
        await ctx.send('Я не нахожусь в голосовом канале')
        return

    await ctx.guild.voice_client.disconnect()
    await ctx.send('Отключилась от голосового канала')


bot.event
async def on_disconnect():
   conn.close()


keep_alive.keep_alive()

bot.run(os.environ.get('TOKEN'))

