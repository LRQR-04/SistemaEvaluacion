from fastapi import APIRouter, Depends, Query

from sqlalchemy.orm import Session

from app.schemas.schema_usuario import (
    EstudianteActivoResponse,
    EstudiantePaginadoResponse,
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
)

from app.services.service_usuario import (
    registrar_usuario,
    obtener_usuarios,
    obtener_estudiantes,
    obtener_docentes,
    actualizar_usuario,
    cambiar_estado_usuario,
    obtener_estudiantes_activos,
)

from app.config.database import get_db

from app.middleware.middleware_roles import require_roles
from app.middleware.middleware_autenticacion import obtener_usuario_actual

from app.models.usuario import Usuario
from app.models.docente import Docente
from app.models.estudiante import Estudiante

router = APIRouter(prefix="", tags=["Usuarios"])


@router.get("/usuarios", dependencies=[Depends(require_roles("admin"))])
def listar_usuarios(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    nombre: str = Query(""),
    correo: str = Query(""),
    rol: str = Query(""),
    estado: str = Query(""),
    db: Session = Depends(get_db),
):
    """
    Lista todos los usuarios del sistema.
    """
    return obtener_usuarios(
        db=db,
        page=page,
        limit=limit,
        nombre=nombre,
        correo=correo,
        rol=rol,
        estado=estado,
    )


@router.get(
    "/estudiantes",
    response_model=EstudiantePaginadoResponse,
    dependencies=[Depends(require_roles("admin", "docente"))],
)
def listar_estudiantes(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    nombre: str = Query(""),
    matricula: str = Query(""),
    grupo: str = Query(""),
    db: Session = Depends(get_db),
):
    """
    Lista de estudiantes.
    """

    return obtener_estudiantes(
        db=db,
        page=page,
        limit=limit,
        nombre=nombre,
        matricula=matricula,
        grupo=grupo,
    )


@router.get(
    "/estudiantes/activos",
    response_model=list[EstudianteActivoResponse],
    dependencies=[Depends(require_roles("admin", "docente"))],
)
def listar_estudiantes_activos(
    db: Session = Depends(get_db),
):
    """
    Lista únicamente estudiantes activos.
    """

    return obtener_estudiantes_activos(db)


@router.get(
    "/docentes",
    dependencies=[Depends(require_roles("admin"))],
)
def listar_docentes(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    nombre: str = Query(""),
    numero_usuario: str = Query(""),
    db: Session = Depends(get_db),
):
    """
    Lista de docentes.
    """

    return obtener_docentes(
        db=db,
        page=page,
        limit=limit,
        nombre=nombre,
        numero_usuario=numero_usuario,
    )


@router.get("/docentes/usuario/{id_usuario}")
def obtener_docente_por_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
):
    docente = db.query(Docente).filter(Docente.id_usuario == id_usuario).first()

    return docente


@router.get("/estudiantes/usuario/{id_usuario}")
def obtener_estudiante_por_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
):
    estudiante = (
        db.query(Estudiante).filter(Estudiante.id_usuario == id_usuario).first()
    )

    return estudiante


@router.post(
    "/usuarios",
    dependencies=[Depends(require_roles("admin"))],
    response_model=UsuarioResponse,
)
def crear_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
):
    """
    Crear usuario.
    """

    return registrar_usuario(
        db,
        usuario,
    )


@router.put(
    "/usuarios/{id_usuario}",
    dependencies=[Depends(require_roles("admin"))],
    response_model=UsuarioResponse,
)
def editar_usuario(
    id_usuario: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(obtener_usuario_actual),
):
    """
    Editar usuario.
    """

    return actualizar_usuario(
        db=db,
        id_usuario=id_usuario,
        data=data,
        current_user=current_user,
    )


@router.patch(
    "/usuarios/{id_usuario}/estado",
    dependencies=[Depends(require_roles("admin"))],
)
def cambiar_estado(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(obtener_usuario_actual),
):
    """
    Activar/suspender usuario.
    """

    return cambiar_estado_usuario(
        db=db,
        id_usuario=id_usuario,
        current_user=current_user,
    )
