# Sistema Escolar

Sistema web desarrollado para la gestión y automatización de evaluaciones escolares mediante procesamiento OMR (Optical Mark Recognition), permitiendo administrar usuarios, exámenes y resultados de manera eficiente, segura y modular.

El sistema implementa una arquitectura basada en API REST utilizando FastAPI para el backend y Vue.js para el frontend, incorporando autenticación JWT, control de roles y procesamiento automático de hojas de respuestas mediante visión computacional con OpenCV.

---

# Características principales

- Gestión de usuarios
  - Administradores
  - Docentes
  - Estudiantes

- Sistema de autenticación con JWT

- Gestión de exámenes
  - Registro de exámenes
  - Administración de preguntas
  - Activación/desactivación de exámenes

- Evaluación automática mediante OMR
  - Procesamiento de hojas de respuestas
  - Detección automática de respuestas
  - Cálculo automático de calificaciones

- Gestión de resultados
  - Consulta de resultados por estudiante
  - Consulta de resultados por examen
  - Historial de evaluaciones

- Control de acceso por roles

- Arquitectura modular basada en capas

- Validación robusta de datos y manejo de errores

---

# Tecnologías utilizadas

## Backend

- Python 3.11+
- FastAPI
- SQLAlchemy ORM
- MySQL
- JWT Authentication
- OpenCV 4.13
- NumPy

## Frontend

- Vue.js 3
- Vite
- Axios
- Pinia
- Vue Router

---

# Estructura del proyecto

```bash
sistema-escolar/
│
├── backend/
│   ├── app/
│   │   ├── config/         # Configuración general y base de datos
│   │   ├── core/           # Utilizades generales
│   │   ├── middleware/     # Autenticación y control de roles
│   │   ├── models/         # Modelos ORM
│   │   ├── omr/            # Procesamiento OMR
│   │   ├── repositories/   # Acceso a datos
│   │   ├── routes/         # Endpoints API
│   │   ├── schemas/        # Esquemas y validaciones
│   │   └── services/       # Lógica de negocio
│   │
│   └── ...
│
├── database/
│
├── frontend/
│   ├── src/
│   │   ├── components/     # Componentes reutilizables
│   │   ├── layouts/        # Layouts
│   │   ├── router/         # Configuración de rutas
│   │   ├── services/       # Comunicación con API
│   │   ├── stores/         # Estado global
│   │   ├── views/          # Vistas principales
│   │   └── ...
│   │
│   └── ...
│
└── README.md
```

---

# Instalación y ejecución

## 1. Clonar repositorio

```bash
git clone https://github.com/LRQR-04/SistemaEvaluacion.git
cd sistema-escolar
```

---

# Backend

## 2. Crear entorno virtual

```bash
cd backend

python -m venv venv
```

### Activar entorno virtual

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4. Variables de entorno

Crear un archivo `.env` dentro de `backend/`

```env
DATABASE_URL=mysql+pymysql://usuario:password@localhost/sistema_escolar
SECRET_KEY=clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
```

---

## 5. Ejecutar servidor backend

```bash
cd backend
python run.py
```

Servidor disponible en:

```bash
http://localhost:8000
```

Documentación automática:

```bash
http://localhost:8000/docs
```

---

# Frontend

## 6. Instalar dependencias

```bash
cd frontend
npm install
```

---

## 7. Variables de entorno

Crear un archivo `.env` dentro de `frontend/`

```env
VITE_API_URL=http://localhost:8000
```

---

## 8. Ejecutar frontend

```bash
npm run dev
```

Frontend disponible en:

```bash
http://localhost:5173
```

---

# Arquitectura del sistema

El proyecto implementa una arquitectura modular basada en capas para mantener una separación clara de responsabilidades.

## Capas principales

- Routes
  - Definen los endpoints de la API REST

- Services
  - Implementan la lógica de negocio

- Repositories
  - Manejan consultas y operaciones con la base de datos

- Models
  - Representan las entidades ORM

- Schemas
  - Validación y serialización de datos

- Middleware
  - Control de autenticación y autorización

- OMR
  - Procesamiento de imágenes y detección de respuestas

---

# Procesamiento OMR

El sistema incorpora reconocimiento óptico de marcas (OMR) utilizando OpenCV para evaluar automáticamente hojas de respuestas.

## Funcionalidades implementadas

- Detección automática de hoja
- Corrección de perspectiva
- Conversión binaria de imagen
- Segmentación de preguntas
- Detección de respuestas marcadas
- Validación de respuestas múltiples
- Preguntas anuladas en caso de múltiples marcas
- Preguntas vacías detectadas como NULL
- Cálculo automático de calificación

---

# Módulos principales

## Usuarios

Permite administrar usuarios del sistema:

- Administradores
- Docentes
- Estudiantes

## Exámenes

Permite:

- Crear exámenes
- Registrar preguntas
- Configurar respuestas correctas
- Activar/desactivar evaluaciones

## Evaluación automática

Procesa hojas OMR y genera:

- Respuestas detectadas
- Aciertos
- Calificación final

## Resultados

Permite consultar:

- Resultados por estudiante
- Resultados por examen
- Historial de evaluaciones

---

# Seguridad

El sistema implementa:

- Autenticación JWT
- Control de acceso basado en roles
- Protección de rutas
- Validación de datos
- Manejo de excepciones HTTP

---

# Manejo de errores

El backend implementa manejo centralizado de errores utilizando:

- HTTPException
- Validaciones de FastAPI
- Respuestas controladas para errores OMR
- Validación de imágenes inválidas
- Validación de preguntas inconsistentes

---

# Estándares de desarrollo

- Arquitectura modular
- Separación de responsabilidades
- Código tipado
- Uso de ORM
- API REST
- Validación mediante esquemas
- Convenciones PEP 8

---

# Manual de uso

1. Ejecutar backend
2. Ejecutar frontend
3. Iniciar sesión
4. Gestionar usuarios y exámenes
5. Subir hoja OMR
6. Procesar evaluación
7. Consultar resultados

---

# Autor

- LRQR-04
- GitHub: https://github.com/LRQR-04

---
