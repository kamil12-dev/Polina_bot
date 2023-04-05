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
        
        commands_list = ["/kick", "/clear", "/ban", "/join", "/leave", "/help","/echo", "/daily", "/balance", "/game", "/stay", "/user_agreement", "/profile", "/restart", "/calculate"]
        descriptions_for_commands = [
            "Выгнать пользователя с сервера(Adm)",
            "Очистить чат(Adm)",
            "Забанить пользователя на сервере(Adm)",
            "Зайти в голосовой канал(Adm)",
            "Выйти в голосовой канал(Adm)",
            "Посмотреть все команды",
            "Отправить сообщение от имени Полины(Adm)",
            "Получить ежедневные Poli-coins",
            "Показать баланс",
            "Играть в игры на Poli-coins",
            "Оставить Полину в голосовом канале(Adm)",
            "Пользовательское соглашение",
            "Узнать свою статистику",
            "Перезапуск бота(Adm)",
            "Открыть калькулятор"
        ]
    
        for command_name, description_command in zip(commands_list, descriptions_for_commands):
            embed.add_field(
                name=command_name,
                value=description_command,
                inline=False 
            )

        await ctx.send(embed=embed, ephemeral=True)


       

    @commands.slash_command(name='profile', description='Узнать свою статистику')
    async def profile(ctx, member:disnake.Member):
        created_at = member.created_at 
        joined_at = str(member.joined_at).split()[0].replace('-', '.') 
        roles = member.roles 
        mention_roles = ', '.join([role.mention for role in roles]) 
        top_role = member.top_role.mention 
        embed = disnake.Embed(title=f'User {member.name}', color=0x9b59b6)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name='ID', value=member.id, inline=True)
        embed.add_field(name='Nickname', value=member.nick or member.name, inline=True)
        embed.add_field(name='Created at', value=created_at, inline=True)
        embed.add_field(name='Присоединился', value=joined_at, inline=True)
        embed.add_field(name='Roles', value=mention_roles, inline=True)
        embed.add_field(name='Top role', value=top_role, inline=True)
        embed.add_field(name='Bot', value=member.bot, inline=True)
        embed.set_footer(text='Polina bot | ©', icon_url=ctx.author.avatar.url) 
        await ctx.send(embed=embed, ephemeral=True) 




    @commands.slash_command(name="user_agreement", description="Пользовательское соглашение")
    async def agree_command(self, interaction: disnake.ApplicationCommandInteraction):
        message = ''' 
🙂Пользовательское соглашение Polina_bot🙂
    
💜Добро пожаловать в Polina bot💜 

🖊Этот бот был разработан для модерации улучшения универсальных функций на сервере. Пользуясь нашим ботом, вы автоматически соглашаетесь с нашими условиями использования.
    
🛡 Ваша ответственность.
    
1️⃣ Вы должны быть ответственны за все действия,совершенные во время использования Polina bot.
2️⃣ Нельзя использовать бота для спама или распространения незаконной информации.
3️⃣ Мы не несем ответственности за любую потерю данных, вызванную неисправностью наших систем или отказом бота в работе.
    
🔒 Права нашего бота.
    
1️⃣ Мы имеем право в любое время изменить или удалить любые функции нашего бота без предварительного уведомления.
2️⃣ Мы также имеем право заблокировать доступ к нашему боту пользователям, нарушающим наши условия использования.
3️⃣ Мы собираем и храним определенную информацию о пользователях, чтобы улучшить работу бота и его функциональность.
    
⛔️ Запрет на коммерческое использование.
    
🖤 Нельзя использовать Polina bot или его функции для коммерческих целей без нашего явного письменного согласия.🖤
    
💎Спасибо за использование Polina bot.💎 

💎Мы надеемся, что наш бот будет полезен вам. Если у вас есть вопросы или предложения по улучшению нашего бота, пожалуйста, свяжитесь с нами.💎
        '''
    
        embed = disnake.Embed(title="Пользовательское соглашение", description=f"```{message}```", color=0x9b59b6)
        embed.add_field(name="Polina bot 2022-2023 © Все права защищены",value='',inline=False)
    
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    

    @commands.slash_command(name="calculate", description="Калькулятор")
    async def calc(self, inter, example: str):
            example_calc = example.replace("^", "**")
            example_text = example.replace("**", "^")
            await inter.response.send_message(embed=disnake.Embed(title='Калькулятор', description=f"{example_text} = {eval(example_calc)}", color=0x7788ff), ephemeral=True)



def setup(bot: commands.Bot):
    bot.add_cog(user(bot))