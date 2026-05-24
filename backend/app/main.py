from fastapi import FastAPI
from app.config.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.routes import routes_autenticacion, routes_usuario

app = FastAPI(title="Sistema Escolar")

# crear tablas automáticamente
Base.metadata.create_all(bind=engine)

# Configuración de CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# rutas
app.include_router(routes_autenticacion.router)
app.include_router(routes_usuario.router)


@app.get("/")
def root():
    return {"mensaje": "API funcionando bien"}
