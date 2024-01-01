import disnake
from disnake.ext import commands
import sqlite3
import asyncio
import aiohttp
import datetime

class mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS mutes
                               (user_id INT PRIMARY KEY, unmute_time INT)''')
        self.conn.commit()

    @commands.slash_command(name='voicemute', description='Mute пользователя в голосовых каналах')
    @commands.has_permissions(manage_roles=True)
    async def tempmute(self, ctx, member: disnake.Member, duration: int, reason=None):
        mute_role = disnake.utils.get(ctx.guild.roles, name="mute")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="mute")

        permissions = disnake.Permissions.none()
        permissions.update(send_messages=False, connect=True, speak=True, stream=True, use_voice_activation=True)
        await mute_role.edit(permissions=permissions)

        await member.add_roles(mute_role, reason=reason)

        await self.mute_microphone(member, True)

        unmute_time = asyncio.get_event_loop().time() + duration * 60

        self.cursor.execute('INSERT OR REPLACE INTO mutes VALUES (?, ?)', (member.id, unmute_time))
        self.conn.commit()

        embed = disnake.Embed(title="Мут", color=0xCD853F)
        embed.add_field(name="Пользователь", value=member.mention, inline=True)
        embed.add_field(name="Длительность", value=f"{duration} минут", inline=True)
        embed.add_field(name="Причина", value=reason, inline=True)
        embed.set_footer(text=f"Размут через: {duration} минут ⏰")
        embed.set_footer(text="Polina bot © 2024 Все права защищены")
        
        await ctx.send(embed=embed, ephemeral=True)

        await self.send_mute_dm(member, ctx.guild.name, reason, duration, ctx.author)

        await asyncio.sleep(duration * 60)
        await self.unmute_member(member)

    @commands.slash_command(name='unvoicemute', description='unMute пользователя в голосовых каналах')
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: disnake.Member):
        mute_role = disnake.utils.get(ctx.guild.roles, name="mute")
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await self.unmute_member(member)

            embed = disnake.Embed(title="Размут", color=0xCD853F)
            embed.add_field(name="Пользователь", value=member.mention, inline=True)
            embed.set_footer(text="Был размучен 🎉")
            embed.set_footer(text="Polina bot © 2024 Все права защищены")
            
            await ctx.send(embed=embed, ephemeral=True)

            await self.send_unmute_dm(member)
        else:
            await ctx.send(f"{member.mention} не был mute.")

        self.cursor.execute('DELETE FROM mutes WHERE user_id = ?', (member.id,))
        self.conn.commit()

    async def mute_microphone(self, member: disnake.Member, mute: bool):
        url = f"https://discord.com/api/v10/guilds/{member.guild.id}/members/{member.id}"
        headers = {
            "Authorization": f"Bot {self.bot.http.token}",
            "Content-Type": "application/json"
        }
        data = {
            "mute": mute
        }

        async with aiohttp.ClientSession() as session:
            async with session.patch(url, headers=headers, json=data) as response:
                if response.status == 204:
                    return True
                else:
                    return False

    async def unmute_member(self, member: disnake.Member):
        await self.mute_microphone(member, False)
        await self.send_unmute_dm(member)

    async def send_mute_dm(self, member, guild_name, reason, duration, admin):
        try:
            dm_channel = await member.create_dm()
            embed = disnake.Embed(title="Вы получили Mute", color=0xCD853F)
            embed.add_field(name="Сервер", value=guild_name, inline=True)
            embed.add_field(name="Причина", value=reason, inline=True)
            unmute_datetime = datetime.datetime.now() + datetime.timedelta(minutes=duration)
            embed.add_field(name="Дата и время размута", value=unmute_datetime.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
            embed.add_field(name="Администратор", value=admin.name, inline=True)
            embed.set_footer(text="Вы будете размучены автоматически. 🕒")
            embed.set_footer(text="Polina bot © 2024 Все права защищены")
            await dm_channel.send(embed=embed)
        except Exception as e:
            print(f"Ошибка при отправке сообщения размута пользователю {member}: {e}")

    async def send_unmute_dm(self, member):
        try:
            dm_channel = await member.create_dm()
            embed = disnake.Embed(title="Вы размучены 🎉", color=0xCD853F)
            embed.add_field(name="Сервер", value=member.guild.name, inline=True)
            embed.set_footer(text="Вы размучены 🎉")
            embed.set_footer(text="Polina bot © 2024 Все права защищены")
            await dm_channel.send(embed=embed)
        except Exception as e:
            print(f"Ошибка при отправке сообщения размута пользователю {member}: {e}")

    @commands.Cog.listener()
    async def on_ready(self):
        current_time = asyncio.get_event_loop().time()
        for guild in self.bot.guilds:
            self.cursor.execute('SELECT * FROM mutes WHERE unmute_time <= ?', (current_time,))
            mutes = self.cursor.fetchall()
            for mute in mutes:
                member = guild.get_member(mute[0])
                if member:
                    mute_role = disnake.utils.get(guild.roles, name="mute")
                    if not mute_role:
                        mute_role = await guild.create_role(name="mute")
                    await member.remove_roles(mute_role)
                    self.cursor.execute('DELETE FROM mutes WHERE user_id = ?', (member.id,))
                    self.conn.commit()

def setup(bot):
    bot.add_cog(mute(bot))