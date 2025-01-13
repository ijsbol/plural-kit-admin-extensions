from sqlite3 import Row

from aiosqlite import connect as aio_connect
from discord import Interaction, Permissions, Role
from discord.app_commands import (
    AppCommandContext,
    AppInstallationType,
    Group,
)
from discord.ext.commands import Cog


from bot import PluralAdminExtensions
from utils.env import DATABASE_NAME


class PluralKitAdminExtensionsConfig(Cog):
    def __init__(self, bot: PluralAdminExtensions) -> None:
        self.bot = bot

    config = Group(
        name="config",
        description="Setup your PK Admin Extensions config",
        allowed_contexts=AppCommandContext(guild=True),
        allowed_installs=AppInstallationType(guild=True),
        default_permissions=Permissions(administrator=True),
    )

    config_role_lock = Group(
        parent=config,
        name="proxy-role-lock",
        description="Set/delete a role that users are required to have to use PluralKit proxying in this server.",
    )

    @config_role_lock.command(
        name="set",
        description="Set the role that users are required to have to use PluralKit proxying in this server.",
    )
    async def config_role_lock_set(self, interaction: Interaction[PluralAdminExtensions], role: Role) -> None:
        query = """
            INSERT INTO RoleLock (
                guild_id,
                role_id
            ) VALUES (?, ?)
            ON CONFLICT(guild_id)
                DO UPDATE SET role_id=?;
        """
        args = (str(interaction.guild_id), str(role.id), str(role.id))
        async with aio_connect(DATABASE_NAME) as db:
            db.row_factory = Row
            await db.execute(query, args)
            await db.commit()

        if interaction.guild_id in self.bot.cache.keys():
            del self.bot.cache[interaction.guild.id]

        return await interaction.response.send_message(
            content=f"Users will now be required to have the {role.mention} role in order to use PluralKit proxying on this server.",
            ephemeral=True,
        )

    @config_role_lock.command(
        name="delete",
        description="Allow all users to use PluralKit proxying again on this server.",
    )
    async def config_role_lock_delete(self, interaction: Interaction[PluralAdminExtensions]) -> None:
        query = """
            INSERT INTO RoleLock (
                guild_id,
                role_id
            ) VALUES (?, ?)
            ON CONFLICT(guild_id)
                DO UPDATE SET role_id=?;
        """
        args = (str(interaction.guild_id), None, None)
        async with aio_connect(DATABASE_NAME) as db:
            db.row_factory = Row
            await db.execute(query, args)
            await db.commit()

        if interaction.guild_id in self.bot.cache.keys():
            del self.bot.cache[interaction.guild.id]

        return await interaction.response.send_message(
            content=f"All users on this server can now use PluralKit proxying without needing to have a role.",
            ephemeral=True,
        )

    @config_role_lock.command(
        name="set-alert-message",
        description="Set the message sent to users that attempt to proxy without the bypass role.",
    )
    async def config_role_lock_delete(self, interaction: Interaction[PluralAdminExtensions], message: str) -> None:
        query = """
            INSERT INTO RoleLock (
                guild_id,
                alert_message
            ) VALUES (?, ?)
            ON CONFLICT(guild_id)
                DO UPDATE SET alert_message=?;
        """
        args = (str(interaction.guild_id), message, message)
        async with aio_connect(DATABASE_NAME) as db:
            db.row_factory = Row
            await db.execute(query, args)
            await db.commit()

        if interaction.guild_id in self.bot.cache.keys():
            del self.bot.cache[interaction.guild.id]

        return await interaction.response.send_message(
            content=f"Users will now be sent this message when attempting to proxy without the bypass role.\n> {message}",
            ephemeral=True,
        )

    @config_role_lock.command(
        name="set-alert-message-auto-delete",
        description="Set the time taken to delete the alert message.",
    )
    async def config_role_lock_delete(self, interaction: Interaction[PluralAdminExtensions], seconds: int) -> None:
        query = """
            INSERT INTO RoleLock (
                guild_id,
                delete_after
            ) VALUES (?, ?)
            ON CONFLICT(guild_id)
                DO UPDATE SET delete_after=?;
        """
        args = (str(interaction.guild_id), seconds, seconds)
        async with aio_connect(DATABASE_NAME) as db:
            db.row_factory = Row
            await db.execute(query, args)
            await db.commit()

        if interaction.guild_id in self.bot.cache.keys():
            del self.bot.cache[interaction.guild.id]

        return await interaction.response.send_message(
            content=f"The alert message will now auto delete after **{seconds} seconds**.",
            ephemeral=True,
        )


async def setup(bot: PluralKitAdminExtensionsConfig) -> None:
    await bot.add_cog(PluralKitAdminExtensionsConfig(bot))
