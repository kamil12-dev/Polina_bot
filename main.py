#Основной файл бота куда всё добавляется
import disnake
from disnake.ext import commands
import asyncio
import random
import keep_alive
import os


bot = commands.Bot(command_prefix='/', intents=disnake.Intents.all())



@bot.event
async def on_ready():
    await bot.change_presence(status=disnake.Status.online, activity=disnake.Game("Majestic RP"))



@bot.event
async def on_member_join(member):
    emb = disnake.Embed(title="Привет кисунь😊 добро пожаловать на сервер - Мир Хачей..", color=0x9b59b6)
    emb.add_field(name= "Мои команды😊",value="Чтобы узнать подробнее команды кис напиши - /help")
    await member.send(embed = emb)

    


@bot.slash_command(name="kick", description="Выгнать пользователя с сервера.")
@commands.has_permissions(kick_members=True)
async def kick_user(ctx: disnake.ApplicationCommandInteraction, user: disnake.Member, reason: str = None):
    await user.kick(reason=reason)
    await ctx.send(f"{user.mention} Я удалила кисуню.😳")



@bot.slash_command(name="ban", description="Забанить пользователя.")
@commands.has_permissions(ban_members=True)
async def ban_user(ctx: disnake.ApplicationCommandInteraction, user: disnake.Member, reason: str = None):
    await user.ban(reason=reason)
    await ctx.send(f"{user.mention} Я забанила эту хамку.😤")



@bot.slash_command(name="timer", description="Устанавливает таймер на указанное количество времени.")
async def set_timer(ctx: disnake.ApplicationCommandInteraction, seconds: int):
    await ctx.send(f"Timer set for {seconds} seconds.")
    await asyncio.sleep(seconds)
    await ctx.send(f"{ctx.author.mention}, время вышло кисунь!⏲")



@bot.slash_command(name="playgame", description="Игра камень ножницы")
async def play_game(ctx: disnake.ApplicationCommandInteraction, game: str):
    if game == "1":
        await ctx.send("Давайте поиграем в камень-ножницы-бумага! Выберите свой ход: камень, ножницы или бумага.")
        def check(m):
            return m.author == ctx.author and m.content.lower() in ["камень", "ножницы", "бумага"]
        try:
            user_choice = await bot.wait_for("message", check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send("Ты слишком долго выбирал!😊")
            return
        bot_choice = random.choice(["камень", "ножницы", "бумага"])
        await ctx.send(f"На кисунь {bot_choice}!")
        if user_choice.content.lower() == bot_choice:
            await ctx.send("Ничья кисунь!")
        elif user_choice.content.lower() == "камень" and bot_choice == "бумага":
            await ctx.send("Ты победил!")
        elif user_choice.content.lower() == "ножницы" and bot_choice == "камень":
            await ctx.send("Ты победил!")
        elif user_choice.content.lower() == "бумага" and bot_choice == "ножницы":
            await ctx.send("Ты победил!")
        else:
            await ctx.send("Я победила!")
    else:
        await ctx.send(f"Я не знаю, как играть {game} в это!")



@bot.slash_command(name='help', description='Посмотреть все доступные команды')
async def help(ctx):
    embed = disnake.Embed(
        title="Все мои команды Кисунь😊",
        color=0x9b59b6
        
    )
    commands_list = ["/kick", "/clear", "/ban", "/join", "/leave", "/help", "/playgame", "/time"]
    descriptions_for_commands = ["Выгнать пользователя с сервера", "Очистить чат", "Забанить пользователя на сервере", "Зайти в голосовой канал", "Выйти в голосовой канал", "Посмотреть все команды","Поиграть в игры с ботом", "Поставить таймер на время"]

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





keep_alive.keep_alive()

bot.run(os.environ.get('TOKEN'))