from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from app.models.usuario import Usuario, RolUsuario
from app.models.socio import Socio
from app.schemas.usuario import UsuarioRegistro
from app.core.security import hashear_password, verificar_password

def registrar_usuario(datos: UsuarioRegistro, db: Session):
    # Validar que el email no exista (regla 409)
    if db.execute(select(Usuario).where(Usuario.email == datos.email.lower())).scalar_one_or_none():
        raise HTTPException(status_code=409, detail="El email ya está registrado en usuarios")
    
    if db.execute(select(Socio).where(Socio.email == datos.email.lower())).scalar_one_or_none():
        raise HTTPException(status_code=409, detail="El email ya pertenece a un socio")

    # 1. Crear el socio vinculado
    nuevo_socio = Socio(
        nombre=datos.nombre.title(),
        email=datos.email.lower(),
        telefono=datos.telefono
    )
    db.add(nuevo_socio)
    db.flush() # Manda a la BD para obtener el ID, pero sin hacer commit definitivo

    # 2. Crear el usuario usando el ID del socio y hasheando la contraseña Argon2
    nuevo_usuario = Usuario(
        email=datos.email.lower(),
        nombre=datos.nombre.title(),
        password_hash=hashear_password(datos.password),
        rol=RolUsuario.socio,
        socio_id=nuevo_socio.id
    )
    db.add(nuevo_usuario)
    db.commit() # Ahora sí guarda todo junto
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario

def autenticar_usuario(db: Session, email: str, password: str):
    usuario = db.execute(select(Usuario).where(Usuario.email == email)).scalar_one_or_none()
    if not usuario:
        return None
    # Verificar que la clave coincida con el hash de Argon2
    if not verificar_password(password, usuario.password_hash):
        return None
    return usuario