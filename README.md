# 🤖 Maldito Verification Bot

Bot de verificación multi-servidor, 100% configurable desde Discord.

> Developed by Maldito Cupido

## 🚀 Instalación

```bash
git clone https://github.com/ownixoficial/Maldito-Verification
cd Maldito-Verification
python -m pip install -r requirements.txt
```

Crea un archivo `.env`:
```env
DISCORD_TOKEN=tu_token_aquí
```

Ejecuta el bot:
```bash
python bot.py
```

## ⚙️ Comandos (solo Administradores)

| Comando | Descripción |
|---|---|
| `/setup-role <rol>` | Define el rol que se da al verificarse |
| `/setup-log <canal>` | Define el canal de logs de verificación |
| `/setup-info` | Muestra la configuración actual del servidor |
| `/setup-reset` | Resetea toda la configuración |
| `/send-verify` | Envía el panel con el botón de verificación |

## 📋 Flujo de uso

1. Invita el bot con permisos: `Manage Roles`, `Send Messages`, `View Channels`
2. Usa `/setup-role` para elegir qué rol dar al verificarse
3. Usa `/setup-log` para elegir dónde se registran los logs (opcional)
4. Usa `/send-verify` en el canal de bienvenida para publicar el panel
5. Los usuarios pulsarán **✅ Verificarme** y recibirán el rol automáticamente

## 🔑 Permisos necesarios del bot

- `application.commands`
- `bot` con: Manage Roles, Send Messages, Read Message History, View Channels, Members Intent

## 📝 Notas

- La configuración se guarda por servidor en `guild_configs.json`
- El botón es **persistente** (funciona aunque reinicies el bot)
- Funciona en múltiples servidores a la vez
