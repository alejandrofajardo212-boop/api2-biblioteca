from fastapi import Query, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.usuario import Usuario

settings = get_settings()

# Esto le dice a FastAPI dónde está el login y activa el botón "Authorize" en Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Su función original de paginación
def paginacion_params(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(10, ge=1, le=100, description="Límite de registros por página")
) -> dict:
    return {"skip": skip, "limit": limit}

# Dependencia de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para sacar el usuario actual a partir del token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credenciales_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="El token ha expirado")
    except jwt.InvalidTokenError:
        raise credenciales_exception

    usuario = db.execute(select(Usuario).where(Usuario.email == email)).scalar_one_or_none()
    if usuario is None or not usuario.activo:
        raise credenciales_exception
    
    return usuario

# Verificador dinámico de roles (Admin, Bibliotecario, Socio)
class RoleChecker:
    def __init__(self, roles_permitidos: list[str]):
        self.roles_permitidos = roles_permitidos

    def __call__(self, usuario: Usuario = Depends(get_current_user)):
        if usuario.rol.value not in self.roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos suficientes para realizar esta acción"
            )
        return usuario