from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.usuario import Usuario, RolUsuario
from app.core.security import hashear_password

def crear_super_admin():
    db = SessionLocal()
    try:
        # Revisar si ya existe para no duplicarlo
        admin_existente = db.execute(select(Usuario).where(Usuario.email == "admin@biblioteca.com")).scalar_one_or_none()
        if admin_existente:
            print("El administrador ya existe en la base de datos.")
            return

        # Crear el admin (sin socio_id porque es del staff)
        nuevo_admin = Usuario(
            email="admin@biblioteca.com", 
            nombre="Super Administrador",
            password_hash=hashear_password("Admin123*"),
            rol=RolUsuario.admin,
            activo=True
        )
        db.add(nuevo_admin)
        db.commit()
        print("¡Administrador creado con éxito! Email: admin@biblioteca.com | Clave: Admin123*")
    except Exception as e:
        print(f"Error creando admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    crear_super_admin()