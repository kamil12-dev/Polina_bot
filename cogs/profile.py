import disnake
from disnake import Embed
from disnake.ext import commands
from datetime import datetime


class profile(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.slash_command(name='profile', description='Посмотреть свой профиль')
    async def userinfo(self, inter, member: disnake.Member = None):
        if member is None:
            member = inter.author

        роли = member.roles  
        упоминаемые_роли = []  
        for роль in роли: 
            упоминаемые_роли.append(роль.mention) 
        упоминаемые_роли = str(упоминаемые_роли).replace('[', '').replace(']', '').replace("'", '') 
        верхняя_роль = member.top_role.mention 

        embed = disnake.Embed(
            title=f'Информация о пользователе {member.name}',
            colour=disnake.Colour.random()
        )
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name='** ID  **', value=member.id, inline=False)
        embed.add_field(name='** Никнейм  **', value=member.name)
        embed.add_field(name='** Отображаемое имя **', value=member.display_name)
        embed.add_field(name='** Создан в **', value=f"<t:{int(member.created_at.timestamp())}>")
        embed.add_field(name='** Присоединился в **', value=f"<t:{int(member.joined_at.timestamp())}>")
        embed.add_field(name='** Роли **', value=упоминаемые_роли, inline=False)
        embed.add_field(name='** Высшая роль **', value=верхняя_роль)
        embed.add_field(name='** Бот **', value=True if member.bot == True else False)
        embed.add_field(name='** Статус **', value=f'{member.status}')
        embed.set_footer(text='Polina | 2023', icon_url=self.client.user.avatar)
        await inter.response.send_message(embed=embed)


def setup(client: commands.Bot):
    client.add_cog(profile(client))