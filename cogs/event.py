import disnake
from disnake.ext import commands



class events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=disnake.Status.idle, activity=disnake.Activity(type=disnake.ActivityType.listening, name="Yandex Music"))



    @commands.Cog.listener()
    async def on_slash_command_error(self, interaction: disnake.Interaction, error):
        if isinstance(error, commands.errors.CommandError):
            embed = disnake.Embed(
            title="Error",
            color=0x9b59b6,
            description=f"Команда не смогла отправить ответ\n```js\n- Error Description: {str('{')}\n{error}\n{str('}')}\n```\nЕсли вы хотите помочь в разработке бота, то вы можете отправить эту ошибку нам на [support server](https://discord.gg/EepTPBS8) в [bugs-report](https://discord.gg/wUT3czzU) канал, после чего мы это исправим.")
            await interaction.response.send_message(embed=embed, ephemeral=True)



    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, disnake.errors.MissingPermissions):
            await ctx.response.send_message("У вас недостаточно прав для использования этой команды.", ephemeral=True)



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(embed=disnake.Embed(description=f'** {ctx.author.name}, Данной команды нет, но скоро будет.**', color=0x9b59b6))



    @commands.Cog.listener()
    async def on_member_join(self, member):
        emb = disnake.Embed(title="Привет кисунь😊 добро пожаловать на сервер...", color=0x9b59b6)
        emb.add_field(name="Мои команды😊", value="Чтобы узнать подробнее команды напиши - /help")
        await member.send(embed=emb)



def setup(bot: commands.Bot):
    bot.add_cog(events(bot))