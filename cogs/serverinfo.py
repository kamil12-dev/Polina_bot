from datetime import datetime

import disnake
from disnake.ext import commands


class ServerInfo(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.slash_command(name='serverinfo', description='Отображает информацию о сервере')
    async def serverinfo(self, inter: disnake.ApplicationCommandInteraction):
        guild = inter.guild
        embed = disnake.Embed(
            title='Информация о сервере',
            colour=disnake.Colour.purple(),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=guild.icon.url)
        embed.set_author(name=guild.name)
        embed.add_field(name='**Уровень верификации**', value=f"{str(guild.verification_level).title()}",
                        inline=True)
        embed.add_field(name='**Владелец**', value=f"{guild.owner}", inline=True)
        embed.add_field(name='**Дата создания**', value=f"<t:{int(guild.created_at.timestamp())}>", inline=True)
        embed.add_field(name='**Количество каналов**',
                        value=f" - Общие `{len(guild.channels)}`\n - Текстовые `{len(guild.text_channels)}`\n - Голосовые `{len(guild.voice_channels)}`\n - Категории `{len(guild.categories)}`")
        embed.add_field(name='**Участники**',
                        value=f" - Всего `{guild.member_count}`\n - Пользователей `{len([x for x in guild.members if not x.bot])}`\n - Ботов `{len([bot for bot in guild.members if bot.bot])}`")

        embed.add_field(name='** <:verify:1079411764921372693> Пользовательское поле **',
                        value=f" - Пользовательское значение здесь",
                        inline=False)

        if guild.premium_tier == 0:
            boost_tier = '▱▱▱▱▱▱ | 0 уровень'
        elif guild.premium_tier <= 1:
            boost_tier = '▰▰▱▱▱▱ | 1 уровень'
        elif guild.premium_tier <= 2:
            boost_tier = '▰▰▰▰▱▱ | 2 уровень'
        elif guild.premium_tier <= 3:
            boost_tier = '▰▰▰▰▰▰ | 3 уровень%'

        embed.add_field(name="**Бусты сервера**",
                        value=f"Уровень {boost_tier}\nОсобенности уровня `{guild.premium_tier} lvl`\nКоличество бустов `{guild.premium_subscription_count}`")

        await inter.response.send_message(embed=embed, ephemeral=True)


def setup(client: commands.Bot):
    client.add_cog(ServerInfo(client))
