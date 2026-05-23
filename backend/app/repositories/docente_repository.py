from sqlalchemy.orm import Session
from app.models.docente import Docente


def crear_docente(db: Session, docente: Docente):
    db.add(docente)
