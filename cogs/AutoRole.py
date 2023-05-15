import disnake
from disnake.ext import commands
import sqlite3



class AutoRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_role_id = None
        self.conn = sqlite3.connect('role.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS default_role
                               (role_id INTEGER)''')
        self.conn.commit()

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        self.cursor.execute("SELECT role_id FROM default_role")
        result = self.cursor.fetchone()

        if result:
            role_id = result[0]
            guild = member.guild
            role = guild.get_role(role_id)
            try:
                await member.add_roles(role)
                emb = disnake.Embed(title=f"Привет {member.display_name}!", color=0x7788ff)
                emb.description = f"Я назначила тебе роль **{role.name}** на сервере {guild.name}."
                await member.send(embed=emb)
            except disnake.errors.Forbidden:
                print("")

    @commands.slash_command(name="setroleap", description="Установить роль, для Автовыдачи")
    @commands.has_permissions(manage_roles=True, administrator=True)
    async def set_default_role(self, ctx, role: disnake.Role = None):
        if role:
            self.default_role_id = role.id
            self.cursor.execute("DELETE FROM default_role")
            self.cursor.execute("INSERT INTO default_role (role_id) VALUES (?)", (self.default_role_id,))
            self.conn.commit()

            embed = disnake.Embed(
                title=f"Роль {role.name} установлена как роль по умолчанию.",
                color=0x7788ff
            )
        else:
            embed = disnake.Embed(
                title="Ошибка при установке роли по умолчанию!",
                description="Укажите корректную роль",
                color=0x7788ff
            )
        await ctx.send(embed=embed)

    @set_default_role.error
    async def set_default_role_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingPermissions):
            embed = disnake.Embed(
                title="Ошибка при установке роли по умолчанию!",
                description="У вас нет разрешения управлять ролями!",
                color=0x7788ff
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AutoRole(bot))
