import discord
from discord.ext import commands
from discord import app_commands
import config_manager
from datetime import datetime


# ── Vista persistente del botón de verificación ──────────────────────────────

class VerifyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="✅ Verificarme",
        style=discord.ButtonStyle.success,
        custom_id="verify_button"
    )
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        config = config_manager.get_guild_config(interaction.guild_id)
        role_id = config.get("verify_role_id")

        if not role_id:
            await interaction.response.send_message(
                "⚠️ No hay ningún rol de verificación configurado. "
                "Un administrador debe usar `/setup-role` primero.",
                ephemeral=True
            )
            return

        role = interaction.guild.get_role(int(role_id))
        if not role:
            await interaction.response.send_message(
                "⚠️ El rol configurado ya no existe. Contacta a un administrador.",
                ephemeral=True
            )
            return

        if role in interaction.user.roles:
            await interaction.response.send_message(
                "ℹ️ Ya tienes el rol de verificación.",
                ephemeral=True
            )
            return

        try:
            await interaction.user.add_roles(role, reason="Verificación por botón")
            await interaction.response.send_message(
                f"🎉 ¡Verificado! Se te ha asignado el rol **{role.name}**.",
                ephemeral=True
            )
            await send_verify_log(interaction, role, success=True)
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ No tengo permisos para asignarte ese rol.",
                ephemeral=True
            )
            await send_verify_log(interaction, role, success=False)


# ── Helper: enviar log de verificación ───────────────────────────────────────

async def send_verify_log(interaction: discord.Interaction, role: discord.Role, success: bool):
    config = config_manager.get_guild_config(interaction.guild_id)
    log_channel_id = config.get("verify_log_channel_id")
    if not log_channel_id:
        return

    channel = interaction.guild.get_channel(int(log_channel_id))
    if not channel:
        return

    color = discord.Color.green() if success else discord.Color.red()
    status = "✅ Verificado" if success else "❌ Falló la verificación"

    embed = discord.Embed(
        title="📋 Log de Verificación",
        color=color,
        timestamp=datetime.utcnow()
    )
    embed.set_author(
        name=str(interaction.user),
        icon_url=interaction.user.display_avatar.url
    )
    embed.add_field(name="👤 Usuario", value=interaction.user.mention, inline=True)
    embed.add_field(name="🆔 ID", value=str(interaction.user.id), inline=True)
    embed.add_field(name="🎭 Rol", value=role.mention, inline=True)
    embed.add_field(name="📌 Estado", value=status, inline=True)
    embed.set_footer(text=f"Servidor: {interaction.guild.name}")

    await channel.send(embed=embed)


# ── Cog principal ─────────────────────────────────────────────────────────────

class Verification(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.add_view(VerifyButton())

    @app_commands.command(
        name="send-verify",
        description="Envía el panel de verificación en el canal actual."
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def send_verify(
        self,
        interaction: discord.Interaction,
        titulo: str = "Verificación",
        descripcion: str = "Pulsa el botón para verificarte y acceder al servidor.",
        color_hex: str = "2ecc71"
    ):
        config = config_manager.get_guild_config(interaction.guild_id)
        role_id = config.get("verify_role_id")

        if not role_id:
            await interaction.response.send_message(
                "⚠️ Primero configura el rol con `/setup-role`.",
                ephemeral=True
            )
            return

        role = interaction.guild.get_role(int(role_id))
        role_mention = role.mention if role else "*(rol no encontrado)*"

        try:
            color = discord.Color(int(color_hex.lstrip("#"), 16))
        except ValueError:
            color = discord.Color.green()

        embed = discord.Embed(title=titulo, description=descripcion, color=color)
        embed.add_field(name="🎭 Rol que recibirás", value=role_mention)
        embed.set_footer(text=interaction.guild.name)

        await interaction.channel.send(embed=embed, view=VerifyButton())
        await interaction.response.send_message(
            "✅ Panel de verificación enviado.", ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Verification(bot))
