import disnake
from disnake.ext import commands
import os 
import sys



developer_id = 702187267988652032

class Restart(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.slash_command(name='restart', description='For developers | Выполняет полную перезагрузку бота')
    async def restart(self, inter):
        if inter.author.id != developer_id:
            await inter.response.send_message("Вы не являетесь разработчиком бота и не можете использовать эту команду.", ephemeral=True)
            return

        embed = disnake.Embed(
            description="Команда перезагрузки была успешно выполнена, ожидайте включения!",
            color=0xCD853F

        )
        embed.set_footer(text='Polina bot | © 2024 Все права защищены', icon_url=self.client.user.avatar)

        await inter.response.send_message(embed=embed, ephemeral=True)
        restart()

def restart():
    print('Выполняется рестарт. Бот будет включен через пару секунд!')
    os.system('cls')
    os.execl(sys.executable, sys.executable, *sys.argv)

def setup(client: commands.Bot):
    client.add_cog(Restart(client))
