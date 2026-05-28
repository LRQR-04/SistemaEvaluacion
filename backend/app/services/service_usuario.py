from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_

from app.models.usuario import Usuario
from app.models.estudiante import Estudiante
from app.models.docente import Docente

from app.schemas.schema_usuario import UsuarioCreate, UsuarioUpdate

from app.core.security import hashear_contrasenia

from app.repositories.usuario_repository import crear_usuario
from app.repositories.estudiante_repository import crear_estudiante
from app.repositories.docente_repository import crear_docente


def registrar_usuario(db: Session, user_data: UsuarioCreate) -> Usuario:
    """
    Registra un nuevo usuario en la base de datos.
    Dependiendo del rol, también registra en la tabla
    estudiantes o docentes.
    """
    try:
        existente = (
            db.query(Usuario)
            .filter(func.lower(Usuario.email) == user_data.email.lower())
            .first()
        )

        if existente:
            raise HTTPException(status_code=401, detail="El correo ya está registrado")

        hashed_password = hashear_contrasenia(user_data.contrasenia)

        nuevo_usuario = Usuario(
            nombre=user_data.nombre,
            apellido_paterno=user_data.apellido_paterno,
            apellido_materno=user_data.apellido_materno,
            email=user_data.email,
            contrasenia=hashed_password,
            rol=user_data.rol,
            estado="activo",
        )

        usuario_creado = crear_usuario(db, nuevo_usuario)

        # Registro como estudiante
        if user_data.rol == "estudiante":
            # Validar matrícula duplicada
            matricula_existente = (
                db.query(Estudiante)
                .filter(Estudiante.matricula == user_data.matricula)
                .first()
            )

            if matricula_existente:
                raise HTTPException(
                    status_code=400, detail="La matrícula ya está registrada"
                )

            nuevo_estudiante = Estudiante(
                id_usuario=usuario_creado.id_usuario,
                matricula=user_data.matricula,
                grupo=user_data.grupo,
            )

            crear_estudiante(db, nuevo_estudiante)

        # Registro como docente
        elif user_data.rol == "docente":
            # Validar número de usuario duplicado
            docente_existente = (
                db.query(Docente)
                .filter(Docente.numero_usuario == user_data.numero_usuario)
                .first()
            )

            if docente_existente:
                raise HTTPException(
                    status_code=400, detail="El número de usuario ya está registrado"
                )

            nuevo_docente = Docente(
                id_usuario=usuario_creado.id_usuario,
                numero_usuario=user_data.numero_usuario,
                especialidad=user_data.especialidad,
            )

            crear_docente(db, nuevo_docente)

        db.commit()
        return usuario_creado

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# Listar usuarios (paginación + filtros)
def obtener_usuarios(
    db: Session,
    page: int = 1,
    limit: int = 10,
    nombre: str = "",
    correo: str = "",
    rol: str = "",
    estado: str = "",
) -> dict:
    """
    Obtiene una lista de usuarios con filtros y paginación.
    """
    try:
        query = db.query(Usuario).options(
            joinedload(Usuario.estudiante),
            joinedload(Usuario.docente),
        )

        # Búsqueda por nombre
        if nombre:
            nombre = nombre.lower()
            query = query.filter(
                or_(
                    func.lower(Usuario.nombre).like(f"{nombre}%"),
                    func.lower(Usuario.apellido_paterno).like(f"{nombre}%"),
                    func.lower(Usuario.apellido_materno).like(f"{nombre}%"),
                )
            )

        # Filtro por correo
        query = query.filter(func.lower(Usuario.email).like(f"{correo.lower()}%"))

        # Filtro por rol
        if rol:
            query = query.filter(Usuario.rol == rol)

        # Filtro por estado
        if estado:
            if estado:
                query = query.filter(Usuario.estado == estado)

        total = query.count()

        usuarios = (
            query.order_by(Usuario.id_usuario.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {"data": usuarios, "total": total}

    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener usuarios")


# obtener estudiantes
def obtener_estudiantes(
    db: Session,
    page: int = 1,
    limit: int = 10,
    nombre: str = "",
    matricula: str = "",
    grupo: str = "",
):
    try:
        query = (
            db.query(Estudiante).options(joinedload(Estudiante.usuario)).join(Usuario)
        )

        # Filtro por nombre
        if nombre:
            nombre = nombre.lower()
            query = query.filter(
                or_(
                    func.lower(Usuario.nombre).like(f"{nombre}%"),
                    func.lower(Usuario.apellido_paterno).like(f"{nombre}%"),
                    func.lower(Usuario.apellido_materno).like(f"{nombre}%"),
                )
            )

        # Filtro por matricula
        if matricula:
            query = query.filter(Estudiante.matricula.like(f"{matricula}%"))

        # Filtro por grupo
        if grupo:
            query = query.filter(Estudiante.grupo.like(f"{grupo}%"))

        total = query.count()

        estudiantes = (
            query.order_by(Estudiante.id_estudiante.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "data": estudiantes,
            "total": total,
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al obtener estudiantes",
        )


def obtener_estudiantes_activos(db: Session):
    estudiantes = (
        db.query(
            Estudiante.id_estudiante,
            Usuario.nombre,
            Usuario.apellido_paterno,
            Usuario.apellido_materno,
        )
        .join(Usuario, Usuario.id_usuario == Estudiante.id_usuario)
        .filter(Usuario.estado == "activo")
        .all()
    )

    return estudiantes


# Obtener docentes
def obtener_docentes(
    db: Session,
    page: int = 1,
    limit: int = 10,
    nombre: str = "",
    numero_usuario: str = "",
):
    try:
        query = db.query(Docente).options(joinedload(Docente.usuario)).join(Usuario)

        # Filtro por nombre
        if nombre:
            nombre = nombre.lower()
            query = query.filter(
                or_(
                    func.lower(Usuario.nombre).like(f"{nombre}%"),
                    func.lower(Usuario.apellido_paterno).like(f"{nombre}%"),
                    func.lower(Usuario.apellido_materno).like(f"{nombre}%"),
                )
            )

        # Filtro por numero de usuario
        if numero_usuario:
            query = query.filter(Docente.numero_usuario.like(f"{numero_usuario}%"))

        total = query.count()

        docentes = (
            query.order_by(Docente.id_docente.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return {
            "data": docentes,
            "total": total,
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al obtener docentes",
        )


# Actualizar datos del usuario
def actualizar_usuario(
    db: Session,
    id_usuario: int,
    data: UsuarioUpdate,
    current_user: Usuario,
) -> Usuario:
    """
    Actualiza los datos de un usuario existente.
    """
    try:
        usuario = (
            db.query(Usuario)
            .options(
                joinedload(Usuario.estudiante),
                joinedload(Usuario.docente),
            )
            .filter(Usuario.id_usuario == id_usuario)
            .first()
        )

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # El admin no puede editar otros admins
        if usuario.rol == "admin" and usuario.id_usuario != current_user.id_usuario:
            raise HTTPException(
                status_code=403, detail="No es posible editar otro admin"
            )

        # validar email único si se modifica
        if data.email and data.email != usuario.email:
            existente = (
                db.query(Usuario)
                .filter(func.lower(Usuario.email) == data.email.lower())
                .first()
            )
            if existente:
                raise HTTPException(
                    status_code=400, detail="El correo ya está registrado"
                )

            usuario.email = data.email

        # Datos generales
        if data.nombre is not None:
            usuario.nombre = data.nombre

        if data.apellido_paterno is not None:
            usuario.apellido_paterno = data.apellido_paterno

        if data.apellido_materno is not None:
            usuario.apellido_materno = data.apellido_materno

        if data.estado is not None:
            usuario.estado = data.estado

        # Estudiante
        if usuario.rol == "estudiante" and usuario.estudiante:

            if data.matricula is not None:

                matricula_existente = (
                    db.query(Estudiante)
                    .filter(
                        Estudiante.matricula == data.matricula,
                        Estudiante.id_estudiante != usuario.estudiante.id_estudiante,
                    )
                    .first()
                )

                if matricula_existente:
                    raise HTTPException(
                        status_code=400,
                        detail="La matrícula ya está registrada",
                    )

                usuario.estudiante.matricula = data.matricula

            if data.grupo is not None:
                usuario.estudiante.grupo = data.grupo

        # Docente
        elif usuario.rol == "docente" and usuario.docente:

            if data.numero_usuario is not None:

                numero_existente = (
                    db.query(Docente)
                    .filter(
                        Docente.numero_usuario == data.numero_usuario,
                        Docente.id_docente != usuario.docente.id_docente,
                    )
                    .first()
                )

                if numero_existente:
                    raise HTTPException(
                        status_code=400,
                        detail="El número de usuario ya está registrado",
                    )

                usuario.docente.numero_usuario = data.numero_usuario

            if data.especialidad is not None:
                usuario.docente.especialidad = data.especialidad

        db.commit()
        db.refresh(usuario)

        return usuario

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al actualizar usuario")


# Cambiar estado del usuario
def cambiar_estado_usuario(
    db: Session,
    id_usuario: int,
    current_user: Usuario,
) -> dict:
    """
    Cambia el estado de un usuario (activo/suspendido).
    """
    try:
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # El admin no puede modificar otros admins
        if usuario.rol == "admin" and usuario.id_usuario != current_user.id_usuario:
            raise HTTPException(
                status_code=403, detail="No se puede modificar otro admin"
            )

        usuario.estado = "inactivo" if usuario.estado == "activo" else "activo"

        db.commit()

        return {"message": "Estado actualizado correctamente"}

    except HTTPException as e:
        db.rollback()
        raise e

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al cambiar estado")


def obtener_usuario_por_email(db: Session, email: str) -> Usuario | None:
    """
    Obtiene un usuario por su correo electrónico.
    """
    return db.query(Usuario).filter(func.lower(Usuario.email) == email.lower()).first()


# def verificar_usuario_activo(usuario: Usuario) -> bool:
#     """
#     Verifica si un usuario está activo.
#     """
#     return usuario.estado == "activo"
