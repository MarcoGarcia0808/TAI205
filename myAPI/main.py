#1. importaciones
from fastapi import FastAPI

#2. Inicialización de la aplicación
app = FastAPI()

#3. endpoints de la API
@app.get("/")
async def holaMundo():
    return {"message": "Hola Mundo desde FastAPI"}

@app.get("/bienvenidos")
async def bien():
    return {"message": "bienvenidos a mi API con FastAPI"}
