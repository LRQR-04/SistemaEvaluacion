from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.config.database import Base


class Respuesta(Base):
    __tablename__ = "respuestas"

    id_respuesta = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    id_resultado = Column(
        Integer,
        ForeignKey("resultados.id_resultado"),
        nullable=False,
    )
    id_pregunta = Column(
        Integer,
        ForeignKey("preguntas.id_pregunta"),
        nullable=False,
    )
    respuesta_alumno = Column(
        String(10),
        nullable=True,
    )
    es_correcta = Column(
        Boolean,
        default=False,
    )

    resultado = relationship(
        "Resultado",
        back_populates="respuestas",
    )

    pregunta = relationship(
        "Pregunta",
        back_populates="respuestas",
    )
