from datetime import datetime
from disnake import Embed, User
from disnake.ext import commands

class status(commands.Cog):
    def __init__(self, client: commands.Bot, developer_id: int):
        self.client = client
        self.developer_id = developer_id

    @commands.slash_command(name='status', description='For developers | Информация о статусе бота')
    async def status(self, inter):
        user: User = inter.author
        if user.id != self.developer_id:
            await inter.response.send_message("Вы не разработчик бота", ephemeral=True)
            return

        now = datetime.now().strftime('%d.%m.%y')

        e = Embed(
            color=0xCD853F,
            description=f"""
            Status as of <t:{round(datetime.now().timestamp())}>
            ```js\n
- AutoRole: [Готов | {now}]
- Clear: [Готов | {now}]
- Config: [50% | {now}]
- Ban, Kick, Timeout: [0% | {now}]
- Logs: [75% {now}]\n```
            """
        )
        e.set_footer(text='Polina bot | © 2024 Все права защищены', icon_url=self.client.user.avatar)
        await inter.response.send_message(embed=e, ephemeral=True)

def setup(client: commands.Bot):
    developer_id = 702187267988652032
    client.add_cog(status(client, developer_id))
