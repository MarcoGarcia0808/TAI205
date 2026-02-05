# FastAPI REST API – Práctica

API REST desarrollada con FastAPI para practicar endpoints, asincronía,
manejo de parámetros y documentación automática.

## Tecnologías
- Python
- FastAPI
- Uvicorn
- Asyncio
- REST API
- JSON

## Funcionalidades
- Endpoints REST básicos
- Manejo de parámetros obligatorios y opcionales
- Operaciones asincrónicas con async/await
- Simulación de consultas a base de datos
- Documentación automática con Swagger y ReDoc

## Ejecución del proyecto

pip install fastapi uvicorn
uvicorn main:app --reload

## Documentación automática

FastAPI genera documentación automática a partir del código.

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Endpoints

- GET /Hola Mundo
- GET /v1/bienvenidos
- GET /v1/promedios
- GET /v1/usuario/{id}
- GET /v1/usuario_op/?id={id}

