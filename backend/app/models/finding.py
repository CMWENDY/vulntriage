from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[int] = mapped_column(primary_key=True)
    scan_id: Mapped[int] = mapped_column(
        ForeignKey("scans.id", ondelete="CASCADE"), index=True
    )
    dependency_id: Mapped[int | None] = mapped_column(
        ForeignKey("dependencies.id", ondelete="CASCADE"), index=True
    )

    type: Mapped[str] = mapped_column(String(20))
    severity: Mapped[str] = mapped_column(String(20), index=True)
    status: Mapped[str] = mapped_column(String(20), default="open", index=True)
    summary: Mapped[str] = mapped_column(Text)
    cve_id: Mapped[str | None] = mapped_column(String(50), index=True)
    cwe_id: Mapped[str | None] = mapped_column(String(20))
    source_tool: Mapped[str] = mapped_column(String(50), default="osv")

    scan: Mapped["Scan"] = relationship(back_populates="findings")
    dependency: Mapped["Dependency | None"] = relationship(back_populates="findings")

