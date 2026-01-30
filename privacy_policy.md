# Nutzungsbedingungen und Datenschutz

_Zuletzt aktualisiert: 30. Januar 2026_

---

## 1. Nutzungsbedingungen

### 1.1 Geltungsbereich

Diese Nutzungsbedingungen und die Datenschutzhinweise gelten für den Discord-Bot **drache_ai_dev** (Discord User ID: `1355540716205510767`, im Folgenden „Bot“) und alle damit verbundenen Funktionen.

### 1.2 Voraussetzungen

Sie dürfen den Bot nur auf Server einladen, für die Sie ausreichende Berechtigungen besitzen. Sie verpflichten sich außerdem, den Bot ausschließlich im Rahmen der geltenden Discord-Regeln (insbesondere [Discord Nutzungsbedingungen](https://discord.com/terms) und [Discord Community-Richtlinien](https://discord.com/guidelines)) sowie der jeweils anwendbaren Gesetze und Rechtsvorschriften zu verwenden (insbesondere im Land Ihres gewöhnlichen Aufenthalts bzw. des Server-Standorts, soweit einschlägig).

Der Bot darf nicht zur Erstellung, Verbreitung oder Förderung rechtswidriger Inhalte oder Handlungen genutzt werden.

### 1.3 Altersfreigabe

Der Bot richtet sich an Nutzer, die mindestens das Mindestalter gemäß den Discord-Nutzungsbedingungen erreicht haben.

#### 1.3.1 Keine NSFW-Inhalte

Der Bot ist so ausgelegt, dass keine NSFW-Inhalte erzeugt oder unterstützt werden. Die Nutzung des Bots ist ausschließlich für Inhalte vorgesehen, die für Personen unter 18 Jahren geeignet sind und den Discord-Regeln sowie dem jeweils anwendbaren Recht entsprechen.

Sie verpflichten sich ausdrücklich:

- keine NSFW-Inhalte anzufordern, zu übermitteln oder zu verbreiten
- keine sexualisierten Inhalte, keine pornografischen Inhalte und keine Inhalte mit sexueller Ausbeutung darzustellen oder anzufordern
- keine Inhalte zu übermitteln, die Minderjährige sexualisieren oder anderweitig gefährden
- keine Inhalte zu übermitteln, die gegen geltendes Recht, die Discord-Nutzungsbedingungen oder die Discord-Community-Richtlinien verstoßen

Der Bot kann Anfragen ablehnen, die gegen diese Regeln verstoßen oder die nach vertretbarer Einschätzung riskant sind.

### 1.4 Keine Verbindung zu Discord

Der Bot steht in keiner Verbindung zu Discord Inc. und wird nicht von dieser unterstützt oder bereitgestellt. Alle erwähnten Marken und Inhalte sind Eigentum ihrer jeweiligen Rechteinhaber.

### 1.5 KI-Funktionen und externe Anbieter (OpenRouter)

Für KI-Funktionen werden Inhalte an externe Dienste übermittelt. Der Bot nutzt dafür insbesondere **OpenRouter** (openrouter.ai) als Router, der Anfragen an den jeweils verwendeten Modellanbieter weiterleitet.

#### 1.5.1 Welche Inhalte können übermittelt werden

Je nach Funktion und Nutzung können an OpenRouter und den Modellanbieter übermittelt werden:

- Nachrichteninhalte (Text)
- Technische Kontextinformationen, sofern eine Funktion diese in den Prompt einbindet (z. B. Server-/Kanalnamen)
- Bei Bildauswertung: Bild-URLs (Discord-CDN) und/oder Bilddaten, sofern technisch erforderlich

Der Bot übermittelt nicht automatisch Ihre Discord-User-ID an OpenRouter. Wenn Sie jedoch selbst personenbezogene Daten in eine Nachricht schreiben oder in einem Bild enthalten sind, können diese Inhalte Bestandteil der Anfrage sein.

#### 1.5.2 Welche Modelle verwendet werden

Der Bot wählt das Modell abhängig von der Anfrageart. Die Modellbezeichner sind konfigurierbar und können sich ändern.

- Text: über die Konfiguration `OPENROUTER_MODEL`
- Bilder (Vision): über die Konfiguration `OPENROUTER_IMAGE_MODEL`
- Video: eine Konfiguration `OPENROUTER_VIDEO_MODEL` kann vorhanden sein; aktuell ist die Video-Auswertung im Bot nicht aktiv

#### 1.5.3 Hinweise zur Datenverarbeitung bei OpenRouter

OpenRouter beschreibt in der eigenen Dokumentation unter anderem:

- OpenRouter speichert Prompts und Antworten grundsätzlich nicht, außer wenn im OpenRouter-Account ausdrücklich Prompt-Logging aktiviert wurde
- OpenRouter speichert Metadaten (z. B. Tokenanzahl, Latenz) zu Anfragen
- Modellanbieter können eigene Logging- und Aufbewahrungsrichtlinien haben; diese sind modell- und providerabhängig
- Es gibt bei OpenRouter eine Zero-Data-Retention (ZDR) Option, mit der Anfragen nur zu Endpoints geroutet werden, die keine Daten speichern

Maßgeblich sind immer die jeweils aktuellen Richtlinien und Bedingungen von OpenRouter und des verwendeten Modellanbieters.

Quellen und weiterführende Links: siehe Abschnitt 3.

### 1.6 Einwilligung für Bild-Uploads

Wenn Sie dem Bot Bilder senden und eine KI-Auswertung wünschen, werden Bilder nur nach ausdrücklicher Einwilligung an den externen KI-Dienst übertragen. Diese Einwilligung betrifft ausschließlich die Übermittlung von Bildinhalten an externe KI-Dienste zur Analyse.

- Die Einwilligung wird für 14 Tage gespeichert oder bis diese ToS geändert werden
- Nach Ablauf oder ToS-Änderung wird erneut eine Einwilligung abgefragt
- Ein Widerruf ist jederzeit möglich; dann werden keine Bilder mehr hochgeladen

Mit dem Erteilen der Einwilligung bestätigen Sie zusätzlich, dass die von Ihnen übermittelten Bilder rechtlich zulässig sind und nicht gegen die Regeln aus Abschnitt 1.3.1 verstoßen. Insbesondere dürfen keine NSFW-Inhalte übermittelt werden.

### 1.7 Haftungsausschluss

Der Bot wird „wie gesehen“ bereitgestellt. Ausgaben externer KI-Anbieter können fehlerhaft, unvollständig oder irreführend sein. Der Betreiber haftet nicht für Inhalte, Ausgaben oder Entscheidungen externer KI-Anbieter.

Nutzen Sie KI-Antworten nicht als alleinige Grundlage für rechtliche, medizinische, finanzielle oder sicherheitsrelevante Entscheidungen.

### 1.8 Änderungen

Diese Bedingungen können aktualisiert werden. Wenn Sie mit Änderungen nicht einverstanden sind, entfernen Sie den Bot bitte vom Server und nutzen Sie seine Funktionen nicht weiter.

---

## 2. Datenschutz

### 2.1 Zweck der Verarbeitung

Der Bot verarbeitet Daten ausschließlich, um Bot-Funktionen bereitzustellen (Befehle, Spiele, KI-Funktionen, Moderationsfunktionen, Logging und technische Fehleranalyse).

### 2.2 Welche Daten verarbeitet werden

Je nach Nutzung können folgende Daten verarbeitet werden:

#### 2.2.1 Discord-Daten

- User-IDs (für Befehle, Sessions, Moderation und Admin-Funktionen)
- Server-/Kanal-IDs und Namen (für Befehlsausführung, Statistiken und Logging)
- Nachrichteninhalte (für die unmittelbare Verarbeitung; bei KI-Funktionen zusätzlich zur Generierung einer Antwort)
- Anhänge (bei Bildauswertung: siehe Einwilligung)

#### 2.2.2 Session- und Funktionsdaten

- Session-basierter Gesprächsverlauf für KI-Funktionen (maximal 15 Nachrichten pro Benutzer-Session)
- Fehler- und Ereignislogs zur Stabilität und Missbrauchsprävention
- Optional: Protokollierung von KI-Anfragen/Antworten in einem serverinternen Logging-Kanal (wenn konfiguriert)

#### 2.2.3 Einwilligungsdaten für Bild-Uploads

Für Bild-Uploads an externe KI-Dienste wird eine Einwilligung gespeichert:

- User-ID
- Zeitpunkt der Einwilligung
- ToS-Version (Änderungserkennung)
- Letzte Anfrage-Metadaten (Server-ID, Channel-ID, Message-ID, Quelle)
- Audit-Log (Ereignisprotokoll, begrenzt auf eine feste Anzahl aktueller Einträge)

IP-Adressen von Nutzern werden nicht erhoben. Discord stellt dem Bot keine IP-Adresse von Nutzern bereit.

### 2.3 Empfänger der Daten

- Discord (notwendiger Plattformbetrieb)
- Bei KI-Funktionen: OpenRouter und der jeweils verwendete Modellanbieter

### 2.4 Speicherdauer

- Session-Kontexte werden begrenzt gespeichert (max. 15 Nachrichten pro Benutzer-Session)
- Einwilligungen für Bild-Uploads werden bis zum Ablauf (14 Tage), Widerruf oder ToS-Änderung berücksichtigt; Einträge können technisch darüber hinaus in Backups oder Log-Rotation enthalten sein
- Audit-Logs werden in der Größe begrenzt (nur die neuesten Einträge)

### 2.5 Widerruf und Löschung

Sie können eine erteilte Einwilligung jederzeit widerrufen. Danach werden keine Bilder mehr an externe KI-Dienste übertragen.

Wenn Sie eine Löschung Ihrer gespeicherten Einwilligungsdaten wünschen, kontaktieren Sie bitte das Server-Team oder die Betreiber des Bots über die üblichen Support-Kanäle des Servers, auf dem der Bot genutzt wird.

### 2.6 Ihre Rechte

Je nach anwendbarer Rechtslage (insbesondere DSGVO) können Ihnen Rechte auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung und Widerspruch zustehen. Da der Bot typischerweise in einem Server-Kontext betrieben wird, erfolgt die Kommunikation dazu über die üblichen Support-Kanäle des Servers, auf dem der Bot genutzt wird.

---

## 3. Quellen und weiterführende Links

- Discord Nutzungsbedingungen: https://discord.com/terms
- Discord Community-Richtlinien: https://discord.com/guidelines
- OpenRouter Datenschutz (Datenerhebung): https://openrouter.ai/docs/guides/privacy/data-collection
- OpenRouter Logging: https://openrouter.ai/docs/guides/privacy/logging
- OpenRouter Zero Data Retention (ZDR): https://openrouter.ai/docs/guides/features/zdr

---

## 4. Zustimmung und Geltung

Bitte lesen Sie diese Nutzungsbedingungen und Datenschutzhinweise vollständig, bevor Sie den Bot einladen oder seine Funktionen nutzen.

Wenn Sie mit diesen Bedingungen nicht einverstanden sind, entfernen Sie den Bot bitte vom Server und nutzen Sie seine Funktionen nicht weiter.

Mit dem Einladen des Bots auf einen Discord-Server oder der Nutzung seiner Funktionen erklären Sie, dass Sie diese Bedingungen gelesen und verstanden haben und mit ihrer Geltung einverstanden sind.
