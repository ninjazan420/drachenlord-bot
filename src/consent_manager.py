import asyncio
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import discord


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _to_iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


def _parse_iso(value: str) -> Optional[datetime]:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value)
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def _safe_read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def _sha256_short(text: str, length: int = 12) -> str:
    if text is None:
        text = ""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def _guess_media_kind(attachment: discord.Attachment) -> Optional[str]:
    content_type = (attachment.content_type or "").lower().strip()
    filename = (attachment.filename or "").lower().strip()

    if content_type.startswith("image/"):
        return "bild"
    if content_type.startswith("video/"):
        return "video"

    if filename.endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
        return "bild"
    if filename.endswith((".mp4", ".mpeg", ".mov", ".webm")):
        return "video"

    return None


@dataclass(frozen=True)
class ConsentCheckResult:
    ok: bool
    reason: Optional[str] = None
    record: Optional[dict[str, Any]] = None
    tos_version: Optional[str] = None


class ConsentManager:
    def __init__(
        self,
        consent_file: Optional[str] = None,
        tos_file: Optional[str] = None,
        renew_days: int = 14,
        tos_url: Optional[str] = None,
    ):
        self.consent_file = consent_file or os.path.join("data", "user_consents.json")
        self.tos_file = tos_file or "privacy_policy.md"
        self.renew_days = int(renew_days)
        self.tos_url = tos_url or os.getenv("PUBLIC_TOS_URL", "").strip() or None
        self._lock = asyncio.Lock()

    def get_tos_version(self) -> str:
        text = _safe_read_text(self.tos_file)
        last_updated = ""
        for line in text.splitlines()[:40]:
            if "Last updated:" in line:
                last_updated = line.split("Last updated:", 1)[-1].strip().strip("_").strip()
                break
            if "Zuletzt aktualisiert:" in line:
                last_updated = line.split("Zuletzt aktualisiert:", 1)[-1].strip().strip("_").strip()
                break
        digest = _sha256_short(text)
        if last_updated:
            return f"{last_updated}|sha256:{digest}"
        return f"sha256:{digest}"

    def _load(self) -> dict[str, Any]:
        if not os.path.exists(self.consent_file):
            return {"schema_version": 2, "users": {}, "audit_log": []}
        try:
            with open(self.consent_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                return {"schema_version": 2, "users": {}, "audit_log": []}
            if "users" not in data or not isinstance(data.get("users"), dict):
                data["users"] = {}
            if "audit_log" not in data or not isinstance(data.get("audit_log"), list):
                data["audit_log"] = []
            if "schema_version" not in data or not isinstance(data.get("schema_version"), int):
                data["schema_version"] = 2
            return data
        except Exception:
            return {"schema_version": 2, "users": {}, "audit_log": []}

    def _save(self, data: dict[str, Any]) -> None:
        dir_path = os.path.dirname(self.consent_file)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        tmp_path = f"{self.consent_file}.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, self.consent_file)

    def _normalize_audit_log(self, audit_log: list[dict[str, Any]], keep_last: int = 500) -> list[dict[str, Any]]:
        if not audit_log:
            return []
        if keep_last <= 0:
            return []
        if len(audit_log) <= keep_last:
            return audit_log
        return audit_log[-keep_last:]

    async def log_event(
        self,
        action: str,
        actor_user_id: Optional[int] = None,
        target_user_id: Optional[int] = None,
        guild_id: Optional[int] = None,
        channel_id: Optional[int] = None,
        message_id: Optional[int] = None,
        extra: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        entry: dict[str, Any] = {
            "timestamp": _to_iso(_utc_now()),
            "action": str(action or "").strip() or "unbekannt",
            "actor_user_id": str(actor_user_id) if actor_user_id is not None else None,
            "target_user_id": str(target_user_id) if target_user_id is not None else None,
            "guild_id": str(guild_id) if guild_id is not None else None,
            "channel_id": str(channel_id) if channel_id is not None else None,
            "message_id": str(message_id) if message_id is not None else None,
            "extra": extra or {},
        }
        async with self._lock:
            data = self._load()
            audit_log = data.setdefault("audit_log", [])
            if not isinstance(audit_log, list):
                audit_log = []
            audit_log.append(entry)
            data["audit_log"] = self._normalize_audit_log(audit_log)
            data["schema_version"] = int(data.get("schema_version") or 2)
            self._save(data)
        return entry

    async def checkConsent(self, user_id: int) -> ConsentCheckResult:
        tos_version = self.get_tos_version()
        async with self._lock:
            data = self._load()
            users = data.get("users", {})
            record = users.get(str(user_id))
            if not isinstance(record, dict):
                return ConsentCheckResult(ok=False, reason="keine_einwilligung", tos_version=tos_version)

            if record.get("revoked") is True:
                return ConsentCheckResult(ok=False, reason="widerrufen", record=record, tos_version=tos_version)

            if record.get("tos_version") != tos_version:
                return ConsentCheckResult(ok=False, reason="tos_geaendert", record=record, tos_version=tos_version)

            ts = _parse_iso(record.get("consented_at", ""))
            if ts is None:
                return ConsentCheckResult(ok=False, reason="zeitstempel_unlesbar", record=record, tos_version=tos_version)

            if _utc_now() - ts > timedelta(days=self.renew_days):
                return ConsentCheckResult(ok=False, reason="abgelaufen", record=record, tos_version=tos_version)

            return ConsentCheckResult(ok=True, record=record, tos_version=tos_version)

    async def storeConsent(
        self,
        user_id: int,
        ip_address: Optional[str] = None,
        request_guild_id: Optional[int] = None,
        request_channel_id: Optional[int] = None,
        request_message_id: Optional[int] = None,
        request_source: Optional[str] = None,
    ) -> dict[str, Any]:
        tos_version = self.get_tos_version()
        record = {
            "user_id": str(user_id),
            "consented_at": _to_iso(_utc_now()),
            "ip_address": ip_address or "nicht verfügbar (Discord liefert keine IP-Adresse)",
            "tos_version": tos_version,
            "revoked": False,
            "revoked_at": None,
            "last_request": {
                "guild_id": str(request_guild_id) if request_guild_id is not None else None,
                "channel_id": str(request_channel_id) if request_channel_id is not None else None,
                "message_id": str(request_message_id) if request_message_id is not None else None,
                "source": str(request_source or "").strip() or None,
                "requested_at": _to_iso(_utc_now()),
            },
        }
        async with self._lock:
            data = self._load()
            users = data.setdefault("users", {})
            users[str(user_id)] = record
            data["schema_version"] = int(data.get("schema_version") or 2)
            self._save(data)
        await self.log_event(
            action="zustimmung_gespeichert",
            actor_user_id=user_id,
            target_user_id=user_id,
            guild_id=request_guild_id,
            channel_id=request_channel_id,
            message_id=request_message_id,
            extra={"tos_version": tos_version, "source": request_source or None},
        )
        return record

    async def revokeConsent(self, user_id: int) -> bool:
        async with self._lock:
            data = self._load()
            users = data.get("users", {})
            record = users.get(str(user_id))
            if not isinstance(record, dict):
                return False
            record["revoked"] = True
            record["revoked_at"] = _to_iso(_utc_now())
            users[str(user_id)] = record
            data["schema_version"] = int(data.get("schema_version") or 2)
            self._save(data)
        await self.log_event(action="zustimmung_widerrufen", actor_user_id=user_id, target_user_id=user_id)
        return True

    async def deleteConsent(self, user_id: int, actor_user_id: Optional[int] = None, purge_audit: bool = False) -> bool:
        async with self._lock:
            data = self._load()
            users = data.get("users", {})
            if not isinstance(users, dict) or str(user_id) not in users:
                return False
            users.pop(str(user_id), None)
            data["users"] = users
            if purge_audit:
                audit_log = data.get("audit_log", [])
                if isinstance(audit_log, list):
                    data["audit_log"] = [
                        e for e in audit_log
                        if not isinstance(e, dict) or e.get("target_user_id") != str(user_id)
                    ]
            data["schema_version"] = int(data.get("schema_version") or 2)
            self._save(data)
        await self.log_event(
            action="zustimmung_geloescht",
            actor_user_id=actor_user_id,
            target_user_id=user_id,
            extra={"purge_audit": bool(purge_audit)},
        )
        return True

    async def getConsentRecord(self, user_id: int) -> Optional[dict[str, Any]]:
        async with self._lock:
            data = self._load()
            users = data.get("users", {})
            record = users.get(str(user_id)) if isinstance(users, dict) else None
            return record if isinstance(record, dict) else None

    async def listConsentUserIds(self) -> list[str]:
        async with self._lock:
            data = self._load()
            users = data.get("users", {})
            if not isinstance(users, dict):
                return []
            return sorted([str(k) for k in users.keys() if str(k).isdigit()], key=lambda x: int(x))

    async def getAllConsentRecords(self) -> dict[str, dict[str, Any]]:
        async with self._lock:
            data = self._load()
            users = data.get("users", {})
            if not isinstance(users, dict):
                return {}
            out: dict[str, dict[str, Any]] = {}
            for k, v in users.items():
                if isinstance(v, dict):
                    out[str(k)] = dict(v)
            return out

    async def searchConsentUserIds(self, query: str, limit: int = 25) -> list[str]:
        q = (query or "").strip()
        if not q:
            return []
        user_ids = await self.listConsentUserIds()
        hits = [uid for uid in user_ids if q in uid]
        return hits[: max(1, int(limit))]

    async def getAuditLog(self, target_user_id: Optional[int] = None, limit: int = 50) -> list[dict[str, Any]]:
        async with self._lock:
            data = self._load()
            audit_log = data.get("audit_log", [])
            if not isinstance(audit_log, list):
                return []
            entries = [e for e in audit_log if isinstance(e, dict)]
            if target_user_id is not None:
                entries = [e for e in entries if e.get("target_user_id") == str(target_user_id)]
            return entries[-max(1, int(limit)) :]

    async def requestConsent(self, message: discord.Message) -> bool:
        view = _ConsentRequestView(manager=self, user_id=message.author.id, timeout=20)
        tos_version = self.get_tos_version()
        tos_link = self.tos_url or "nicht konfiguriert"
        view.request_context = {
            "guild_id": getattr(getattr(message, "guild", None), "id", None),
            "channel_id": getattr(getattr(message, "channel", None), "id", None),
            "message_id": getattr(message, "id", None),
            "source": "ki_bild_upload",
        }
        text = (
            "Für Bild-Uploads an externe KI-Dienste brauche ich deine ausdrückliche Einwilligung.\n\n"
            f"ToS-Version: {tos_version}\n"
            f"ToS-Link: {tos_link}\n\n"
            "Mit deiner Zustimmung verpflichtest du dich zusätzlich, keine NSFW- oder sonstigen rechtswidrigen Inhalte zu übermitteln oder anzufordern. "
            "Bilder müssen für Personen unter 18 Jahren geeignet sein und den Discord-Regeln sowie dem jeweils anwendbaren Recht entsprechen.\n"
            "Wichtig: Nach deiner Zustimmung gilt ein Haftungsausschluss für den Entwickler für Inhalte/Antworten externer Anbieter.\n"
            f"Die Einwilligung gilt dann für {self.renew_days} Tage oder bis die ToS geändert werden.\n"
            "Du kannst jederzeit abbrechen."
        )
        sent = await message.reply(text, view=view, mention_author=False)
        view.message = sent
        allowed = await view.wait_result()
        return bool(allowed)

    async def requestConsentInteraction(
        self,
        interaction: discord.Interaction,
        request_guild_id: Optional[int] = None,
        request_channel_id: Optional[int] = None,
        request_message_id: Optional[int] = None,
        request_source: str = "slash_ki_bild",
    ) -> bool:
        view = _ConsentRequestView(manager=self, user_id=interaction.user.id, timeout=60)
        tos_version = self.get_tos_version()
        tos_link = self.tos_url or "nicht konfiguriert"
        view.request_context = {
            "guild_id": request_guild_id,
            "channel_id": request_channel_id,
            "message_id": request_message_id,
            "source": request_source or "slash_ki_bild",
        }

        text = (
            "🖼️ **Einwilligung für Bild-Analyse erforderlich**\n\n"
            "✅ Wenn du zustimmst, darf ich dein Bild für KI-Analyse an externe KI-Dienste übertragen.\n"
            "❌ Ohne Zustimmung wird nichts hochgeladen oder verarbeitet.\n\n"
            f"ToS-Version: {tos_version}\n"
            f"ToS-Link: {tos_link}\n\n"
            "Mit deiner Zustimmung verpflichtest du dich zusätzlich, keine NSFW- oder sonstigen rechtswidrigen Inhalte zu übermitteln oder anzufordern. "
            "Bilder müssen für Personen unter 18 Jahren geeignet sein und den Discord-Regeln sowie dem jeweils anwendbaren Recht entsprechen.\n"
            f"Die Einwilligung gilt dann für {self.renew_days} Tage oder bis die ToS geändert werden."
        )

        try:
            if interaction.response.is_done():
                sent = await interaction.followup.send(text, view=view, ephemeral=True)
            else:
                await interaction.response.send_message(text, view=view, ephemeral=True)
                sent = await interaction.original_response()
        except Exception:
            return False

        view.message = sent
        allowed = await view.wait_result()
        return bool(allowed)


class _ConsentModal(discord.ui.Modal):
    def __init__(self, manager: ConsentManager, user_id: int, parent_view: "_ConsentRequestView"):
        super().__init__(title="Einwilligung für Bild-Uploads", timeout=None)
        self._manager = manager
        self._user_id = int(user_id)
        self._parent_view = parent_view
        self._confirm = discord.ui.TextInput(
            label="Bitte exakt eintippen: ICH STIMME ZU",
            placeholder="ICH STIMME ZU",
            required=True,
            max_length=50,
        )
        self.add_item(self._confirm)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if interaction.user.id != self._user_id:
            await interaction.response.send_message("Das ist nicht deine Einwilligungsabfrage.", ephemeral=True)
            return

        value = (self._confirm.value or "").strip()
        if value != "ICH STIMME ZU":
            await interaction.response.send_message("Eingabe stimmt nicht. Bitte exakt `ICH STIMME ZU` eintippen.", ephemeral=True)
            return

        ctx = getattr(self._parent_view, "request_context", None)
        if isinstance(ctx, dict):
            request_guild_id = ctx.get("guild_id")
            request_channel_id = ctx.get("channel_id")
            request_message_id = ctx.get("message_id")
            request_source = ctx.get("source") or "ki_bild_upload"
        else:
            request_message = getattr(self._parent_view, "message", None)
            request_guild_id = getattr(getattr(request_message, "guild", None), "id", None)
            request_channel_id = getattr(getattr(request_message, "channel", None), "id", None)
            request_message_id = getattr(request_message, "id", None)
            request_source = "ki_bild_upload"
        await self._manager.storeConsent(
            self._user_id,
            request_guild_id=request_guild_id,
            request_channel_id=request_channel_id,
            request_message_id=request_message_id,
            request_source=request_source,
        )
        await interaction.response.send_message(
            f"Einwilligung gespeichert. Ab jetzt kannst du für {self._manager.renew_days} Tage Bilder senden, ohne jedes Mal zu bestätigen.",
            ephemeral=True,
        )
        await self._parent_view.finish(True)


class _ConsentRequestView(discord.ui.View):
    def __init__(self, manager: ConsentManager, user_id: int, timeout: int = 20):
        super().__init__(timeout=timeout)
        self.manager = manager
        self.user_id = int(user_id)
        self.message: Optional[discord.Message] = None
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()
        self._result: asyncio.Future[bool] = loop.create_future()

    async def wait_result(self) -> bool:
        try:
            return await self._result
        except Exception:
            return False

    async def finish(self, allowed: bool) -> None:
        if not self._result.done():
            self._result.set_result(bool(allowed))
        for item in self.children:
            if hasattr(item, "disabled"):
                item.disabled = True
        if self.message is not None:
            try:
                await self.message.edit(view=self)
            except Exception:
                pass
        self.stop()

    async def on_timeout(self) -> None:
        if not self._result.done():
            self._result.set_result(False)
        for item in self.children:
            if hasattr(item, "disabled"):
                item.disabled = True
        if self.message is not None:
            try:
                await self.message.edit(
                    content="Zeitüberschreitung - Zustimmung erforderlich. Bitte nutze den Bot-Kontakt für Support.",
                    view=self,
                )
            except Exception:
                pass
        self.stop()

    @discord.ui.button(label="✅ Zustimmen", style=discord.ButtonStyle.success)
    async def grant(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Das ist nicht deine Einwilligungsabfrage.", ephemeral=True)
            return
        await interaction.response.send_modal(_ConsentModal(manager=self.manager, user_id=self.user_id, parent_view=self))

    @discord.ui.button(label="❌ Ablehnen", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Das ist nicht deine Einwilligungsabfrage.", ephemeral=True)
            return
        await interaction.response.send_message("❌ Abgebrochen. Ohne Zustimmung wird nichts hochgeladen.", ephemeral=True)
        await self.finish(False)
