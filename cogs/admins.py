import disnake
from disnake.ext import commands
from random import randint, random
from disnake import Option
import sqlite3
import os 
import sys
import typing
from datetime import datetime


conn = sqlite3.connect('bans.db')
c = conn.cursor()

conn = sqlite3.connect('warn.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS warnings
             (user_id INTEGER PRIMARY KEY, num_warnings INTEGER)''')

conn = sqlite3.connect('black-list-words.db')
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS bad_words (word TEXT)")



class admins(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        

             
     
    @commands.slash_command(name="kick", description="Выгнать пользователя с сервера.")
    @commands.has_permissions(kick_members=True, administrator=True)
    async def kick_user(self, ctx: disnake.ApplicationCommandInteraction, user: disnake.Member, reason: str = None):
        await user.kick(reason=reason)
        embed=disnake.Embed(color=0x7788ff)
        embed.add_field(name="Kick", value=f"{ctx.author.mention} кикнула {user.mention} из {ctx.guild} сервера")
        await ctx.send(embed=embed, ephemeral=True) 


    @commands.slash_command(name='clear', description='Очистить чат')
    async def clear(self, ctx: disnake.ApplicationCommandInteraction, amount: int):
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send('Эта команда доступна только для администраторов.')
            return
        if amount > 1000:
            await ctx.send('Кискис нельзя удалить больше 1000 сообщений за раз.')
            return
        deleted = await ctx.channel.purge(limit=amount)
        embed=disnake.Embed(color=0x7788ff)
        embed.add_field(name="Очистила чат", value=f"Удалила {len(deleted)} сообщений 😊", inline=False)
        await ctx.send(embed=embed, ephemeral=True)


    
    @commands.slash_command(name="ban", description="Забанить пользователя.")
    @commands.has_permissions(ban_members=True, administrator=True)
    async def ban_user(self, ctx: disnake.ApplicationCommandInteraction, user: disnake.Member, reason: str = None):
        conn = sqlite3.connect('bans.db')
        c = conn.cursor()
        c.execute("SELECT user_id FROM bans WHERE user_id=?", (user.id,))
        banned_user = c.fetchone()  
        if banned_user:
            embed = disnake.Embed(title="Бан", description=f"{user.mention} Этот пользователь уже забанен.", color=0x7788ff)
        else:
            await user.ban(reason=reason)
            c.execute("INSERT INTO bans (user_id, username, reason) VALUES (?, ?, ?)", (user.id, user.name, reason))
            conn.commit()
            embed = disnake.Embed(title="Бан", description=f"{user.mention} Я забанила эту хамку.😤", color=0x7788ff)    
        await ctx.send(embed=embed, ephemeral=True) 


    @commands.slash_command(name="unban", description="Разбанить пользователя.")
    @commands.has_permissions(ban_members=True, administrator=True)
    async def unban_user(self, ctx: disnake.ApplicationCommandInteraction, user: disnake.User, reason: str = None):
        banned_users = await ctx.guild.bans()
        user_name, user_discriminator = user.name, user.discriminator
        for banned_entry in banned_users:
            banned_user = banned_entry.user
            if (banned_user.name, banned_user.discriminator) == (user_name, user_discriminator):
                await ctx.guild.unban(banned_user, reason=reason)
                c.execute("DELETE FROM bans WHERE user_id=?", (banned_user.id,))
                conn.commit()
                embed = disnake.Embed(title="Разбан", description=f"{banned_user.mention} был успешно разбанен.", color=0x7788ff)
                await ctx.send(embed=embed, ephemeral=True)
                return
        embed = disnake.Embed(title="Ошибка", description=f"Пользователь {user.mention} не был найден в списке забаненных.", color=0xff0000)
        await ctx.send(embed=embed, ephemeral=True)


    
    @commands.slash_command(name="message_bot", description="Отправить сообщение от имени Полины.")
    @commands.has_permissions(administrator=True)
    async def echo(self, ctx: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel, *, message: str):
        message = message.replace("-", "\n")
        embed=disnake.Embed(color=0x7788ff)
        embed.add_field(name="", value=message, inline=False)
        await channel.send(embed=embed) 





    @commands.slash_command(name='join', description='Зайти в голосовой канал')
    @commands.has_permissions(administrator=True)
    async def join(ctx: disnake.ApplicationCommandInteraction):
        if not ctx.author.voice:
            embed = disnake.Embed(
                color=0xe21212,
                title="Ошибка",
                description="Ты должен находиться в голосовом канале для использования этой команды"
            )
            await ctx.send(embed=embed, ephemeral=True)
            return

        channel = ctx.author.voice.channel
        await channel.connect()
        embed = disnake.Embed(
            color=0x7788ff,
            title="Готово",
            description=f"Успешно подключилась к голосовому каналу {channel.name}"
        )
        await ctx.send(embed=embed, ephemeral=True)

        voice_channel = ctx.author.voice.channel
        embed = disnake.Embed(color=0x7788ff)
        embed.add_field(name="voice", value=voice_channel.name, inline=False)
        await ctx.send(embed=embed, ephemeral=True)





    @commands.slash_command(name='leave', description='Выйти из голосового канала')
    @commands.has_permissions(administrator=True)
    async def leave(ctx: disnake.ApplicationCommandInteraction):
        if not ctx.guild.voice_client:
            embed = disnake.Embed(
                color=0x7788ff,
                title="Ошибка",
                description="Я не нахожусь в голосовом канале"
            )
            await ctx.response.send_message(embed=embed, ephemeral=True)
            return

        await ctx.guild.voice_client.disconnect()
        embed = disnake.Embed(
            color=0x7788ff,
            title="Готово",
            description="Успешно отключилась от голосового канала"
        )
        await ctx.response.send_message(embed=embed, ephemeral=True)



    @commands.slash_command(name='stay', description='Оставаться Полине в голосовом канале')
    @commands.has_permissions(administrator=True)
    async def stay(ctx):
        if not ctx.author.voice:
            embed = disnake.Embed(
                color=0x7788ff,
                title="Ошибка",
                description="Вы должны находиться в голосовом канале, чтобы использовать эту команду."
            )
            await ctx.send(embed=embed, ephemeral=True)
            return

        vc = ctx.author.voice.channel
        voice_client = ctx.guild.voice_client
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(vc)
            embed = disnake.Embed(
                color=0x7788ff,
                title="Готово",
                description=f'Я останусь в голосовом канале "{vc.name}" до тех пор, пока меня не попросят выйти. Для этого напиши /leave.'
            )
        else:
            voice_client = await vc.connect()
            embed = disnake.Embed(
                color=0x7788ff,
                title="Готово",
                description="Удачно зашла в голосовой канал."
            )

        await ctx.send(embed=embed, ephemeral=True)





    @commands.slash_command(name='restart', description='Перезапустить бота')
    @commands.has_permissions(administrator=True)
    async def restart(ctx: disnake.ApplicationCommandInteraction):
        await ctx.response.defer()

        try:
            os.execv(sys.executable, ['python'] + [arg for arg in sys.argv if arg != '--handle-sls'])
        except Exception as e:
            embed = disnake.Embed(title='Ошибка при перезапуске бота', color=0x7788ff)
            await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = disnake.Embed(title='Бот перезапущен успешно', color=0x7788ff)
            await ctx.send(embed=embed, ephemeral=True)

            
        



    @commands.slash_command(name='create_role', description='Создание новой роли')
    @commands.has_permissions(administrator=True)
    async def create_role(ctx, name: str):
        guild = ctx.guild
        role = await guild.create_role(name=name)
        embed = disnake.Embed(
            title=f'Роль создана',
            description=f'Новая роль {role.mention} была создана!',
            color=0x7788ff
        )
        await ctx.send(embed=embed, ephemeral=True)



    @commands.slash_command(name='assign_role', description='Выдача роли пользователю')
    @commands.has_permissions(administrator=True)
    async def assign_role(ctx, role: disnake.Role, member: disnake.Member):
        await member.add_roles(role)
        embed = disnake.embeds.Embed(
            title='Роль добавлена',
            description=f'Кисуне {member.mention} была выдана роль {role.mention}!',
            color=0x7788ff
        )
        await ctx.send(embed=embed, ephemeral=True)



    @commands.slash_command(name='remove_role', description='Удаление роли у пользователя')
    @commands.has_permissions(administrator=True)
    async def remove_role(ctx, role: disnake.Role, member: disnake.Member):
        await member.remove_roles(role)
        embed = disnake.embeds.Embed(
            title='Роль удалена',
            description=f'У кисуни {member.mention} была удалена роль {role.mention}!',
            color=0x7788ff
        )
        await ctx.send(embed=embed, ephemeral=True)



    @commands.slash_command(name="setnick", description="Сменить никнейм участнику.")
    @commands.has_permissions(administrator=True)
    async def set_nickname(self, ctx, member: disnake.Member, new_nickname: str):
        await member.edit(nick=new_nickname)
        embed = disnake.Embed(
            title="Изменение никнейма :pen_ballpoint:",
            description=f"Никнейм участника {member.mention} был изменен на {new_nickname}.",
            color=0x7788ff
        )
        await ctx.send(embed=embed, ephemeral=True)


    @commands.slash_command(name="setcolorrole", description="Изменить цвет роли")
    @commands.has_permissions(administrator=True)
    async def set_color_role(ctx, role: disnake.Role, color: str = None):
        if color is not None:
            try:
                color = disnake.Color(int(color.lstrip('#'), 16))
            except ValueError:
                embed = disnake.Embed(title='Ошибка', description='Некорректный формат цвета. Цвет должен быть указан в HEX-формате (например, #ff0000)', color=0xff0000)
                await ctx.send(embed=embed, ephemeral=True)
                return
        else:
            color = disnake.Color.random()

        await role.edit(color=color)

        embed = disnake.Embed(title='Цвет изменен', color=0x7788ff)
        embed.add_field(name='Роль', value=role.mention)
        embed.add_field(name='Цвет', value=f'#{color.value:06x}')

        await ctx.send(embed=embed, ephemeral=True)


    @commands.guild_only()
    @commands.slash_command(
        name="voting", 
        description="Провести голосование",
        options=[
            disnake.Option("text", "Введите текст!", required=True)
        ]
    )
    @commands.has_permissions(administrator=True)
    async def poll(self, ctx, *, text):
        await ctx.channel.purge(limit=1)
        poll = disnake.Embed(description=text, colour=randint(0, 0x7788ff))
        poll.timestamp = datetime.utcnow()
        msg = await ctx.channel.send(embed=poll)
        await msg.add_reaction("✔")
        await msg.add_reaction("❌")



    @commands.slash_command(name="send-dm", description="Отправить в лс сообщение от имени бота")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def send(self, ctx, member: disnake.Member, *, text):
        embed = disnake.Embed(title="Обращение к вам!", color=disnake.Color.dark_red())
        embed.add_field(name="Сообщение:", value=text)
        embed.set_thumbnail(url=ctx.bot.user.display_avatar)
        await member.send(embed=embed)

        success_embed = disnake.Embed(title="Сообщение отправлено!",
                                      description=f"Успешно отправил участнику {member.mention}",
                                      color=0x7788ff)
        await ctx.send(embed=success_embed, ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(admins(bot))