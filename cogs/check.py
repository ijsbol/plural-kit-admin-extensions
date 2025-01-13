from sqlite3 import Row
from typing import cast

from aiohttp import ClientSession
from aiosqlite import connect as aio_connect
from discord import AllowedMentions, Message, Webhook
from discord.ext.commands import Cog


from bot import PluralAdminExtensions
from utils.constants import DEFAULT_ALERT_MESSAGE, DEFAULT_AUTO_DELETE_TIMEOUT, PLURAL_KIT_BOT_USER_ID
from utils.env import DATABASE_NAME
from utils.types import RoleLock


class PluralKitAdminExtensionsCheck(Cog):
    def __init__(self, bot: PluralAdminExtensions) -> None:
        self.bot = bot
        self._cached_webhooks: dict[int, dict[int, Webhook]] = {}
        self._session = ClientSession()

    @Cog.listener('on_message')
    async def ensure_proxy_is_allowed(self, message: Message) -> None:
        # Check message is a webhook response.
        if message.webhook_id is None or message.guild is None:
            return

        # Check message is a PluralKit proxy.
        if (
            message.webhook_id not in
            self._cached_webhooks.get(message.guild.id, {}).keys()
        ):
            self._cached_webhooks[message.guild.id] = {w.id: w for w in await message.guild.webhooks()}
        webhook = self._cached_webhooks[message.guild.id][message.webhook_id]
        if webhook.user.id != PLURAL_KIT_BOT_USER_ID:
            return

        # Checking the guild config is present and is cached.
        cached_guild_config = self.bot.cache.get(message.guild.id)
        if cached_guild_config is None:
            query = """
                SELECT * FROM RoleLock
                    WHERE guild_id=?
            """
            args = (str(message.guild.id),)
            async with aio_connect(DATABASE_NAME) as db:
                db.row_factory = Row
                result = await db.execute_fetchall(query, args)
                if len(result) == 0:
                    self.bot.cache[message.guild.id] = False
                    return
                self.bot.cache[message.guild.id] = cast(RoleLock, result[0])
                cached_guild_config = self.bot.cache[message.guild.id]
        if cached_guild_config == False:
            return

        # Check user has proxy permissions.
        async with self._session.get(
            url=f"https://api.pluralkit.me/v2/messages/{message.id}",
            headers={
                "User-Agent": "Bot (https://git.uwu.gal/plural-kit-admin-extensions)",
            },
        ) as resp:
            data = await resp.json()
            sender_id = int(data["sender"])

        sender = (
            message.guild.get_member(sender_id)
            or await message.guild.fetch_member(sender_id)
        )

        if not (
            cached_guild_config['role_id'] is not None
            and int(cached_guild_config['role_id']) not in [
                r.id for r in sender.roles
            ]
        ):
            return

        # User doesn't have proxy permisisons.
        default_message = DEFAULT_ALERT_MESSAGE.replace("(!role)", f"<@&{cached_guild_config['role_id']}>")
        await message.delete()
        await message.channel.send(
            content=f":bell: {sender.mention} - {cached_guild_config['alert_message'] or default_message}",
            allowed_mentions=AllowedMentions(users=True, roles=False, everyone=False),
            delete_after=cached_guild_config['delete_after'] or DEFAULT_AUTO_DELETE_TIMEOUT,
        )


async def setup(bot: PluralKitAdminExtensionsCheck) -> None:
    await bot.add_cog(PluralKitAdminExtensionsCheck(bot))
