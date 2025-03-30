<p align="center"><img src="https://github.com/Blackstonecoden/Fuchs-Bot/blob/main/images/bot_logo.png?raw=true" alt="Fuchs Bot Logo" width="200"></p>
<h1 align="center">Fuchs Bot - Python<br>
	<a href="https://github.com/Blackstonecoden/Fuchs-Bot"><img src="https://img.shields.io/github/stars/Blackstonecoden/Fuchs-Bot"></a>
	<a href="https://discord.gg/9QA8DVRKqw"><img src="https://img.shields.io/discord/1192851131760656435?color=5865f2&label=Discord&style=flat" alt="Discord"></a>
	<br><br>
</h1>

---

# Was ist der Fuchs Bot?

Der Fuchs Bot ist die Custom-Made APP für den Fuchs Höhle Discord Server. Die Features von der APP sind: WelcomeSystem, Counting System, Temp-Channel System, Ticket System und Level System.

--- 

# 1. Setup
## 1.1 Anforderungen
Wenn du einen eigene APP haben möchtest, erstelle zuerst eine auf [discord.com/developers](https://discord.com/developers/applications) und gib der APP alle intents. Klone den Code und packe ihn auf deinen Server. Sonstige Anforderungen:
- Server mit Python instaliert (um die APP zu hosten)
- MySQL / MariaDB Database

## 1.2 Config Setup
### 1.2.1 Umgebungsvariablen
Erstelle eine Date namens `.env` auf deinem Server und fülle sie mit deinen APP und Database Anmeldeinformationen.
```py
TOKEN = MTI...

database_host = 1.2.3.4:3306
database_user = nutzername
database_password = passwort
database_name = discord_app
```
### 1.2.2 Config Datei
Erstelle nun eine Datei namens `config.json` und fülle sie mit deinen Konfigurationen
```json
{ 
    "custom_app_status": "🦊 Fuchs",

    "guild_id": 1234,
    "join_role": 1234,
    "suggestion_role": 1234,

    "channels": {
        "welcome": 1234,
        "temp_join": 1234,
        "counting": 1234
    },

    "categories": {
        "tickets": 1234,
        "temp_channels": 1234
    },    

    "ticket_types": {
        "general": {
            "disabled": false,
            "roles": [1234,1234],
            "name": "Allgemeiner Support",
            "description": "Allgemeiner Support / Fragen",
            "short_name": "Allgemein",
            "emoji": "📨",
            "discord_emoji": "mail"
        },
        "application": {
            "disabled": false,
            "roles": [1234,1234],
            "name": "Team Bewerbung",
            "description": "Bewirb dich als Teammitglied",
            "short_name": "Bewerbung",
            "emoji": "📄",
            "discord_emoji": "file_text"
        }
    },

    "daily_rewards": {
        "0": 100,
        "1": 200,
        "2": 300,
        "3": 400,
        "4": 500,
        "5": 600,
        "6": 700,
        "7": 1000
    },

    "emojis": {
        "edit":         "<:emoji:1234>",
        "eye":          "",
        "eye_off":      "",
        "lock":         "",
        "trash":        "",
        "unlock":       "",
        "user_minus":   "",
        "user_plus":    "",
        "users":        "",
        "user_check":   "",
        "file_text":    "",
        "block":        "",
        "mail":         "",
        "repeat":       "",
        "zap":          "",
        "refresh":      "",
        "dollar":       "",
        "plus":         "",
        "minus":        "",
        "rotate":       "",
        "key":          "",
    
        "trash_red":    ""
    },

    "images": {
        "grey_ticket_line":     "https:/example.com/line_icons/ticket_grey.png",
        "red_ticket_line":      "https:/example.com/line_icons/ticket_red.png",
        "green_ticket_line":    "https:/example.com/line_icons/ticket_green.png",
    
        "user_plus_grey":       "https:/example.com/line_icons/user_plus_grey.png",
        "user_minus_grey":      "https:/example.com/line_icons/user_minus_grey.png",
    
        "red_trash_line":       "https:/example.com/line_icons/trash_red.png"
    }
}
```

## 1.3 APP starten
Nun sollte alles startklar sein und du kannst die main.py starten und die APP soltle fehlerfrei laufen. Falls du Hilfe benötigst, tritt gerne unserem [Discord Server](https://discord.gg/9QA8DVRKqw) bei.