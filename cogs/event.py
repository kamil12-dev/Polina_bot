import disnake
from disnake.ext import commands



class events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.default_role_id = None 



    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=disnake.Status.idle, activity=disnake.Activity(type=disnake.ActivityType.listening, name="Yandex Music"))



    @commands.Cog.listener()
    async def on_message(self, message):
        await self.bot.process_commands(message)

        msg = message.content.lower()
        censored_words = ["кефир", "чифирный", "мать", "шлюха", "кефирчик", "бахмуте", "украина", "кефир выпил", "Кефирчика", "кефирчиком", "Vступай V ряды ЧVК Vагнер, праvда на нашей стороне, на стороне победителей!!!"]

        for bad_content in msg.split():
            if bad_content in censored_words:
                await message.delete()
                embed = disnake.Embed(
                    title="",
                    description=f"{message.author.mention}, Я удалила ваше сообщение, так как оно нарушает правила сервера!  ❌",
                    color=0xCD853F  
                )
                await message.channel.send(embed=embed)
                break



    @commands.Cog.listener()
    async def on_slash_command_error(self, interaction: disnake.Interaction, error):
        if isinstance(error, commands.errors.CommandError):
            embed = disnake.Embed(
            title="Error",
            color=0xCD853F,
            description=f"Команда не смогла отправить ответ\n```js\n- Error Description: {str('{')}\n{error}\n{str('}')}\n```\nЕсли вы хотите помочь в разработке бота, то вы можете отправить эту ошибку нам на [support server](https://discord.gg/EepTPBS8) в [bugs-report](https://discord.gg/wUT3czzU) канал, после чего мы это исправим.")
            await interaction.response.send_message(embed=embed, ephemeral=True)




    @commands.Cog.listener()
    async def on_member_join(self, member):
        emb = disnake.Embed(title="Привет! добро пожаловать на сервер...", color=0xCD853F)
        emb.add_field(name="Мои команды", value="Чтобы узнать подробнее команды напиши - /help")
        
        await member.send(embed=emb)


def setup(bot: commands.Bot):
    bot.add_cog(events(bot))