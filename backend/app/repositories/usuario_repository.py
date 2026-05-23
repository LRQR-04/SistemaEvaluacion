from sqlalchemy.orm import Session
from app.models.usuario import Usuario


def crear_usuario(db: Session, usuario: Usuario) -> Usuario:
    db.add(usuario)
    db.flush()
    db.refresh(usuario)

    return usuario
