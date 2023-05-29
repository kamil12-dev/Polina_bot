import disnake
from disnake.ext import commands
import aiohttp
from asyncio import sleep
from random import randint, random


class nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="18+ картинки / GIF")
    @commands.is_nsfw()
    async def waifu(self, ctx):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                request = await session.get('https://api.waifu.pics/nsfw/waifu')
                newjson = await request.json()
                pat = disnake.Embed(title = f"{ctx.author.name} Вот это кайф!", color = 0x38f09a)
            pat.set_footer(text="Polina bot © 2023 Все права защищены")
            pat.set_image(url=newjson['url'])
            await ctx.send(embed = pat)


    @commands.slash_command(description="18+ картинки / GIF")
    @commands.is_nsfw()
    async def blowjob(self, ctx):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                request = await session.get('https://api.waifu.pics/nsfw/blowjob')
                blowjobjson = await request.json()
                blowjob = disnake.Embed(title = f"{ctx.author.name} Вот это кайф!", color = 0x38f09a)
            blowjob.set_footer(text="Polina bot © 2023 Все права защищены")
            blowjob.set_image(url=blowjobjson['url'])
            await ctx.send(embed = blowjob)


    @commands.slash_command(description="18+ картинки / GIF")
    @commands.is_nsfw()
    async def trap(self, ctx):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                request = await session.get('https://api.waifu.pics/nsfw/trap')
                trapjson = await request.json()
                trap = disnake.Embed(title = f"{ctx.author.name} Вот это кайф!", color = 0x38f09a)
            trap.set_footer(text="Polina bot © 2023 Все права защищены")
            trap.set_image(url=trapjson['url'])
            await ctx.send(embed = trap)

    @commands.slash_command(description="18+ картинки / GIF")
    @commands.is_nsfw()
    async def neko(self, ctx):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                request = await session.get('https://api.waifu.pics/nsfw/neko')
                nekojson = await request.json()
                neko = disnake.Embed(title = f"{ctx.author.name} Вот это кайф!", color = 0x38f09a)
            neko.set_footer(text="Polina bot © 2023 Все права защищены")
            neko.set_image(url=nekojson['url'])
            await ctx.send(embed = neko)

    @commands.slash_command(description="18+ картинки / GIF")
    @commands.is_nsfw()
    async def sex(self, ctx):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                request = await session.get('https://purrbot.site/api/img/nsfw/fuck/gif')
                sexjson = await request.json()
                sex = disnake.Embed(title = f"{ctx.author.name} Вот это кайф!", color = 0x38f09a)
            sex.set_footer(text="Polina bot © 2022 Все права защищены")
            sex.set_image(url=sexjson['link'])
            await ctx.send(embed = sex)

    @commands.slash_command(description="18+ картинки / GIF")
    @commands.is_nsfw()
    async def solo(self, ctx):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as session:
                request = await session.get('https://purrbot.site/api/img/nsfw/solo/gif')
                solojson = await request.json()
                solo = disnake.Embed(title = f"{ctx.author.name} Вот это кайф!", color = 0x38f09a)
            solo.set_footer(text="Polina bot © 2022 Все права защищены")
            solo.set_image(url=solojson['link'])
            await ctx.send(embed = solo)

    @waifu.error
    async def waifu_error(self, ctx, error):
        if isinstance(error, commands.errors.NSFWChannelRequired):
            embed=disnake.Embed(title = "Этот канал не NSFW", description = f"Этот канал не имеет отметку NSFW!")
            return await ctx.send(embed=embed)

    @blowjob.error
    async def blowjob_error(self, ctx, error):
        if isinstance(error, commands.errors.NSFWChannelRequired):
            embed=disnake.Embed(title = "Этот канал не NSFW", description = f"Этот канал не имеет отметку NSFW!")
            return await ctx.send(embed=embed)

    @trap.error
    async def trap_error(self, ctx, error):
        if isinstance(error, commands.errors.NSFWChannelRequired):
            embed=disnake.Embed(title = "Этот канал не NSFW", description = f"Этот канал не имеет отметку NSFW!")
            return await ctx.send(embed=embed)


    @neko.error
    async def neko_error(self, ctx, error):
        if isinstance(error, commands.errors.NSFWChannelRequired):
            embed=disnake.Embed(title = "Этот канал не NSFW", description = f"Этот канал не имеет отметку NSFW!")
            return await ctx.send(embed=embed)

    @sex.error
    async def sex_error(self, ctx, error):
        if isinstance(error, commands.errors.NSFWChannelRequired):
            embed=disnake.Embed(title = "Этот канал не NSFW", description = f"Этот канал не имеет отметку NSFW!")
            return await ctx.send(embed=embed)

    @solo.error
    async def solo_error(self, ctx, error):
        if isinstance(error, commands.errors.NSFWChannelRequired):
            embed=disnake.Embed(title = "Этот канал не NSFW", description = f"Этот канал не имеет отметку NSFW!")
            return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(nsfw(bot))