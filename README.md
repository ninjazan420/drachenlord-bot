# Buttergolem - Discord Bot

Buttergolem ist ein Discord-Bot mit Spielen, Sounds und KI-Chat-Funktionen.

## Was ist neu in v6.3.0beta1 (15.02.2026)

### Vision-KI und Meme-Generierung
- Vision-KI: die KI kann hochgeladene Bilder analysieren und beschreiben
- Unterstützte Bildformate: JPEG, PNG, WEBP
- Bilder werden nur nach ausdrücklicher Einwilligung (14 Tage gültig) an externe KI-Dienste übertragen
- Meme-Generierung per API mit Template-Auswahl
- Robustere Behandlung nicht unterstützter Formate (z. B. GIF)

## Features

### Slash Commands
Alle Commands sind als moderne Slash Commands verfügbar - keine Prefixe mehr nötig!

#### Nutzer Commands
- `/sound [name]` - Spezifischen Sound abspielen
- `/sounds` - Alle verfügbaren Sounds anzeigen
- `/lord` - Zufälligen Drachenlord Sound
- `/zitat` - Zufälliges Drachenlord Zitat
- `/mett` - Mett-Meme
- `/lordmeme [text] [position]` - Drachenlord Meme erstellen
- `/quiz [runden]` - Drachenlord Quiz starten (1-20 Runden)
- `/ping` - Bot-Latenz prüfen
- `/hangman` - Starte ein Hangman-Spiel
- `/hangman_rankings` - Hangman-Bestenliste anzeigen
- `/hangman_hilfe` - Hangman-Spielregeln und Hilfe
- `/gotchi hilfe` - Drachigotchi Spiel-Anleitung
- `/hilfe` - Komplette Hilfe mit allen Commands
- `/kontakt` - Kontakt-Informationen
- `/privacy` - Datenschutzerklärung

#### Admin Commands
- `/admin neofetch [stil] [farbe]` - Systeminfos im Terminal-Stil
- `/admin memory [action] [user_id] [data]` - Memory-System verwalten (list/show/add/delete)
- `/admin servercount` - Servercounter-Update ausführen
- `/admin server [page]` - Server-Liste (mit Sortierung/Seiten)
- `/admin serverinfo <id>` - Server-Details zu Seq-ID oder Discord-ID
- `/admin leave <id> [grund]` - Server verlassen
- `/admin ban <typ> <id> [grund]` - Server oder User bannen
- `/admin unban <typ> <ban_id>` - Ban aufheben
- `/admin bans [typ]` - Aktive Bans anzeigen
- `/admin consent <action> [query] [page]` - Zustimmungen für Bild-Uploads verwalten
- `/admin antwort <message_id> <text>` - Admin-Antwort senden
- `/admin message <id> <server|user> <text>` - Nachricht an Server/User senden
- `/admin global <text>` - Globale Nachricht an alle Update-Kanäle senden
- `/admin debug_sounds` - Sound-System debuggen
- `/admin butteriq [action] [user]` - ButterIQ Management (enable/disable/status)

Hinweise:
- Admin-Commands werden nur auf dem Support-Server registriert (siehe `MEMBER_COUNTER_SERVER`)
- Die Hilfe für Admins ist in `/hilfe` integriert und wird nur dem Bot-Admin angezeigt

### KI-Chat Features
- Erweiterte Drachenlord Lore: aktuelle Informationen bis 2024/2025
- Kontextbewusste Antworten: versteht den Gesprächskontext
- Authentische Persönlichkeit: echter Drachenlord-Style
- Memory-System: merkt sich wichtige Informationen

### Sound System
- 500+ Soundclips: organisiert und optimiert
- Intelligentes Caching: schnelle Ladezeiten
- Auto-Complete: einfaches Finden von Sounds
- Hohe Qualität: optimierte Audio-Dateien

### Statistiken
- Neofetch-Style: System-Informationen im Terminal-Stil
- Echtzeit-Updates: Live-Statistiken
- Server-Übersicht: alle verbundenen Server
- Performance-Metriken: Bot-Health Monitoring

## Installation

### Docker (empfohlen)
```bash
git clone <repo-url>
cd buttergolem-bot
cp docker-compose.example.yml docker-compose.yml
# docker-compose.yml mit deinen Werten anpassen
docker-compose up -d
```

### Manuelle Installation
```bash
git clone <repo-url>
cd buttergolem-bot
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows

pip install -r requirements.txt
cp .env.example .env
# .env mit deinen Werten anpassen

python src/main.py
```

