import discord
from discord.ext import commands
from discord import app_commands
import config_manager


class Setup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="setup-role",
        description="Elige el rol que se dará al verificarse."
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_role(self, interaction: discord.Interaction, rol: discord.Role):
        if rol >= interaction.guild.me.top_role:
            await interaction.response.send_message(
                f"❌ No puedo asignar **{rol.name}** porque está por encima de mi rol más alto.",
                ephemeral=True
            )
            return

        config_manager.update_guild_config(interaction.guild_id, "verify_role_id", rol.id)
        await interaction.response.send_message(
            f"✅ Rol de verificación actualizado a **{rol.name}**.", ephemeral=True
        )

    @app_commands.command(
        name="setup-log",
        description="Elige el canal donde se enviarán los logs de verificación."
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_log(self, interaction: discord.Interaction, canal: discord.TextChannel):
        config_manager.update_guild_config(
            interaction.guild_id, "verify_log_channel_id", canal.id
        )
        await interaction.response.send_message(
            f"✅ Canal de logs de verificación: {canal.mention}", ephemeral=True
        )

    @app_commands.command(
        name="setup-info",
        description="Muestra la configuración actual del bot en este servidor."
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_info(self, interaction: discord.Interaction):
        config = config_manager.get_guild_config(interaction.guild_id)

        role_id = config.get("verify_role_id")
        log_id  = config.get("verify_log_channel_id")

        role    = interaction.guild.get_role(int(role_id)) if role_id else None
        channel = interaction.guild.get_channel(int(log_id)) if log_id else None

        embed = discord.Embed(
            title="⚙️ Configuración del Bot",
            color=discord.Color.blurple()
        )
        embed.add_field(
            name="🎭 Rol de verificación",
            value=role.mention if role else "❌ No configurado",
            inline=False
        )
        embed.add_field(
            name="📋 Canal de logs",
            value=channel.mention if channel else "❌ No configurado",
            inline=False
        )
        embed.set_footer(text=interaction.guild.name)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="setup-reset",
        description="Resetea TODA la configuración del bot en este servidor."
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_reset(self, interaction: discord.Interaction):
        config_manager.set_guild_config(interaction.guild_id, {})
        await interaction.response.send_message(
            "🗑️ Configuración reseteada completamente.", ephemeral=True
        )

    async def cog_app_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "🚫 Necesitas permisos de **Administrador** para usar este comando.",
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Setup(bot))
