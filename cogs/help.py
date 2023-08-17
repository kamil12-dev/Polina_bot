import disnake
from disnake.ext import commands



class helpc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(name="help", description="Помощь по командам.", permissions=[disnake.Permissions().none()])
    async def __help(self, ctx):
        view = design_help_cmd()
        embed = disnake.Embed(title=f'**__Список команд__**', description='Пожалуйста, выберите категорию.', color=disnake.Color.green())
        embed.set_footer(text=f"Запросил команду: {ctx.author.name}")
        await ctx.send(embed=embed, view=view, ephemeral=True)


class design_help_cmd(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(help_cmd())

class help_cmd(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label='Developers', description='Команды для разработчиков ботов.', emoji='👨‍💻'),
            disnake.SelectOption(label='Развлечения', description='Куча весёлостей и развлечений!', emoji='<:fun:1004671040116490300>'),
            disnake.SelectOption(label='Модерация', description='Команды для модераторов / Администрации.', emoji='<:moderator:1004670538758754445>'),
            disnake.SelectOption(label='Level', description='Общение с разнами серверами через бота.', emoji='<:chat:992097506748010656>'),
            disnake.SelectOption(label='Общее', description='Общие команды для обычных юзеров.', emoji='<:all:1004659237336657972>'),
            disnake.SelectOption(label='Животные', description='Животные', emoji='<:animals:1004669831217422417>'),
            disnake.SelectOption(label='NSFW', description='18+ изображение', emoji='<:18:1004669364705955852>'),
            disnake.SelectOption(label='Информация', description='Полезные команды', emoji='<:info:992096997500780574>'),
            disnake.SelectOption(label='Premium', description='Покупка подписки', emoji='💲'),
            disnake.SelectOption(label='Экономика', description='Команды для экономики', emoji='💰'),
        ]
        super().__init__(placeholder='Выбор категории', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: disnake.Interaction):
        if "Развлечения" in self.values:
            embed = disnake.Embed(color=disnake.Color.yellow())
            embed.add_field(name='Развлечения', value=(
                '`/gay` > в разработке...\n'
                '`/chill` > Узнать размер члена! 😌\n'
                '`/8ball` > Задать вопрос магическому шару. 🎱\n'
            ))
            await interaction.response.edit_message(embed=embed)
        if "Модерация" in self.values:
            embed = disnake.Embed(color=disnake.Color.blurple())
            embed.add_field(name='Модерация', value=(
                '`/clear` >  Очистка чата 🗑️\n'
                '`/embed` > Эмбед от имени бота 📑\n'
                '`/poll` > Голосование 🗳️\n'
                '`/kick` > Выгнать пользователя с сервера 😠\n'
                '`/ban` > Забанить пользователя на сервере 🚫\n'
                '`/join` > Зайти в голосовой канал 🎤\n'
                '`/leave` > Выйти из голосового канала 🎙️\n'
                '`/echo` > Отправить сообщение от имени Полины 📢\n'
                '`/stay` > Оставить Полину в голосовом канале 🙏\n'
                '`/create_role` > Создание новой роли 🛠️\n'
                '`/assign_role` > Выдача роли пользователю 🤝\n'
                '`/setroleap` > Установить роль для Автовыдачи 👥\n'
                '`/remove_role` > Удаление роли у пользователя ❌\n'
                '`/setcolorrole` > Изменить цвет роли 🌈\n'
                '`/voting` > Провести голосование 🗳️ \n'
                '`/send-dm` > Отправить в лс сообщение от имени бота 💬\n'
                '`/voicemute` > Mute пользователя в голосовых каналах 😶\n'
                '`/unvoicemute` > unMute пользователя в голосовых каналах🎙️\n'
                '`/mchat` > Блокировка чата пользователю 🔒\n'
                '`/unmchat` > Снять блокировку чата у пользователя 🔓\n'
                '`/mchatinfo` > Показать список пользователей в муте 📋\n'
            ))
            await interaction.response.edit_message(embed=embed)
        if "Level" in self.values:
            embed = disnake.Embed(color=disnake.Color.purple())
            embed.add_field(name='Общее', value=(
                '`/reset` > Сбросить уровни и опыт всех пользователей \n'
                '`/setlevel` > Установить уровень пользователю \n'
                '`/addxp` > Добавить опыт пользователю \n'
            ))
            await interaction.response.edit_message(embed=embed)
        if "Developers" in self.values:
            embed = disnake.Embed(color=disnake.Color.purple())
            embed.add_field(name='Общее', value=(
                '`/restart` > For developers | Выполняет полную перезагрузку бота.\n'
                '`/status` > For developers | Информация о статусе бота.\n'
                '`/...` > в разработке...\n'
            ))
            await interaction.response.edit_message(embed=embed)
        if "Общее" in self.values:
            embed = disnake.Embed(color=disnake.Color.blue())
            embed.add_field(name='Общее', value=(
                '`/help` > Посмотреть все команды 👀\n'
                '`/dice` > Играть в Dice 🎲\n'
                '`/user_agreement` > Пользовательское соглашение 📜\n'
                '`/profile` > Узнать свою статистику 📊\n'
                '`/calculate` > Открыть калькулятор 🧮\n'
                '`/level` > Узнать свой уровень 📈\n'
                '`/avatar` > Посмотреть аватар пользователя 👤\n'
                '`/short` > Сократить URL-адрес 🔗\n'
                '`/server` > Просмотр информации о сервере 🖥️\n'
                '`/ping` > Проверка бота на работу 🏓\n'
                '`/nitro` > Генерирует Discord Nitro 🎁\n'
                '`/ticket` > Создать тикет для связи с администрацией 📲\n'
                '`/reverse` > Отзеркалить текст. 🔁\n'
                '`/qrcode` > Генерировать QR-код.. \n'
            ))
            await interaction.response.edit_message(embed=embed)
        if "Животные" in self.values:
            embed = disnake.Embed(color=disnake.Color.green())
            embed.add_field(name='Животные', value=(
                '`/dog` > в разработке...\n'
            ))
            await interaction.response.edit_message(embed=embed)
        if "NSFW" in self.values:
            embed = disnake.Embed(color=disnake.Color.red())
            embed.add_field(name='NSFW', value=(
                '`/waifu` > 18+ картинки / GIF 🍑\n'
                '`/blowjob` > 18+ картинки / GIF 🍆\n'
                '`/trap` > 18+ картинки / GIF 🚻\n'
                '`/neko` > 18+ картинки / GIF 😺\n'
                '`/sex` > 18+ картинки / GIF 🍌\n'
                '`/solo` > 18+ картинки / GIF 👄'
            ))
            await interaction.response.edit_message(embed=embed)
        if "Информация" in self.values:
            embed = disnake.Embed(color=disnake.Color.green())
            embed.add_field(name='Информация', value=(
                '`/news` > в разработке...\n'
            ))
            await interaction.response.edit_message(embed=embed)
        if "Premium" in self.values:
            embed = disnake.Embed(color = disnake.Color.dark_theme())
            embed.add_field(name='Premium', value=(
                '`/premium` > в разработке...\n'
                '`/buy-premium` > в разработке...\n'
            ))
            await interaction.response.edit_message(embed=embed)

        if "Экономика" in self.values:
            embed = disnake.Embed(color=disnake.Color.gold())
            embed.add_field(name='Экономика', value=(
                '`/balance` > Показать баланс 💵\n'
                '`/daily` > Получить ежедневные Poli-coins 💰\n'
                '`/dice` > Играть в Dice 🎲\n'
                '`/miner` > Работа шахтёра ⛏️ \n'
                '`/prostitute` > Работа проституткой 👠 \n'
                '`/programmer` > Работа программистом 💻\n'
                '`/transfer` > Перевести Poli-coins другому пользователю \n'
                '`/setbalance` > Установить баланс пользователя \n'
                '`/leaderboard` > Показать топ пользователей по балансу 🏆\n'
            ))
            await interaction.response.edit_message(embed=embed)

def setup(bot):
    bot.add_cog(helpc(bot))