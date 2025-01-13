from typing import Any
from discord import Intents
from discord.ext.commands import AutoShardedBot, Context, dm_only, when_mentioned

from utils.env import DISCORD_BOT_TOKEN, YOUR_DISCORD_USER_ID
from utils.database import check_sqlite_connection
from utils.types import RoleLock


class PluralAdminExtensions(AutoShardedBot):
    def __init__(self, intents: Intents, *args, **kwargs):
        self.cache: dict[int, RoleLock] = {}
        super().__init__(
            intents=intents,
            command_prefix=when_mentioned,
            *args,
            **kwargs,
        )

    async def setup_hook(self):
        check_sqlite_connection()
        await self.load_extension('cogs.check')
        await self.load_extension('cogs.config')


intents = Intents.none()
intents.dm_messages = True
intents.guild_messages = True
intents.webhooks = True
intents.members = True
intents.guilds = True
bot = PluralAdminExtensions(intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command(name="sync")
@dm_only()
async def sync_command(ctx: Context[PluralAdminExtensions]) -> None:
    if ctx.author.id == YOUR_DISCORD_USER_ID:
        await bot.tree.sync()
        await ctx.reply("Synced!")


if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
