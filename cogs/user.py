import disnake
from disnake.ext import commands
from random import randint, random
from asyncio import sleep
import typing
import requests
import random
from datetime import datetime
import qrcode



class user(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client


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
    
        embed = disnake.Embed(title="Пользовательское соглашение", description=f"```{message}```", color=0xCD853F)
        embed.add_field(name="Polina bot 2024 © Все права защищены",value='',inline=False)
    
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    

    @commands.slash_command(name="calculate", description="Калькулятор")
    async def calc(self, inter, example: str):
            example_calc = example.replace("^", "**")
            example_text = example.replace("**", "^")
            await inter.response.send_message(embed=disnake.Embed(title='Калькулятор', description=f"{example_text} = {eval(example_calc)}", color=0xCD853F), ephemeral=True)




    @commands.slash_command(name="chill", description="Узнать длину своего члена")
    async def your_dick(ctx):
        result1 = (
            list(range(-3, 5)) + list(range(5, 10)) * 4 + list(range(10, 15)) * 6 + list(range(15, 20)) * 2 + list(range(20, 30))
        )
        height = random.choice(result1)
        embed = disnake.Embed(description=f"@{ctx.author.display_name}, длина твоего члена - {height} см", color=0xCD853F)
        await ctx.response.send_message(embed=embed, ephemeral=True)
        random.seed()


    @commands.slash_command(name="avatar", description="Посмотреть аватар пользователя")
    async def avatar(self, ctx, user: typing.Optional[disnake.Member] = None):
        if not user:
            user = ctx.author
        avatar_url = user.avatar.url
        embed = disnake.Embed(title=f"Аватар {user.display_name} :frame_photo:", color=0xCD853F)
        embed.set_image(url=avatar_url)
        await ctx.send(embed=embed, ephemeral=True)


    @commands.slash_command(name="server", description="Просмотр информации о сервере")
    async def server_info(self, ctx):
        guild = ctx.guild
        joined_at = guild.me.joined_at.strftime("%d.%m.%Y %H:%M:%S")
        mention_roles = ', '.join([role.mention for role in guild.roles])
        top_role = guild.roles[-1].mention

        embed = disnake.Embed(title=f"Информация о сервере {guild.name} :desktop:", color=0xCD853F)
        embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="ID :id:", value=guild.id, inline=True)
        embed.add_field(name="Создан :date:", value=guild.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=True)
        embed.add_field(name="Владелец :crown:", value=guild.owner.display_name, inline=True)
        embed.add_field(name='Присоединился', value=joined_at, inline=True)
        embed.add_field(name="Участники :busts_in_silhouette:", value=str(guild.member_count), inline=True)
        embed.add_field(name='Топ роли', value=top_role, inline=True)
        embed.add_field(name="Каналы :loudspeaker:", value=f"Текстовые: {len(guild.text_channels)}\n"
                                                          f"Голосовые: {len(guild.voice_channels)}", inline=True)
        embed.add_field(name='Роли', value=mention_roles, inline=True)
        
        embed.set_footer(text='Polina bot | ©2024', icon_url=ctx.author.avatar.url) 

        await ctx.send(embed=embed, ephemeral=True)



    @commands.slash_command(name="short", description="Сократить URL-адрес")
    async def shorten_url(ctx: disnake.ApplicationCommandInteraction, url: str):
        response = requests.get(f"https://tinyurl.com/api-create.php?url={url}")
        embed = disnake.Embed(title="Сокращенный URL-адрес",
                              description=f"Ваш сокращенный URL-адрес: {response.text}",
                              color=0xCD853F)
        embed.set_footer(text='Polina bot | ©2024', icon_url=ctx.author.avatar.url)
        await ctx.response.send_message(embed=embed, ephemeral=True)


    

    @commands.slash_command(name="ping", description="Проверка бота на работу")
    async def botinfo(ctx):
        bot = ctx.bot

        uptime = datetime.utcnow() - bot.user.created_at.replace(tzinfo=None)
        uptime_str = f"{uptime.days} дней {uptime.seconds // 3600} часа {(uptime.seconds // 60) % 60} минуты {uptime.seconds % 60} секунды"

        embed = disnake.Embed(title="Pong! :ping_pong:", color=0xCD853F)
        embed.add_field(name="Работаю 🕒", value=uptime_str + "\n", inline=False)
        embed.add_field(name="Задержка 🚀", value=f"{round(bot.latency * 1000)} мс\n", inline=False)
        embed.add_field(name="Задержка хостинга 🌐", value=f"{round(bot.ws.latency * 1000)} мс\n", inline=False)

        await ctx.send(embed=embed, ephemeral=True)


    @commands.slash_command(name="nitro", description="Генерирует Discord Nitro")
    async def generate_nitro_link(self, ctx):

        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        
        link = ''.join(random.choices(alphabet, k=16))
        embed = disnake.Embed(title="Discord Nitro", description=f"https://discord.gift/{link}", color=0xCD853F)
        await ctx.send(embed=embed, ephemeral=True)
        



    @commands.slash_command(name='8ball', description= 'Задать вопрос магическому шару.')
    async def eight_ball(self, ctx, *, question: str):
        responses = [
            "Бесспорно",
            "Предрешено",
            "Никаких сомнений",
            "Определённо да",
            "Можешь быть уверен в этом",
            "Мне кажется — «да»",
            "Вероятнее всего",
            "Хорошие перспективы",
            "Знаки говорят — «да»",
            "Да",
            "Пока не ясно, попробуй снова",
            "Спроси позже",
            "Лучше не рассказывать",
            "Сейчас нельзя предсказать",
            "Сконцентрируйся и спроси опять",
            "Даже не думай",
            "Мой ответ — «нет»",
            "По моим данным — «нет»",
            "Перспективы не очень хорошие",
            "Весьма сомнительно"
        ]
        response = random.choice(responses)
        embed = disnake.Embed(title="Магический шар 🎱", description=f"Вопрос: {question}\nОтвет: {response}", color=0xCD853F)
        await ctx.send(embed=embed, ephemeral=True)




    @commands.slash_command(name='reverse', description='Отзеркалить текст.')
    async def reverse_text(self, ctx, *, текст: str):
        reversed_text = текст[::-1]
        emoji = "🔁"  
        embed = disnake.Embed(title=f"{emoji} Отзеркаленный текст", description=reversed_text, color=0xCD853F)
        await ctx.send(embed=embed, ephemeral=True)




    @commands.slash_command(name="qrcode", description="Генерировать QR-код.")
    async def generate_qr(self, ctx, link: str):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        with open("qrcode.png", "wb") as img_file:
            qr_img.save(img_file)

        embed = disnake.Embed(title="QR-код", color=0xCD853F)
        embed.set_image(url="attachment://qrcode.png")

        await ctx.send(file=disnake.File("qrcode.png", filename="qrcode.png"), embed=embed, ephemeral=True)




def setup(bot: commands.Bot):
    bot.add_cog(user(bot))