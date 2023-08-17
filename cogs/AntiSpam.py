import disnake
from disnake.ext import commands
import time


class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_cooldown = 5
        self.message_logs = {}

    async def log_message(self, message):
        guild_id = message.guild.id
        channel_id = message.channel.id
        author_id = message.author.id
        content = message.content

        if guild_id not in self.message_logs:
            self.message_logs[guild_id] = {}

        if channel_id not in self.message_logs[guild_id]:
            self.message_logs[guild_id][channel_id] = []

        self.message_logs[guild_id][channel_id].append({
            'author_id': author_id,
            'content': content,
            'timestamp': time.time()
        })

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        await self.log_message(message)

        guild_id = message.guild.id
        channel_id = message.channel.id
        author_id = message.author.id
        content = message.content

        if guild_id in self.message_logs and channel_id in self.message_logs[guild_id]:
            recent_messages = self.message_logs[guild_id][channel_id]
            current_time = time.time()

            recent_messages = [msg for msg in recent_messages if current_time - msg['timestamp'] < self.spam_cooldown]

            self.message_logs[guild_id][channel_id] = recent_messages

            if len(recent_messages) > 5:
                try:
                    await message.delete()

                    warn_embed = disnake.Embed(
                        title="⚠️ Предупреждение за спам",
                        description=f"{message.author.mention}, ваши сообщения удаляются из-за подозрения в спаме.",
                        color=0xCD853F
                    )
                    await message.author.send(embed=warn_embed)
                except disnake.NotFound:
                    pass

def setup(bot):
    bot.add_cog(AntiSpam(bot))
