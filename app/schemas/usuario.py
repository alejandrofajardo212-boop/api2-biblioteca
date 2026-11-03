from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime
import re
from app.models.usuario import RolUsuario

class UsuarioRespuesta(BaseModel):
    id: int
    email: EmailStr
    nombre: str
    rol: RolUsuario
    activo: bool
    socio_id: Optional[int]
    creado_en: datetime

    model_config = {"from_attributes": True}

class UsuarioRegistro(BaseModel):
    email: EmailStr
    nombre: str = Field(min_length=3, max_length=100)
    telefono: Optional[str] = Field(default=None, max_length=20)
    password: str = Field(min_length=8, max_length=64)
    confirmar_password: str

    @field_validator("password")
    @classmethod
    def validar_password(cls, v: str) -> str:
        if not re.search(r'[A-Z]', v):
            raise ValueError('La contraseña debe tener al menos una mayúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('La contraseña debe tener al menos una minúscula')
        if not re.search(r'\d', v):
            raise ValueError('La contraseña debe tener al menos un número')
        return v

    @model_validator(mode="after")
    def verificar_passwords(self) -> 'UsuarioRegistro':
        if self.password != self.confirmar_password:
            raise ValueError('Las contraseñas no coinciden')
        return self

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str