## Migration von v5.x

### Für Server-Admins
1. Bot mit aktualisierten Permissions neu einladen
2. Alte `!` Commands durch `/` Commands ersetzen
3. Admin-Commands testen und konfigurieren

### Für Nutzer
1. Neue Slash Commands verwenden
2. Auto-Complete für einfachere Bedienung nutzen
3. Ephemeral Responses für private Antworten

## Systemanforderungen

- **Python**: 3.9 oder höher
- **Discord.py**: 2.3 oder höher
- **Intents**: Keine privilegierten Intents nötig
- **Speicher**: Mindestens 2GB RAM
- **Speicherplatz**: 500MB für Sounds und Daten

## Konfiguration

### Docker Compose
```yaml
services:
  buttergolem:
    build: .
    volumes:
      - ./data:/app/data # Persistenter Speicher für Spieldaten

    environment:
      DISCORD_API_TOKEN: "Discord Token API" # Discord Bot-Token
      ENABLE_RANDOM_JOINS: "False" # Zufällige VC-Joins aktivieren
      BLACKLISTED_GUILDS: "123456,654321" # Komma-separierte Liste

      ADMIN_USER_ID: "123123123" # Achtung: darf Admin-Commands nutzen

      # Mongodb

      MONGODB_CONNECTION_STRING: "mongodb+srv://your:string@databasename.randomstring.mongodb.net/?retryWrites=true&w=majority&appName=YOURAPPNAME"
      MONGODB_DATABASE_NAME: "Your app Name"
      MONGODB_TIMEOUT: "5000"
      MONGODB_POOL_SIZE: "50"
      ENABLE_MONGODB: "false"  # Feature-Flag: wenn deaktiviert, wird alles in JSON gespeichert

      # API Keys

      OPENROUTER_KEY: "Open Router Key"
      VOID_API_KEY: "Void.ai Key"
      OPENROUTER_MODEL: "arcee-ai/trinity-large-preview:free"
      OPENROUTER_IMAGE_MODEL: "nvidia/nemotron-nano-12b-v2-vl:free"
      PUBLIC_TOS_URL: "https://deine-domain.tld/privacy_policy"

      # Channel-spezifisch

      LOGGING_CHANNEL: "Your Logging Channel ID" # Logging Channel ID
      CHAT_MIRROR_CHANNEL: "Chat Mirror Channel"
      MEMBER_COUNTER_SERVER: "Membercounter Voice Channel Server"

      # Sonstiges

      DISCORDS_KEY: "discords.com server counter api key" # optional
      TOPGG_KEY: "top.gg key" # optional

      # Monero Wallet für Spenden
      
      MONERO_SPENDEN_ID: "Your Monero Wallet"

```

## Verwendung

### Erste Schritte
1. Bot zu deinem Server einladen
2. `/hilfe` für die vollständige Command-Liste
3. `/lord` für einen zufälligen Sound
4. `/drache stats` für Bot-Statistiken

### Sound-System
- `/sounds` zeigt alle verfügbaren Sounds
- `/sound [name]` spielt einen spezifischen Sound
- Auto-Complete hilft beim Finden

### Admin-Funktionen
- Nur für Bot-Admins verfügbar
- Detaillierte Hilfe mit `/hilfe`
- Sichere Permission-Systeme

## Bild-Einwilligung (Consent)

Für Bild-Uploads an externe KI-Dienste gilt:
- Einwilligung wird pro User gespeichert und ist 14 Tage gültig
- Bei geänderten ToS muss erneut zugestimmt werden
- Die Einwilligung kann jederzeit widerrufen/gelöscht werden (Admin)
- Speicherort: `data/user_consents.json`
- ToS-Quelle: `privacy_policy.md` (Link optional per `PUBLIC_TOS_URL`)

## Support

- Issues und Feature-Requests bitte über die jeweilige Projekt-Plattform einreichen.

## Beitragen

1. Fork das Repository
2. Erstelle einen Feature Branch
3. Commit deine Änderungen
4. Push zum Branch
5. Erstelle einen Pull Request

## Lizenz

Dieses Projekt ist unter der GNU General Public License v3 lizenziert. Siehe [LICENSE](LICENSE) für Details.

## Danksagung

- **Drachenlord** - Für die Inspiration
- **Discord.py Community** - Für die großartige Library
- **Alle Unterstützer** - Für die großzügigen Spenden
- **Community** - Für Feedback und Feature-Ideen

---

Erstellt vom Buttergolem Team
