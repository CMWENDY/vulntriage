from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Dependency(Base):
    __tablename__ = "dependencies"

    id: Mapped[int] = mapped_column(primary_key=True)
    scan_id: Mapped[int] = mapped_column(
        ForeignKey("scans.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(200))
    version: Mapped[str | None] = mapped_column(String(100))
    ecosystem: Mapped[str] = mapped_column(String(50))
    manifest_path: Mapped[str] = mapped_column(String(500))

    scan: Mapped["Scan"] = relationship(back_populates="dependencies")
    findings: Mapped[list["Finding"]] = relationship(back_populates="dependency")

