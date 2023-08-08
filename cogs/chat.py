#import disnake
#from disnake.ext import commands
#from disnake import OptionType, Embed
#
#import openai
#
#openai.api_key = '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'
#
#class chat(commands.Cog):
#    def __init__(self, bot):
#        self.bot = bot
#
#    @commands.slash_command(
#        name='chat',
#        description='ChatGPT',
#        options=[
#            disnake.Option(
#                name='message',
#                description='Сообщение для чата с ботом',
#                type=OptionType.string,
#                required=True
#            )
#        ]
#    )
#    async def chat(self, inter, message: str):
#        await inter.response.defer(ephemeral=True)
#
#        response = openai.Completion.create(
#            engine='text-davinci-003',
#            prompt=message,
#            max_tokens=2000,
#            temperature=0.7,
#            n=1,
#            stop=None,
#        )
#
#        full_response = response.choices[0].text.strip()
#
#        if len(full_response) <= 2000:
#            if response.choices[0].finish_reason == 'stop' and response.choices[0].index == 0:
#                embed = Embed(title="ChatGPT", description=f"```{full_response}```", color=0xCD853F)
#            else:
#                embed = Embed(title="ChatGPT", description=full_response, color=0xCD853F)
#        else:
#            embed = Embed(title="ChatGPT", description=f"{full_response[:2000]}...\n\n[Описание обрезано из-за ограничения Discord на 2000 символов.]", color=0xCD853F)
#
#        if not inter.responded:
#            await inter.send(embed=embed, ephemeral=True)
#
#
#def setup(bot):
#    bot.add_cog(chat(bot))