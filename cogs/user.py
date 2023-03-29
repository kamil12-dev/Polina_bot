import disnake
from disnake.ext import commands



class user(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client




    @commands.slash_command(name='help', description='Посмотреть все команды')
    async def help(ctx):
        embed = disnake.Embed(
            title="Все мои команды Кисунь 😊",
            color=0x9b59b6
        )
        
        commands_list = ["/kick", "/clear", "/ban", "/join", "/leave", "/help","/echo", "/daily", "/balance", "/game", "/stay"]
        descriptions_for_commands = [
            "Выгнать пользователя с сервера",
            "Очистить чат",
            "Забанить пользователя на сервере",
            "Зайти в голосовой канал",
            "Выйти в голосовой канал",
            "Посмотреть все команды",
            "Отправить сообщение от имени Полины",
            "Получить ежедневные Poli-coins",
            "Показать баланс",
            "Играть в игры на Poli-coins",
            "Оставить Полину в голосовом канале"
        ]
    
        for command_name, description_command in zip(commands_list, descriptions_for_commands):
            embed.add_field(
                name=command_name,
                value=description_command,
                inline=False 
            )
    
        await ctx.send(embed=embed)




def setup(bot: commands.Bot):
    bot.add_cog(user(bot))