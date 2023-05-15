import disnake
from disnake.ext import commands
from random import randint, random




class infobots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name= "bot", description="Информация о Polina bot")
    async def bot(self, ctx):
        info=disnake.Embed(title = ":robot: Информация о боте", description = f"Информация об **Polina bot**", colour=randint(0, 0xffffff))
        info.add_field(name = ":bearded_person: Разработчик:", value = "`П͓̽р͓̽о͓̽в͓̽а͓̽й͓̽д͓̽е͓̽р͓̽#6666`")
        info.add_field(name = ":ledger: Моя библиотека:", value="Disnake", inline=False)
        info.add_field(name = ":floppy_disk: Моя версия:", value = "`v3.0`", inline=False)
        info.add_field(name = "🔗 Приглашение:", value = f"[Нажми](https://discord.com/api/oauth2/authorize?client_id=1023602153694183475&permissions=8&scope=bot)", inline = True)
        info.add_field(name = "⚙️ Команд:", value = f"{len(self.bot.slash_commands)}")
        info.add_field(name = "📊 Кол-во гильдий:", value = f"{len(self.bot.guilds)}")
        info.add_field(name = ":busts_in_silhouette: Пользователей:", value = f"{len(self.bot.users)}", inline=False)
        info.add_field(name=":ping_pong: Ping:", value=f"{round(self.bot.latency * 1000)}ms")
        info.set_footer(text="Polina bot © 2023 Все права защищены")
        await ctx.send(embed=info, ephemeral=True)


def setup(bot):
    bot.add_cog(infobots(bot))
