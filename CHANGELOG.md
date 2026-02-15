# Buttergolem Changelog

Dieses Changelog fasst die wichtigsten Änderungen pro Version zusammen.

## 6.3.0beta1 (20. November 2025) - 100.000 User Special Update - Vision KI und Meme-Generierung

### Neue Funktionen
- Vision-KI: Analyse und Beschreibung hochgeladener Bilder
- Unterstützte Bildformate: JPEG, PNG, WEBP
- Meme-Generierung per API mit Template-Auswahl
- Automatische Erkennung von Meme-Anfragen im Chat
- Bilder werden nur nach ausdrücklicher Einwilligung (14 Tage) an externe KI-Dienste übertragen

### Verbesserungen und Bugfixes
- Verbesserte Keyword-Erkennung für Meme-Generierung (flexiblere Erkennung)
- Nicht unterstützte Formate (z. B. GIF) werden sauber abgefangen und führen nicht mehr zu Abstürzen

### Technische Änderungen
- OpenRouter Vision Model Integration (OPENROUTER_IMAGE_MODEL)
- Multimodale Prompts (Text und Bild)
- Erweiterte Fehlerbehandlung für nicht unterstützte Bildformate
- Admin: /admin neofetch und /admin serverinfo ergänzt
- Versionsanzeige vereinheitlicht

## 6.2.1rc1 (24. August 2025) - Hotfixes und neues KI-Modell

### Technische Änderungen
- Alle /drache Befehle sind nur noch im MEMBER_COUNTER_SERVER verfügbar

## 6.2.0 (16. August 2025) - Gaming Update - Hangman und Snake plus AI Memory System

### Neue Funktionen
- Neues Hangman-Spiel mit Rankings und Hilfe
- Snake-Spiel mit Highscore-System und Schwierigkeitsgraden
- KI-Memory-System: persistente Erinnerungen und kontextbewusste Antworten
- Neue Gaming-Kategorie in der Hilfe

### Verbesserungen und Bugfixes
- Stats-System Performance verbessert
- Stabilere Datenbank-Verbindungen für Spiele-Daten
- Optimierte Embed-Generierung und Fehlerbehandlung

## 6.1.0 (04. Juli 2025) - Admin Command Visibility und Changelog Fix

### Neue Funktionen
- Admin-Commands sind für normale Nutzer unsichtbar (native Discord-Permissions)
- Changelog-Ansicht für spezifische Versionen wiederhergestellt
- Drachigotchi als persistentes Spielsystem ergänzt

### Verbesserungen und Bugfixes
- Command-Registration und Permission-Handling stabilisiert

## 6.0.0 (2025) - Großes Update

### Highlights
- Komplette Migration auf Slash Commands
- Keine privilegierten Intents erforderlich
- Erweiterte KI-Funktionen und Sound-System
- Admin-Tools, Statistiken und Ban-Management

## 5.4.0 und früher

Für ältere Versionen siehe Git-History.
