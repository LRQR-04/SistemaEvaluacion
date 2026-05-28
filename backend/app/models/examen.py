from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.config.database import Base

from app.models.pregunta import Pregunta


class Examen(Base):
    __tablename__ = "examenes"

    id_examen = Column(Integer, primary_key=True, index=True)
    id_docente = Column(
        Integer,
        ForeignKey("docentes.id_docente"),
        nullable=False,
    )
    nombre_examen = Column(String(150), nullable=False)
    fecha_aplicacion = Column(Date, nullable=False)
    total_reactivos = Column(Integer, default=0)
    estatus = Column(
        Enum("activo", "inactivo", "borrador", name="estatus_examen"),
        default="activo",
        nullable=False,
    )

    docente = relationship(
        "Docente",
        back_populates="examenes",
    )
    preguntas = relationship(
        "Pregunta",
        back_populates="examen",
        cascade="all, delete-orphan",
    )
    resultados = relationship(
        "Resultado",
        back_populates="examen",
    )
