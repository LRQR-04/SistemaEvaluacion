from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship
from datetime import datetime

from app.config.database import Base


class Resultado(Base):
    __tablename__ = "resultados"

    id_resultado = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    id_estudiante = Column(
        Integer,
        ForeignKey("estudiantes.id_estudiante"),
        nullable=False,
    )
    id_examen = Column(
        Integer,
        ForeignKey("examenes.id_examen"),
        nullable=False,
    )
    calificacion = Column(
        Float,
        nullable=False,
        default=0,
    )
    fecha_evaluacion = Column(
        DateTime,
        default=datetime.utcnow,
    )

    estudiante = relationship(
        "Estudiante",
        back_populates="resultados",
    )
    examen = relationship(
        "Examen",
        back_populates="resultados",
    )
    respuestas = relationship(
        "Respuesta",
        back_populates="resultado",
        cascade="all, delete-orphan",
    )
