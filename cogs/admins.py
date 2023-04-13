import disnake
from disnake.ext import commands
import sqlite3
import os 
import sys

conn = sqlite3.connect('bans.db')
c = conn.cursor()


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
            await ctx.send(embed=embed)
            return

        channel = ctx.author.voice.channel
        await channel.connect()
        embed = disnake.Embed(
            color=0x7788ff,
            title="Готово",
            description=f"Успешно подключилась к голосовому каналу {channel.name}"
        )
        await ctx.send(embed=embed)

        voice_channel = ctx.author.voice.channel
        await voice_channel.connect()
        embed=disnake.Embed(color=0x7788ff)
        embed.add_field(name="voice", value=voice_channel.name, inline=False)
        await ctx.send(f'Подключился к голосовому каналу "{voice_channel.name}".', embed=embed, ephemeral=True)



    @commands.slash_command(name='leave', description='Выйти из голосового канала')
    @commands.has_permissions(administrator=True)
    async def leave(ctx: disnake.ApplicationCommandInteraction):
        if not ctx.guild.voice_client:
            embed = disnake.Embed(
                color=0x7788ff,
                title="Ошибка",
                description="Я не нахожусь в голосовом канале"
            )
            await ctx.send(embed=embed)
            return

        await ctx.guild.voice_client.disconnect()
        embed = disnake.Embed(
            color=0x7788ff,
            title="Готово",
            description="Успешно отключилась от голосового канала"
        )
        await ctx.send(embed=embed, ephemeral=True)


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
        else:
            voice_client = await vc.connect()

        embed = disnake.Embed(
            color=0x7788ff,
            title="Готово",
            description=f'Я останусь в голосовом канале "{vc.name}" до тех пор, пока меня не попросят выйти. Для этого напиши /leave.'
        )
        await ctx.send(embed=embed, ephemeral=True)




    @commands.slash_command(name='restart', description='Перезапустить бота')
    @commands.has_permissions(administrator=True)
    async def restart(ctx: disnake.ApplicationCommandInteraction):
        await ctx.response.defer()

        try:
            os.execv(sys.executable, ['python'] + [arg for arg in sys.argv if arg != '--handle-sls'])
        except Exception as e:
            await ctx.senzzd(ephemeral=True)
            
        



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



def setup(bot: commands.Bot):
    bot.add_cog(admins(bot))