from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.usuario import UsuarioRegistro, UsuarioRespuesta
from app.controllers import auth as auth_controller
from app.core.database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.usuario import Token
from app.core.security import crear_access_token, crear_refresh_token
from fastapi import HTTPException, status

router = APIRouter(prefix="/auth", tags=["Auth"])

# Dependencia para sacar la sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/registro", response_model=UsuarioRespuesta, status_code=201)
def registro(datos: UsuarioRegistro, db: Session = Depends(get_db)):
    return auth_controller.registrar_usuario(datos, db)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm usa 'username' por defecto, ahí meteremos el email
    usuario = auth_controller.autenticar_usuario(db, form_data.username, form_data.password)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not usuario.activo:
        raise HTTPException(status_code=403, detail="El usuario está inactivo")
    
    # Fabricar las llaves si pasa las validaciones
    access_token = crear_access_token(data={"sub": usuario.email, "rol": usuario.rol.value})
    refresh_token = crear_refresh_token(data={"sub": usuario.email})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }