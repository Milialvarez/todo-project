# Task Manager API – Backend

## Backend de una aplicación de gestión de tareas desarrollado con FastAPI, enfocado en autenticación con JWT y operaciones CRUD protegidas por usuario.

El objetivo del proyecto fue profundizar conocimientos en Python, FastAPI y arquitectura backend moderna, incorporando buenas prácticas como testing automatizado, contenedorización con Docker y validación continua mediante CI.

---

### Funcionalidades
 - Registro de usuarios
 - Login con JWT (access token)
 - Logout real mediante revocación de tokens
 - Refresh token para mantener sesiones activas
 - CRUD completo de tareas y recordatorios
 - Tareas y recordatorios asociadas a un usuario autenticado
 - Filtrado de tareas por estado
 - Diferenciación de usuarios por roles (admin vs user) con permisos especiales
 - Protección de rutas con dependencias (Depends)
 - Validación de datos con Pydantic
 - ORM con SQLAlchemy
 - Unit Testing de auth y módulo de tasks
 - Envío automático a las 9am de cada día a usuarios que tengan recordatorios para el día siguiente
 - Uso de middlewares de logging, custom exceptions y exception handlers

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
 - SMTP

---

### Testing y CI

El proyecto cuenta con tests unitarios implementados con Pytest, enfocados principalmente en autenticación y operaciones sobre tareas. Además, se incorporó Integración Continua (CI) mediante GitHub Actions, que ejecuta automáticamente en cada push o pull request:
- Instalación del proyecto en un entorno limpio
- Levantamiento de una base de datos PostgreSQL en contenedor
- Inicialización del esquema de la base de datos
- Ejecución completa de la suite de tests
