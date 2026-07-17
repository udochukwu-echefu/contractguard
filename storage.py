"""Durable, owner-scoped storage for ContractGuard workspaces.

The repository defaults to SQLite for local development and accepts a
``DATABASE_URL`` for production Postgres deployments. All public reads and
writes require an owner identifier so one user's records cannot be retrieved
through another user's session.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, create_engine, delete, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _json(value: Any) -> str:
    return json.dumps(value if value is not None else {}, ensure_ascii=False, default=str)


def _from_json(value: str | None, fallback: Any) -> Any:
    if not value:
        return fallback
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return fallback


class Base(DeclarativeBase):
    pass


class ReviewRecord(Base):
    __tablename__ = "reviews"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    owner_id: Mapped[str] = mapped_column(String(255), index=True)
    organization_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    source_name: Mapped[str] = mapped_column(String(512))
    contract_type: Mapped[str] = mapped_column(String(255))
    analysis_json: Mapped[str] = mapped_column(Text)
    summary_json: Mapped[str] = mapped_column(Text)
    context_json: Mapped[str] = mapped_column(Text)
    quality_json: Mapped[str] = mapped_column(Text)
    comparison_json: Mapped[str] = mapped_column(Text, default="{}")
    messages_json: Mapped[str] = mapped_column(Text, default="[]")
    review_notes: Mapped[str] = mapped_column(Text, default="")
    source_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    retain_source_text: Mapped[bool] = mapped_column(Boolean, default=False)
    retention_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    playbook_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)


class PlaybookRecord(Base):
    __tablename__ = "playbooks"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    owner_id: Mapped[str] = mapped_column(String(255), index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, default="")
    contract_types_json: Mapped[str] = mapped_column(Text, default="[]")
    rules_json: Mapped[str] = mapped_column(Text, default="[]")
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class DecisionRecord(Base):
    __tablename__ = "review_decisions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    review_id: Mapped[str] = mapped_column(ForeignKey("reviews.id"), index=True)
    owner_id: Mapped[str] = mapped_column(String(255), index=True)
    finding_key: Mapped[str] = mapped_column(String(128), index=True)
    finding_type: Mapped[str] = mapped_column(String(64))
    finding_title: Mapped[str] = mapped_column(String(512))
    status: Mapped[str] = mapped_column(String(64))
    rationale: Mapped[str] = mapped_column(Text, default="")
    assigned_to: Mapped[str] = mapped_column(String(255), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class AuditEventRecord(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    review_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    owner_id: Mapped[str] = mapped_column(String(255), index=True)
    action: Mapped[str] = mapped_column(String(128))
    detail_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


@dataclass(frozen=True)
class StorageConfig:
    url: str
    local_only: bool


def storage_config() -> StorageConfig:
    configured = os.environ.get("DATABASE_URL", "").strip()
    if configured:
        if configured.startswith("postgres://"):
            configured = configured.replace("postgres://", "postgresql+psycopg://", 1)
        elif configured.startswith("postgresql://") and "+" not in configured.split("://", 1)[0]:
            configured = configured.replace("postgresql://", "postgresql+psycopg://", 1)
        return StorageConfig(configured, local_only=False)

    db_path = Path(os.environ.get("CONTRACTGUARD_DB_PATH", ".contractguard/contractguard.db"))
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return StorageConfig(f"sqlite:///{db_path.resolve()}", local_only=True)


class ReviewStore:
    def __init__(self, url: str | None = None):
        config = storage_config() if url is None else StorageConfig(url, url.startswith("sqlite"))
        kwargs: dict[str, Any] = {"pool_pre_ping": True}
        if config.url.startswith("sqlite"):
            kwargs["connect_args"] = {"check_same_thread": False}
        self.config = config
        self.engine = create_engine(config.url, **kwargs)
        Base.metadata.create_all(self.engine)

    def _audit(self, session: Session, owner_id: str, action: str, review_id: str | None, detail: Any = None) -> None:
        session.add(
            AuditEventRecord(
                id=str(uuid4()),
                owner_id=owner_id,
                review_id=review_id,
                action=action,
                detail_json=_json(detail or {}),
            )
        )

    def upsert_review(self, owner_id: str, review: dict[str, Any]) -> str:
        review_id = review.get("id") or str(uuid4())
        now = utcnow()
        retention_days = review.get("retention_days")
        retention_days_value = int(retention_days) if retention_days else None
        retain_source = bool(review.get("retain_source_text"))
        with Session(self.engine) as session:
            record = session.scalar(
                select(ReviewRecord).where(ReviewRecord.id == review_id, ReviewRecord.owner_id == owner_id)
            )
            action = "review.updated" if record else "review.created"
            if record is None:
                expires_at = now + timedelta(days=retention_days_value) if retention_days_value else None
                record = ReviewRecord(
                    id=review_id,
                    owner_id=owner_id,
                    organization_id=review.get("organization_id"),
                    source_name=review.get("source_name") or "Uploaded contract",
                    contract_type=review.get("contract_type") or "Unknown contract",
                    analysis_json="{}",
                    summary_json="{}",
                    context_json="{}",
                    quality_json="{}",
                    created_at=now,
                    expires_at=expires_at,
                )
                session.add(record)
            elif record.retention_days != retention_days_value:
                record.expires_at = now + timedelta(days=retention_days_value) if retention_days_value else None
            record.source_name = review.get("source_name") or record.source_name
            record.contract_type = review.get("contract_type") or record.contract_type
            record.analysis_json = _json(review.get("analysis"))
            record.summary_json = _json(review.get("summary"))
            record.context_json = _json(review.get("review_context"))
            record.quality_json = _json(review.get("document_quality"))
            record.comparison_json = _json(review.get("comparison"))
            record.messages_json = _json(review.get("messages") or [])
            record.review_notes = review.get("review_notes") or ""
            record.source_text = review.get("document_text") if retain_source else None
            record.retain_source_text = retain_source
            record.retention_days = retention_days_value
            record.playbook_id = review.get("playbook_id")
            record.updated_at = now
            self._audit(session, owner_id, action, review_id, {"source_name": record.source_name})
            session.commit()
        return review_id

    @staticmethod
    def _review_dict(record: ReviewRecord, include_detail: bool = True) -> dict[str, Any]:
        value: dict[str, Any] = {
            "id": record.id,
            "source_name": record.source_name,
            "contract_type": record.contract_type,
            "summary": _from_json(record.summary_json, {}),
            "created_at": record.created_at.astimezone().strftime("%b %d, %Y %I:%M %p"),
            "updated_at": record.updated_at.isoformat(),
            "retention_days": record.retention_days,
            "retain_source_text": record.retain_source_text,
            "playbook_id": record.playbook_id,
        }
        if include_detail:
            value.update(
                {
                    "analysis": _from_json(record.analysis_json, {}),
                    "review_context": _from_json(record.context_json, {}),
                    "document_quality": _from_json(record.quality_json, {}),
                    "comparison": _from_json(record.comparison_json, None),
                    "messages": _from_json(record.messages_json, []),
                    "review_notes": record.review_notes,
                    "document_text": record.source_text or "",
                }
            )
        return value

    def list_reviews(self, owner_id: str) -> list[dict[str, Any]]:
        self.purge_expired(owner_id)
        with Session(self.engine) as session:
            records = session.scalars(
                select(ReviewRecord)
                .where(ReviewRecord.owner_id == owner_id)
                .order_by(ReviewRecord.updated_at.desc())
            ).all()
            return [self._review_dict(record, include_detail=False) for record in records]

    def get_review(self, owner_id: str, review_id: str) -> dict[str, Any] | None:
        self.purge_expired(owner_id)
        with Session(self.engine) as session:
            record = session.scalar(
                select(ReviewRecord).where(ReviewRecord.id == review_id, ReviewRecord.owner_id == owner_id)
            )
            return self._review_dict(record) if record else None

    def delete_review(self, owner_id: str, review_id: str) -> bool:
        with Session(self.engine) as session:
            record = session.scalar(
                select(ReviewRecord).where(ReviewRecord.id == review_id, ReviewRecord.owner_id == owner_id)
            )
            if record is None:
                return False
            session.execute(delete(DecisionRecord).where(DecisionRecord.review_id == review_id, DecisionRecord.owner_id == owner_id))
            session.execute(delete(AuditEventRecord).where(AuditEventRecord.review_id == review_id, AuditEventRecord.owner_id == owner_id))
            session.delete(record)
            session.commit()
            return True

    def clear_reviews(self, owner_id: str) -> int:
        with Session(self.engine) as session:
            review_ids = list(session.scalars(select(ReviewRecord.id).where(ReviewRecord.owner_id == owner_id)))
            if review_ids:
                session.execute(delete(DecisionRecord).where(DecisionRecord.owner_id == owner_id, DecisionRecord.review_id.in_(review_ids)))
                session.execute(delete(AuditEventRecord).where(AuditEventRecord.owner_id == owner_id, AuditEventRecord.review_id.in_(review_ids)))
            result = session.execute(delete(ReviewRecord).where(ReviewRecord.owner_id == owner_id))
            session.commit()
            return int(result.rowcount or 0)

    def purge_expired(self, owner_id: str) -> int:
        now = utcnow()
        with Session(self.engine) as session:
            ids = list(
                session.scalars(
                    select(ReviewRecord.id).where(
                        ReviewRecord.owner_id == owner_id,
                        ReviewRecord.expires_at.is_not(None),
                        ReviewRecord.expires_at <= now,
                    )
                )
            )
            if not ids:
                return 0
            session.execute(delete(DecisionRecord).where(DecisionRecord.owner_id == owner_id, DecisionRecord.review_id.in_(ids)))
            session.execute(delete(AuditEventRecord).where(AuditEventRecord.owner_id == owner_id, AuditEventRecord.review_id.in_(ids)))
            session.execute(delete(ReviewRecord).where(ReviewRecord.owner_id == owner_id, ReviewRecord.id.in_(ids)))
            session.commit()
            return len(ids)

    def save_playbook(self, owner_id: str, playbook: dict[str, Any]) -> str:
        playbook_id = playbook.get("id") or str(uuid4())
        now = utcnow()
        with Session(self.engine) as session:
            record = session.scalar(
                select(PlaybookRecord).where(PlaybookRecord.id == playbook_id, PlaybookRecord.owner_id == owner_id)
            )
            if record is None:
                record = PlaybookRecord(id=playbook_id, owner_id=owner_id, name=playbook["name"], created_at=now)
                session.add(record)
            record.name = playbook["name"]
            record.description = playbook.get("description") or ""
            record.contract_types_json = _json(playbook.get("contract_types") or [])
            record.rules_json = _json(playbook.get("rules") or [])
            record.is_default = bool(playbook.get("is_default"))
            record.updated_at = now
            session.commit()
        return playbook_id

    @staticmethod
    def _playbook_dict(record: PlaybookRecord) -> dict[str, Any]:
        return {
            "id": record.id,
            "name": record.name,
            "description": record.description,
            "contract_types": _from_json(record.contract_types_json, []),
            "rules": _from_json(record.rules_json, []),
            "is_default": record.is_default,
            "updated_at": record.updated_at.isoformat(),
        }

    def list_playbooks(self, owner_id: str) -> list[dict[str, Any]]:
        with Session(self.engine) as session:
            records = session.scalars(
                select(PlaybookRecord)
                .where(PlaybookRecord.owner_id == owner_id)
                .order_by(PlaybookRecord.is_default.desc(), PlaybookRecord.name.asc())
            ).all()
            return [self._playbook_dict(record) for record in records]

    def get_playbook(self, owner_id: str, playbook_id: str | None) -> dict[str, Any] | None:
        if not playbook_id:
            return None
        with Session(self.engine) as session:
            record = session.scalar(
                select(PlaybookRecord).where(PlaybookRecord.id == playbook_id, PlaybookRecord.owner_id == owner_id)
            )
            return self._playbook_dict(record) if record else None

    def record_decision(self, owner_id: str, review_id: str, decision: dict[str, Any]) -> str:
        decision_id = str(uuid4())
        with Session(self.engine) as session:
            owns_review = session.scalar(
                select(ReviewRecord.id).where(ReviewRecord.id == review_id, ReviewRecord.owner_id == owner_id)
            )
            if not owns_review:
                raise ValueError("Review not found for this user.")
            record = DecisionRecord(
                id=decision_id,
                review_id=review_id,
                owner_id=owner_id,
                finding_key=decision["finding_key"],
                finding_type=decision.get("finding_type") or "risk",
                finding_title=decision.get("finding_title") or "Finding",
                status=decision["status"],
                rationale=decision.get("rationale") or "",
                assigned_to=decision.get("assigned_to") or "",
            )
            session.add(record)
            self._audit(
                session,
                owner_id,
                "decision.recorded",
                review_id,
                {"finding_key": record.finding_key, "status": record.status},
            )
            session.commit()
        return decision_id

    def list_decisions(self, owner_id: str, review_id: str) -> list[dict[str, Any]]:
        with Session(self.engine) as session:
            records = session.scalars(
                select(DecisionRecord)
                .where(DecisionRecord.owner_id == owner_id, DecisionRecord.review_id == review_id)
                .order_by(DecisionRecord.created_at.desc())
            ).all()
            return [
                {
                    "id": record.id,
                    "finding_key": record.finding_key,
                    "finding_type": record.finding_type,
                    "finding_title": record.finding_title,
                    "status": record.status,
                    "rationale": record.rationale,
                    "assigned_to": record.assigned_to,
                    "created_at": record.created_at.astimezone().strftime("%b %d, %Y %I:%M %p"),
                }
                for record in records
            ]

    def list_audit_events(self, owner_id: str, review_id: str, limit: int = 100) -> list[dict[str, Any]]:
        with Session(self.engine) as session:
            records = session.scalars(
                select(AuditEventRecord)
                .where(AuditEventRecord.owner_id == owner_id, AuditEventRecord.review_id == review_id)
                .order_by(AuditEventRecord.created_at.desc())
                .limit(limit)
            ).all()
            return [
                {
                    "action": record.action,
                    "detail": _from_json(record.detail_json, {}),
                    "created_at": record.created_at.astimezone().strftime("%b %d, %Y %I:%M %p"),
                }
                for record in records
            ]
