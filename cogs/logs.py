import disnake
from disnake.ext import commands


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            overwrites = {
                guild.default_role: disnake.PermissionOverwrite(read_messages=False),
                guild.me: disnake.PermissionOverwrite(read_messages=True, read_message_history=True)
            }

            category = disnake.utils.get(guild.categories, name="Логи")
            if not category:
                category = await guild.create_category("Логи")

            admin_channel = disnake.utils.get(category.text_channels, name="admin-logs")
            if not admin_channel:
                admin_channel = await category.create_text_channel("admin-logs", overwrites=overwrites)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = disnake.utils.get(member.guild.text_channels, name="admin-logs")
        if channel:
            embed = disnake.Embed(description=f"👋 Пользователь {member.mention} присоединился к серверу.", color=0xCD853F)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = disnake.utils.get(member.guild.text_channels, name="admin-logs")
        if channel:
            embed = disnake.Embed(description=f"😢 Пользователь {member.mention} покинул сервер.", color=0xCD853F)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            role_changes = []
            for role in before.roles:
                if role not in after.roles:
                    role_changes.append(f"🔴 Убрана роль {role.mention}")
            for role in after.roles:
                if role not in before.roles:
                    role_changes.append(f"🟢 Добавлена роль {role.mention}")
            if role_changes:
                channel = disnake.utils.get(before.guild.text_channels, name="admin-logs")
                if channel:
                    role_changes_str = "\n".join(role_changes)
                    executor = None
                    for role in before.roles:
                        if role not in after.roles:
                            changes = await after.guild.audit_logs(limit=1, action=disnake.AuditLogAction.member_role_update).flatten()
                            executor = changes[0].user.mention if changes else "Неизвестно"
                            break
                    author = after
                    embed = disnake.Embed(description=f"👥 Пользователь {author.mention} изменил роли:\n{role_changes_str}\n\n👤 Выполнил: {executor}", color=0xCD853F)
                    await channel.send(embed=embed)

        if before.display_name != after.display_name:
            channel = disnake.utils.get(before.guild.text_channels, name="admin-logs")
            if channel:
                executor = before.guild.me.mention
                author = after
                embed = disnake.Embed(description=f"📝 Пользователь {author.mention} изменил никнейм: {before.display_name} -> {after.display_name}\n👤 Выполнил: {executor}", color=0xCD853F)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.avatar.url != after.avatar.url:
            channel = disnake.utils.get(after.mutual_guilds[0].text_channels, name="admin-logs")
            if channel:
                embed = disnake.Embed(description=f"📷 Пользователь {after.mention} изменил аватарку.", color=0xCD853F)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild:
            channel = disnake.utils.get(message.guild.text_channels, name="admin-logs")
            if channel:
                author = message.author
                deleted_messages = await message.channel.purge(limit=100, before=message, check=lambda m: m.author == author)
                deleted_messages_content = "\n".join([f"{m.content} ({m.created_at})" for m in deleted_messages])
                embed = disnake.Embed(description=f"🗑️ Пользователь {message.author.mention} удалил сообщение:\n{message.content}\n\n📄 Количество удаленных сообщений: {len(deleted_messages)}\n\n📝 Удаленные сообщения:\n{deleted_messages_content}", color=0xCD853F)
                await channel.send(embed=embed)

                log_channel = disnake.utils.get(message.guild.text_channels, name="admin-logs")
                if log_channel:
                    embed = disnake.Embed(description=f"🗑️ Пользователь {message.author.mention} удалил сообщение:\n{message.content}\n\n📄 Количество удаленных сообщений: {len(deleted_messages)}", color=0xCD853F)
                    await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel:
            channel = disnake.utils.get(member.guild.text_channels, name="admin-logs")
            if channel:
                if before.channel:
                    embed = disnake.Embed(description=f"🔊 Пользователь {member.mention} покинул голосовой канал {before.channel.name}.", color=0xCD853F)
                    await channel.send(embed=embed)
                if after.channel:
                    embed = disnake.Embed(description=f"🔊 Пользователь {member.mention} присоединился к голосовому каналу {after.channel.name}.", color=0xCD853F)
                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if isinstance(channel, disnake.TextChannel):
            log_channel = disnake.utils.get(channel.guild.text_channels, name="admin-logs")
            if log_channel:
                embed = disnake.Embed(description=f"✅ Создан новый текстовый канал: {channel.mention}\n👤 Пользователь {channel.guild.me.mention}", color=0xCD853F)
                await log_channel.send(embed=embed)
        elif isinstance(channel, disnake.VoiceChannel):
            log_channel = disnake.utils.get(channel.guild.text_channels, name="admin-logs")
            if log_channel:
                embed = disnake.Embed(description=f"✅ Создан новый голосовой канал: {channel.mention}\n👤 Пользователь {channel.guild.me.mention}", color=0xCD853F)
                await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if isinstance(channel, disnake.TextChannel):
            log_channel = disnake.utils.get(channel.guild.text_channels, name="admin-logs")
            if log_channel:
                executor = channel.guild.me.mention
                embed = disnake.Embed(description=f"❌ Удален текстовый канал: {channel.mention}\n👤 Выполнил: {executor}", color=0xCD853F)
                await log_channel.send(embed=embed)
        elif isinstance(channel, disnake.VoiceChannel):
            log_channel = disnake.utils.get(channel.guild.text_channels, name="admin-logs")
            if log_channel:
                executor = channel.guild.me.mention
                embed = disnake.Embed(description=f"❌ Удален голосовой канал: {channel.mention}\n👤 Выполнил: {executor}", color=0xCD853F)
                await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if isinstance(before, disnake.TextChannel) and isinstance(after, disnake.TextChannel):
            if before.name != after.name:
                log_channel = disnake.utils.get(before.guild.text_channels, name="admin-logs")
                if log_channel:
                    embed = disnake.Embed(description=f"📝 Пользователь {before.guild.me.mention} изменил название текстового канала: {before.mention} -> {after.mention}", color=0xCD853F)
                    await log_channel.send(embed=embed)

        elif isinstance(before, disnake.VoiceChannel) and isinstance(after, disnake.VoiceChannel):
            if before.name != after.name:
                log_channel = disnake.utils.get(before.guild.text_channels, name="admin-logs")
                if log_channel:
                    embed = disnake.Embed(description=f"📝 Пользователь {before.guild.me.mention} изменил название голосового канала: {before.mention} -> {after.mention}", color=0xCD853F)
                    await log_channel.send(embed=embed)

        elif isinstance(before, disnake.TextChannel) and isinstance(after, disnake.VoiceChannel):
            log_channel = disnake.utils.get(before.guild.text_channels, name="admin-logs")
            if log_channel:
                embed = disnake.Embed(description=f"❗ Пользователь {before.guild.me.mention} изменил тип канала: Текстовый {before.mention} -> Голосовой {after.mention}", color=0xCD853F)
                await log_channel.send(embed=embed)

        elif isinstance(before, disnake.VoiceChannel) and isinstance(after, disnake.TextChannel):
            log_channel = disnake.utils.get(before.guild.text_channels, name="admin-logs")
            if log_channel:
                embed = disnake.Embed(description=f"❗ Пользователь {before.guild.me.mention} изменил тип канала: Голосовой {before.mention} -> Текстовый {after.mention}", color=0xCD853F)
                await log_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Logs(bot))
