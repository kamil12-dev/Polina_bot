import disnake
from disnake.ext import commands
import requests
from disnake import utils

class WeatherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = "ba58dcebaa8a509e3c93aeddc50c3285"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"

    @commands.slash_command(
        name="weather",
        description="Получить информацию о погоде в заданном городе.",
    )
    async def weather(self, inter, город: str):
        city_name = город
        complete_url = f"{self.base_url}appid={self.api_key}&q={city_name}"

        response = requests.get(complete_url)
        x = response.json()

        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature_celsius = str(round(current_temperature - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]

            z = x["weather"]

            embed = disnake.Embed(
                title=f"Погода в городе {city_name}",
                color=0xCD853F,
                timestamp=utils.utcnow(),
            )
            embed.add_field(name="Температура(C)", value=f"**{current_temperature_celsius}°C**", inline=False)
            embed.add_field(name="Влажность(%)", value=f"**{current_humidity}%**", inline=False)
            embed.add_field(name="Атмосферное давление(гПа)", value=f"**{current_pressure}гПа**", inline=False)
            embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
            embed.set_footer(text=f"Запрошено пользователем {inter.author.display_name}")
            await inter.response.send_message(embed=embed, ephemeral=True)
        else:
            await inter.response.send_message("Город не найден.")
            

def setup(bot):
    bot.add_cog(WeatherCog(bot))