import disnake
from disnake.ext import commands


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="ticket",
        description="Создать тикет для связи с администрацией"
    )
    async def ticket(self, inter):
        guild = inter.guild
        user = inter.author

        embed = disnake.Embed(
            title='Техподдержка',
            description='Нажмите на кнопку, чтобы создать обращение в техподдержку.',
            color=disnake.Color.blurple()
        )
        embed.set_footer(text="Техподдержка")

        button = disnake.ui.Button(style=disnake.ButtonStyle.primary, label="Открыть тикет", custom_id="create_ticket", emoji="🎫")
        view = disnake.ui.View()
        view.add_item(button)

        await inter.response.send_message(embed=embed, view=view, ephemeral=True)

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        if inter.component.custom_id == "create_ticket":
            guild = inter.guild
            user = inter.author

            channel_name = f'Техподдержка'
            overwrites = {
                guild.default_role: disnake.PermissionOverwrite(read_messages=False, send_messages=False),
                guild.me: disnake.PermissionOverwrite(read_messages=True, send_messages=True),
                user: disnake.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
            }
            channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites)

            embed = disnake.Embed(
                title='Техподдержка',
                description=f'Привет,{user.mention}! \nМодератор поможет вам в ближайшее время. \nА пока опишите вашу проблему как можно подробнее!)',
                color=disnake.Color.green()
            )
            embed.set_footer(text="Техподдержка")

            close_button = disnake.ui.Button(style=disnake.ButtonStyle.danger, label="Закрыть тикет", custom_id=f"close_ticket:{channel.id}", emoji="🔒")
            close_view = disnake.ui.View()
            close_view.add_item(close_button)

            message = await channel.send(content=f"{user.mention} создал новое обращение в техподдержку!", embed=embed, view=close_view)
            await message.pin()

            await inter.response.send_message(embed=embed, ephemeral=True)

        elif inter.component.custom_id.startswith("close_ticket"):
            channel_id = int(inter.component.custom_id.split(":")[1])
            channel = self.bot.get_channel(channel_id)

            if channel:
                if inter.author.guild_permissions.administrator:
                    await channel.delete()
                    await inter.response.send_message(content="Тикет был закрыт.", ephemeral=True)
                else:
                    await inter.response.send_message(content="У вас нет прав на закрытие тикета.", ephemeral=True)
            else:
                await inter.response.send_message(content="Канал техподдержки не найден.", ephemeral=True)

def setup(bot):
    bot.add_cog(Tickets(bot))
