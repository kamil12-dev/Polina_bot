import disnake
from disnake.ext import commands
from PIL import Image, ImageChops, ImageDraw, ImageFont
from io import BytesIO
import aiohttp
import os

def circle(pfp, size=(215, 215)):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    @commands.slash_command(name='profile', description='Узнать свою статистику', private=True)
    async def test(self, ctx):
        member = ctx.author

        name, Id, status = str(member), str(member.id)[:12], str(member.status).upper()
        created_at = member.created_at.strftime("%a %b\n%B %Y")
        joined_at = member.joined_at.strftime("%a %b\n%B %Y")
        money, level = "2323232", "100"

        base_path = os.path.join(os.getcwd())
        base = Image.open(os.path.join(base_path, "base.png")).convert("RGBA")
        background = Image.open(os.path.join(base_path, "bg.png")).convert("RGBA")

        avatar_url = str(member.avatar.url)
        async with self.session.get(avatar_url) as response:
            avatar_bytes = await response.read()
        pfp = Image.open(BytesIO(avatar_bytes)).convert("RGBA")

        name = f"{name[:16]}.." if len(name) > 16 else name

        draw = ImageDraw.Draw(base)
        pfp = circle(pfp, (215, 215))
        font_size = 38
        font = ImageFont.truetype("arial.ttf", font_size)

        draw.text((280, 240), name, font=font)
        draw.text((270, 315), member.display_name, font=font)
        draw.text((65, 490), Id, font=font)
        draw.text((405, 490), status, font=font)
        draw.text((65, 635), money, font=font)
        draw.text((405, 635), level, font=font)
        draw.text((65, 770), created_at, font=font)
        draw.text((405, 770), joined_at, font=font)
        base.paste(pfp, (56, 158), pfp)

        background.paste(base, (0, 0), base)

        with BytesIO() as a:
            background.save(a, "PNG")
            a.seek(0)
            await ctx.send(file=disnake.File(a, "profile.png"), ephemeral=True)

def setup(bot):
    bot.add_cog(Profile(bot))