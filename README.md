# PluralKit Admin Extensions

This tool allows you to prevent users from using PluralKit without having a specific role.

You can either self-host, or use the public bot: https://discord.com/oauth2/authorize?client_id=1271138169299144795&scope=bot&permissions=536880128

## Config
`/config proxy-role-lock set {@role}`
`/config proxy-role-lock delete`
`/config proxy-role-lock set-alert-message-auto-delete {int}`
`/config proxy-role-lock set-alert-message {str}`

## Self hosting
1. Install python3.12+
2. Install requirements.txt
3. Rename `.env.sample` to `.env` and replace the values.
4. `python bot.py`
