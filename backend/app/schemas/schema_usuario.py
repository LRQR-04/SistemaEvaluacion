from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional, Literal


class UsuarioBase(BaseModel):
    """
    Esquema base para representar un usuario.
    """

    nombre: str
    apellido_paterno: str
    apellido_materno: str

    email: EmailStr

    rol: Literal["estudiante", "docente", "admin"] = "estudiante"

    estado: Literal["activo", "inactivo"] = "activo"

    # Campos opcionales para estudiante
    matricula: Optional[str] = None
    grupo: Optional[str] = None

    # Campos opcionales para docente
    numero_usuario: Optional[str] = None
    especialidad: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    """
    Esquema para la creación de un usuario.
    """

    contrasenia: str

    @model_validator(mode="after")
    def validar_campos_por_rol(self):
        # Validaciones estudiante
        if self.rol == "estudiante":
            if not self.matricula:
                raise ValueError("La matrícula es obligatoria")

            if not self.grupo:
                raise ValueError("El grupo es obligatorio")

        # Validaciones docente
        elif self.rol == "docente":
            if not self.numero_usuario:
                raise ValueError("El número de usuario es obligatorio")

            if not self.especialidad:
                raise ValueError("La especialidad es obligatoria")

        return self


class UsuarioUpdate(BaseModel):
    """
    Esquema para la actualización parcial de un usuario.
    """

    nombre: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None

    email: Optional[EmailStr] = None

    rol: Optional[Literal["estudiante", "docente", "admin"]] = None

    estado: Optional[Literal["activo", "suspendido"]] = None

    # Estudiante
    matricula: Optional[str] = None
    grupo: Optional[str] = None

    # Docente
    numero_usuario: Optional[str] = None
    especialidad: Optional[str] = None


class UsuarioResponse(UsuarioBase):
    """
    Esquema de respuesta para representar un usuario.
    """

    id_usuario: int

    nombre: str
    apellido_paterno: str
    apellido_materno: str

    email: EmailStr

    rol: str
    estado: str

    class Config:
        """
        Configuración para permitir la conversión desde modelos ORM.
        """

        from_attributes = True
