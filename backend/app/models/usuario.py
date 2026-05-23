from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    apellido_paterno = Column(String(100))
    apellido_materno = Column(String(100))
    email = Column(String(100), unique=True)
    contrasenia = Column(String(255))
    rol = Column(String(20))
    estado = Column(String(20), default="activo")

    estudiante = relationship("Estudiante", back_populates="usuario", uselist=False)
    docente = relationship("Docente", back_populates="usuario", uselist=False)
