from pydantic import BaseModel
from datetime import date
from typing import Optional, Literal


class DocenteResumen(BaseModel):
    id_docente: int
    numero_usuario: str

    class Config:
        from_attributes = True


class ExamenBase(BaseModel):
    nombre_examen: str
    fecha_aplicacion: date
    estatus: Literal["activo", "inactivo", "borrador"] = "activo"


class ExamenCreate(ExamenBase):
    pass


class ExamenUpdate(BaseModel):
    nombre_examen: Optional[str] = None
    fecha_aplicacion: Optional[date] = None
    estatus: Optional[Literal["activo", "inactivo", "borrador"]] = None


class ExamenResponse(ExamenBase):
    id_examen: int
    id_docente: int
    total_reactivos: int

    docente: Optional[DocenteResumen]

    class Config:
        from_attributes = True
