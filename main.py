import asyncio
import disnake
from disnake.ext import commands
import config
import keep_alive
import os
bot = commands.Bot(command_prefix=".", help_command=None, intents=disnake.Intents.all())


@bot.event
async def on_ready():
    await bot.change_presence(status=disnake.Status.online, activity=disnake.Game("Majestic RP"))


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    msg = message.content.lower()
    censored_words = ["дурак", "дура", "придурок", "хачи", "сын шлюхи", "полина шлюха", "я твою маму ебал"]

    for bad_content in msg.split():
        if bad_content in censored_words:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, Я не хотела бы это видеть😉")



@bot.event
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author}, у вас недостаточно прав для выполнения данной команды!")
    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=discord.Embed(
            description=f"Правильное использование команды: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief})\nExample: {ctx.prefix}{ctx.command.usage}"))


@bot.command(name="очистить", aliases=["clear", "cls"], brief="Очистить чат от сообщений, по умолчанию 10.", usage="clear <amount=10>")
@commands.has_permissions(administrator=True, manage_messages=True)
async def clear(ctx, amount: int=10):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Было удалено {amount + 1} сообщений.", delete_after=3)


@bot.command(name="кик", aliases=["kick", "kick-member"], brief="Выгнать пользователя с сервера", usage="kick <@user> <reason=None>")
@commands.has_permissions(administrator=True, kick_members=True)
async def kick(ctx, member: disnake.Member, *, reason=None):
    await ctx.message.delete()

    await ctx.send(f"Участник {member.mention}, был выгнан с сервера!", delete_after=3)
    await member.kick(reason=reason)


@bot.command(name="бан", aliases=["ban", "ban-member"], brief="Забанить пользователя на сервере", usage="ban <@user> <reason=None>")
@commands.has_permissions(administrator=True, ban_members=True)
async def ban(ctx, member: disnake.Member, *, reason=None):
    await ctx.message.delete()

    await ctx.send(f"Участник {member.mention}, был забанен на сервере.")
    await member.ban(reason=reason)


@bot.command(name="разбанить", aliases=["unban", "unban-member"], brief="Разбанить пользователя на сервере", usage="unban <user_id>")
@commands.has_permissions(administrator=True, ban_members=True)
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)

    await ctx.send("Участник разбанен")


@bot.command(name="мут", aliases=["mute", "mute-member"], brief="Запретить пользователю отправлять сообщения, стандарт 5 минут.", usage="mute <member> <time (s, h, d)=5m>")
@commands.has_permissions(administrator=True, mute_members=True, manage_roles=True)
async def mute(ctx, member: disnake.Member, mute_time="5m"):
    mute_role = disnake.utils.get(ctx.message.guild.roles, id=config.MUTE_ROLE_ID)

    await member.add_roles(mute_role)
    await ctx.send(f"{member.mention} был замучен на {mute_time}")

    if "s" or "" in mute_time:
        mute_time = int(mute_time[:1])
    elif "m" in mute_time:
        mute_time = int(mute_time[:1] * 60)
    elif "h" in mute_time:
        mute_time = int(mute_time[:1] * 60*60)
    elif "d" in mute_time:
        mute_time = int(mute_time[:1] * 60*60 * 24)

    await asyncio.sleep(mute_time)
    await member.remove_roles(mute_role)


@bot.command()
async def help(ctx):
    embed = disnake.Embed(
        title="Навигация по командам",
        description="Здесь ты сможешь найти доступные команды и их описание"
    )
    commands_list = ["clear", "kick", "ban", "unban"]
    descriptions_for_commands = ["Очистить чат", "Кикнуть пользователя", "Забанить пользователя", "Разбанить пользователя"]

    for command_name, description_command in zip(commands_list, descriptions_for_commands):
        embed.add_field(
            name=command_name,
            value=description_command,
            inline=False # Будет выводиться в столбик, если True - в строчку
        )

    await ctx.send(embed=embed)

keep_alive.keep_alive()
