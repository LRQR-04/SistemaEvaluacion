from sqlalchemy.orm import Session
from app.models.usuario import Usuario


def crear_usuario(db: Session, usuario: Usuario) -> Usuario:
    db.add(usuario)
    db.flush()
    db.refresh(usuario)

    return usuario


def obtener_usuario_por_id(
    db: Session,
    id_usuario: int,
):
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
