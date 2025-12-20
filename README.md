# Task Manager API – Backend

## Backend de una aplicación de gestión de tareas desarrollado con FastAPI, enfocado en autenticación con JWT y operaciones CRUD protegidas por usuario.

El objetivo del proyecto fue profundizar conocimientos en Python, FastAPI y arquitectura backend moderna, incorporando buenas prácticas como testing automatizado, contenedorización con Docker y validación continua mediante CI.

---

### Funcionalidades
 - Registro de usuarios
 - Login con JWT (access token)
 - Logout real mediante revocación de tokens
 - CRUD completo de tareas y recordatorios
 - Tareas y recordatorios asociadas a un usuario autenticado
 - Filtrado de tareas por estado
 - Protección de rutas con dependencias (Depends)
 - Validación de datos con Pydantic
 - ORM con SQLAlchemy
 - Unit Testing de auth y módulo de tasks 

---

### Tecnologías utilizadas
 - Python
 - FastAPI
 - SQLAlchemy
 - Pydantic
 - PostgreSQL
 - JWT (JSON Web Tokens)
 - Uvicorn
 - pgAdmin
 - Pytest
 - Docker & Docker Compose
 - GitHub Actions (CI)

---

### Testing y CI

El proyecto cuenta con tests unitarios implementados con Pytest, enfocados principalmente en autenticación y operaciones sobre tareas. Además, se incorporó Integración Continua (CI) mediante GitHub Actions, que ejecuta automáticamente en cada push o pull request:
- Instalación del proyecto en un entorno limpio
- Levantamiento de una base de datos PostgreSQL en contenedor
- Inicialización del esquema de la base de datos
- Ejecución completa de la suite de tests
