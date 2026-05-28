from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base
from app.models.examen import Examen


class Docente(Base):
    __tablename__ = "docentes"

    id_docente = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    numero_usuario = Column(String(30), unique=True)
    especialidad = Column(String(100))

    usuario = relationship("Usuario", back_populates="docente")
    examenes = relationship(
        "Examen",
        back_populates="docente",
    )
