import discord
from discord.ext import commands
from datetime import datetime
import locale

# Setze deutsche Locale für Datumsformatierung
try:
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'German_Germany.1252')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'de_DE')
        except locale.Error:
            # Fallback auf Standard-Locale - robuste Datumsverarbeitung übernimmt
            print("Warning: Konnte deutsche Locale nicht setzen, verwende robuste Datumsverarbeitung")

class ChangelogCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Monatsnamen-Mapping für robuste Datumsverarbeitung
        self.month_mapping = {
            # Englische Monatsnamen
            'January': 'Januar', 'February': 'Februar', 'March': 'März',
            'April': 'April', 'May': 'Mai', 'June': 'Juni',
            'July': 'Juli', 'August': 'August', 'September': 'September',
            'October': 'Oktober', 'November': 'November', 'December': 'Dezember',
            # Deutsche Monatsnamen (für Konsistenz)
            'Januar': 'Januar', 'Februar': 'Februar', 'März': 'März',
            'Mai': 'Mai', 'Juni': 'Juni', 'Juli': 'Juli',
            'Oktober': 'Oktober', 'Dezember': 'Dezember'
        }

        # Changelog data - format: version: {date, features, fixes, notes}
        self.changelog_data = {
            "6.3.0beta1": {
                "date": "20 November 2025",
                "title": "🖼️ 100.000 User Special Update (thx@all) - Vision AI & Meme Generation Update",
                "features": [
                    "Vision AI Integration - KI kann jetzt hochgeladene Bilder analysieren und beschreiben",
                    "Unterstützte Bildformate: JPEG, PNG, WEBP",
                    "Intelligente Meme-Generierung mit imgflip API",
                    "Kontext-basierte Template-Auswahl für passende Memes",
                    "Automatische Erkennung von Meme-Requests im Chat",
                    "Graceful Handling von nicht unterstützten Formaten (z.B. GIFs)"
                ],
                "fixes": [
                    "Verbesserte Keyword-Erkennung für Meme-Generierung",
                    "Flexible Detection: 'meme' + 'erstellen' wird jetzt erkannt",
                    "GIF-Uploads crashen nicht mehr - freundliche Fehlermeldung stattdessen",
                    "Gespräche werden fortgesetzt auch wenn Bildformat nicht unterstützt wird"
                ],
                "technical": [
                    "OpenRouter Vision Model Integration (OPENROUTER_IMAGE_MODEL)",
                    "Multimodal Content Arrays für Text + Bild Kombination",
                    "Imgflip API Integration mit Template-Auswahl",
                    "Automatische Model-Auswahl basierend auf Attachment-Typ",
                    "Erweiterte Error-Handling für unsupported Image-Formate",
                    "Max Tokens auf 550 reduziert für schnellere Antworten",
                    "Admin System: /admin neofetch und /admin serverinfo ergänzt",
                    "Serverübersicht: gebannte Server werden in der Liste markiert",
                    "Versionsanzeige vereinheitlicht"
                ]
            },


            "6.2.1rc1": {
                "date": "24 August 2025",
                "title": "Hotfixes & Neues KI Modell",
                "technical": [
                    "ALLE `/drache` Befehle sind jetzt nur noch im MEMBER_COUNTER_SERVER verfügbar",
                    "Verhindert dass normale User Bot-Informationen auf anderen Servern einsehen können",
                    "Verbesserte Sicherheit und Kontrolle über Bot-Funktionen"
                ]
            },
            "6.2.0": {
                "date": "16 August 2025",
                "title": "� Gaming Update - Hangman & Snake + AI Memory System",
                "features": [
                    "Neues Hangman-Spiel mit rankings /hangman und /hangman_ranking",
                    "Snake-Spiel mit Highscore-System und verschiedenen Schwierigkeitsgraden",
                    "AI Memory System - KI kann sich jetzt an vorherige Gespräche erinnern",
                    "Verbesserte Stats-Anzeige mit optimierter Performance",
                    "Neue Gaming-Kategorie in der Hilfe mit allen verfügbaren Spielen",
                    "Persistente Speicherung von Spielständen und Highscores"
                ],
                "fixes": [
                    "Stats-System Performance deutlich verbessert",
                    "Memory-Leaks in der Statistik-Anzeige behoben",
                    "Stabilere Datenbank-Verbindungen für Spiele-Daten",
                    "Optimierte Embed-Generierung für bessere Ladezeiten",
                    "Verbesserte Error-Behandlung in allen Gaming-Modulen"
                ],
                "technical": [
                    "Implementierung des Hangman-Systems mit Kategorie-Management",
                    "Snake-Game Engine mit Collision-Detection und Score-Tracking",
                    "AI Memory Backend mit JSON-basierter Persistierung",
                    "Refactoring der Stats-Module für bessere Performance",
                    "Modulare Gaming-Architektur für zukünftige Spiele-Erweiterungen",
                    "Abhängigkeiten geupdated"
                ]
            },

        }

    def parse_date_robust(self, date_string):
        """Robuste Datumsverarbeitung für deutsche und englische Monatsnamen"""
        # Liste von Formaten zum Ausprobieren
        formats = [
            "%d %B %Y",      # z.B. "20 November 2025" (englisch)
            "%d. %B %Y",     # z.B. "20. November 2025" (deutsch mit Punkt)
            "%Y-%m-%d",      # ISO Format
            "%d %b %Y",      # Kurze Monatsnamen
        ]

        # Versuche alle Formate mit original locale
        for fmt in formats:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue

        # Falls das fehlschlägt, konvertiere englische zu deutschen Monatsnamen
        for eng_month, ger_month in self.month_mapping.items():
            if eng_month in date_string:
                german_date = date_string.replace(eng_month, ger_month)
                for fmt in formats:
                    try:
                        return datetime.strptime(german_date, fmt)
                    except ValueError:
                        continue

        # Letzter Fallback: aktuelles Datum
        print(f"Warning: Konnte Datum '{date_string}' nicht parsen, verwende aktuelles Datum")
        return datetime.now()

    @commands.command(name='changelog')
    async def changelog_command(self, ctx, version=None):
        """Display changelog for specific version or latest versions"""

        if version:
            # Entferne "v" prefix falls vorhanden
            if version.startswith('v'):
                version = version[1:]

            # Show specific version
            if version in self.changelog_data:
                await self.send_version_changelog(ctx, version)
            else:
                embed = discord.Embed(
                    title="❌ Version Not Found",
                    description=f"Version `{version}` not found in changelog.\n\nAvailable versions: {', '.join(self.changelog_data.keys())}",
                    color=0xff0000
                )
                await ctx.send(embed=embed)
        else:
            # Show overview of all versions
            await self.send_changelog_overview(ctx)

    async def send_version_changelog(self, ctx, version):
        """Send detailed changelog for a specific version"""
        # Entferne "v" prefix falls vorhanden
        if version.startswith('v'):
            version = version[1:]

        data = self.changelog_data[version]

        embed = discord.Embed(
            title=f"📋 Changelog - Version {version}",
            description=data["title"],
            color=0x00ff00,
            timestamp=self.parse_date_robust(data["date"])
        )

        # Features
        if data.get("features"):
            features_text = "\n".join([f"• {feature}" for feature in data["features"]])
            embed.add_field(
                name="✨ New Features",
                value=features_text[:1024],  # Discord field limit
                inline=False
            )

        # Fixes
        if data.get("fixes"):
            fixes_text = "\n".join([f"• {fix}" for fix in data["fixes"]])
            embed.add_field(
                name="🔧 Improvements & Fixes",
                value=fixes_text[:1024],
                inline=False
            )

        # Technical
        if data.get("technical"):
            technical_text = "\n".join([f"• {tech}" for tech in data["technical"]])
            embed.add_field(
                name="⚙️ Technical Changes",
                value=technical_text[:1024],
                inline=False
            )

        embed.set_footer(text=f"Buttergolem Bot v{version} | Released on {data['date']}")

        # Check if ctx is an Interaction or Context object
        if hasattr(ctx, 'response'):
            # It's an Interaction object
            await ctx.response.send_message(embed=embed, ephemeral=True)
        else:
            # It's a Context object
            await ctx.send(embed=embed)

    async def send_changelog_overview(self, ctx):
        """Send overview of all versions"""
        embed = discord.Embed(
            title="📋 Buttergolem Bot Changelog",
            description="Here's the complete version history of the Buttergolem Discord Bot.\n\nUse `/changelog <version>` for detailed information.",
            color=0xf1c40f
        )

        # Sort versions by date (newest first)
        sorted_versions = sorted(
            self.changelog_data.items(),
            key=lambda x: self.parse_date_robust(x[1]["date"]),
            reverse=True
        )

        for version, data in sorted_versions:
            feature_count = len(data.get("features", []))
            fix_count = len(data.get("fixes", []))

            embed.add_field(
                name=f"🏷️ Version {version}",
                value=f"**{data['title']}**\n"
                      f"📅 Released: {data['date']}\n"
                      f"✨ {feature_count} new features\n"
                      f"🔧 {fix_count} improvements\n"
                      f"`/changelog {version}` for details",
                inline=True
            )

        embed.add_field(
            name="🔗 Links",
            value="[GitHub Repository](https://github.com/ninjazan420/buttergolem-bot)\n"
                  "[Report Issues](https://github.com/ninjazan420/buttergolem-bot/issues)",
            inline=False
        )

        embed.set_footer(text="Buttergolem | Made with ❤️ by ninjazan420")

        # Check if ctx is an Interaction or Context object
        if hasattr(ctx, 'response'):
            # It's an Interaction object
            await ctx.response.send_message(embed=embed, ephemeral=True)
        else:
            # It's a Context object
            await ctx.send(embed=embed)

    def add_version(self, version, date, title, features=None, fixes=None, technical=None):
        """Add a new version to changelog (for future updates)"""
        self.changelog_data[version] = {
            "date": date,
            "title": title,
            "features": features or [],
            "fixes": fixes or [],
            "technical": technical or []
        }

def setup(bot):
    bot.add_cog(ChangelogCog(bot))
