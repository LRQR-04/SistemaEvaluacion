from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base


class Estudiante(Base):
    __tablename__ = "estudiantes"

    id_estudiante = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    matricula = Column(String(30), unique=True)
    grupo = Column(String(30))

    usuario = relationship("Usuario", back_populates="estudiante")
    resultados = relationship(
        "Resultado",
        back_populates="estudiante",
    )
