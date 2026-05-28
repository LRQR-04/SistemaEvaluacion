from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship

from app.config.database import Base


class Pregunta(Base):
    __tablename__ = "preguntas"

    id_pregunta = Column(Integer, primary_key=True, index=True)
    id_examen = Column(
        Integer,
        ForeignKey("examenes.id_examen"),
        nullable=False,
    )
    pregunta = Column(Text, nullable=False)
    opcion_a = Column(String(255), nullable=False)
    opcion_b = Column(String(255), nullable=False)
    opcion_c = Column(String(255), nullable=False)
    respuesta_correcta = Column(
        Enum("a", "b", "c", name="respuesta_correcta_enum"),
        nullable=False,
    )
    estatus = Column(
        Enum("activa", "inactiva", name="estatus_pregunta"),
        default="activa",
        nullable=False,
    )

    examen = relationship(
        "Examen",
        back_populates="preguntas",
    )
    respuestas = relationship(
        "Respuesta",
        back_populates="pregunta",
    )
