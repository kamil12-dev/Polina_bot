import disnake
import sqlite3
from disnake.ext import commands
import typing

class mutechat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="mchat", description="Блокировка чата пользователю")
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, user: disnake.Member, reason: str):
        conn = sqlite3.connect('warn.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS bad_words (word TEXT)")
        c.execute('''CREATE TABLE IF NOT EXISTS warnings (user_id INTEGER PRIMARY KEY, num_warnings INTEGER)''')

        embed = disnake.Embed(title="Пользователь получил блокировку чата!", color=0xCD853F)
        embed.add_field(name="Пользователь", value=f"{user.mention}")
        embed.add_field(name="Причина", value=f"`{reason}`")
        embed.add_field(name="Polina bot 2023 © Все права защищены",value='',inline=False)
        await ctx.response.send_message(embed=embed, ephemeral=True)

        try:
            role = await ctx.guild.create_role(name="mute", reason="mute отправки сообщений")
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, send_messages=False)
            await user.add_roles(role)

            dm_channel = await user.create_dm()
            embed = disnake.Embed(title="Вы получили блокировку чата", color=0xff0f0f)
            embed.add_field(name="Сервер", value=f"{ctx.guild.name}")
            embed.add_field(name="Причина", value=f"`{reason}`")
            embed.add_field(name="Polina bot 2023 © Все права защищены",value='',inline=False)
            await dm_channel.send(embed=embed)

            c.execute("SELECT * FROM warnings WHERE user_id=?", (user.id,))
            row = c.fetchone()
            if row:
                num_warnings = row[1] + 1
                c.execute("UPDATE warnings SET num_warnings=? WHERE user_id=?", (num_warnings, user.id))
            else:
                c.execute("INSERT INTO warnings VALUES (?, ?)", (user.id, 1))

            conn.commit()
            c.execute("SELECT * FROM warnings WHERE user_id=?", (user.id,))
            row = c.fetchone()
            if row and row[1] >= 3:
                kick_embed = disnake.Embed(title="Пользователь был исключен за многочисленные нарушения :x:", color=0xCD853F)
                kick_embed.add_field(name="Участник", value=f"{user.mention}")
                kick_embed.add_field(name="Причина", value=f"Получено `{row[1]}` предупреждений")
                await ctx.response.send_message(embed=kick_embed, ephemeral=True)
                await dm_channel.send(embed=kick_embed)
                await dm_channel.send(f"Вы были исключены с сервера `{ctx.guild.name}` за многочисленные нарушения.")
                await user.kick(reason="Получено 3 предупреждения")
        except disnake.errors.Forbidden:
            await ctx.response.send_message("У меня нет прав, чтобы предупредить этого пользователя", ephemeral=True)


    @commands.slash_command(name="unmchat", description="Снять блокировку чата у пользователя")
    @commands.has_permissions(administrator=True)
    async def unwarn(self, ctx, user: disnake.Member):
        conn = sqlite3.connect('warn.db')
        c = conn.cursor()

        c.execute("SELECT * FROM warnings WHERE user_id=?", (user.id,))
        row = c.fetchone()
        if row:
            num_warnings = row[1] - 1
            if num_warnings <= 0:
                c.execute("DELETE FROM warnings WHERE user_id=?", (user.id,))
            else:
                c.execute("UPDATE warnings SET num_warnings=? WHERE user_id=?", (num_warnings, user.id))
            conn.commit()
            role = disnake.utils.get(ctx.guild.roles, name="mute")
            if role:
                await user.remove_roles(role)

            admin_name = ctx.author.name
            admin_avatar = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url

            embed = disnake.Embed(title="Вы были размучены в чате!", color=0xCD853F)
            embed.add_field(name="Сервер", value=ctx.guild.name)
            embed.add_field(name="Предупреждения", value=f"У вас осталось {num_warnings} предупреждений.")
            embed.add_field(name="Размутил", value=f"Администратор: {admin_name}")
            embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.add_field(name="Polina bot 2023 © Все права защищены",value='',inline=True)
            await user.send(embed=embed)

            await ctx.response.send_message(embed=disnake.Embed(title="Предупреждение снято :white_check_mark:", color=0xCD853F).add_field(name="Пользователь", value=user.mention), ephemeral=True)
        else:
            await ctx.response.send_message(embed=disnake.Embed(title="У пользователя нет предупреждений :x:", color=0xCD853F).add_field(name="Пользователь", value=user.mention), ephemeral=True)


    @commands.slash_command(name="mchatinfo", description="Показать список пользователей в муте")
    async def warnings(self, ctx, user: typing.Optional[disnake.Member] = None):
        conn = sqlite3.connect('warn.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS warnings
                 (user_id INTEGER PRIMARY KEY, num_warnings INTEGER)''')
        c = conn.cursor()

        c.execute("CREATE TABLE IF NOT EXISTS bad_words (word TEXT)")
        if user is None:
            c.execute("SELECT * FROM warnings")
            rows = c.fetchall()
            if rows:
                embed = disnake.Embed(title="Список мутов на сервере :warning:", color=0xCD853F)
                for row in rows:
                    user = ctx.guild.get_member(row[0])
                    if user:
                        embed.add_field(name=f"Участник: {user.display_name}", value=f"Предупреждений: {row[1]}", inline=False)
                        embed.add_field(name="Polina bot 2023 © Все права защищены",value='',inline=True)
            else:
                embed = disnake.Embed(title="На сервере нет мутов :white_check_mark:", color=0xCD853F)
                embed.set_footer(text='Polina bot | ©2023', icon_url=ctx.author.avatar.url)
            await ctx.response.send_message(embed=embed, ephemeral=True)
        else:
            c.execute("SELECT * FROM warnings WHERE user_id=?", (user.id,))
            row = c.fetchone()
            if row:
                embed = disnake.Embed(title=f"Предупреждения для пользователя {user.display_name}", color=0xCD853F)
                embed.add_field(name="Предупреждений", value=row[1])
                embed.add_field(name="Polina bot 2023 © Все права защищены",value='',inline=True)
            else:
               embed = disnake.Embed(title=f"У пользователя {user.display_name} нет предупреждений :white_check_mark:", color=0xCD853F)
               embed.add_field(name="Polina bot 2023 © Все права защищены",value='',inline=True)
            await ctx.response.send_message(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(mutechat(bot))
