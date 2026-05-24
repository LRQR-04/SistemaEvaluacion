from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.usuario import Usuario
from dotenv import load_dotenv

import os

load_dotenv()

# variables JWT
CLAVE_SECRETA = os.getenv("CLAVE_SECRETA")
ALGORITMO = os.getenv("ALGORITMO")

# Esquema de seguridad OAuth2 para autenticación con tokens JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Usuario:
    """
    Obtiene el usuario actual a partir de un token JWT.
    """
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        id_usuario = payload.get("user_id")

        if id_usuario is None:
            raise credenciales_exception

        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

        if not usuario:
            raise credenciales_exception

        # Validar estado del usuario
        if usuario.estado != "activo":

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario suspendido",
            )

        return usuario

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
