import enum
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Enum as SQLAlchemyEnum, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class RolUsuario(str, enum.Enum):
    admin = "admin"
    bibliotecario = "bibliotecario"
    socio = "socio"

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[RolUsuario] = mapped_column(SQLAlchemyEnum(RolUsuario, name="rolusuario"), default=RolUsuario.socio, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    intentos_fallidos: Mapped[int] = mapped_column(default=0, nullable=False)
    bloqueado_hasta: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    socio_id: Mapped[int | None] = mapped_column(ForeignKey("socios.id"), unique=True, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)