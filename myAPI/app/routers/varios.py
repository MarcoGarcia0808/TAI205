from fastapi import APIRouter

from typing import Optional
import asyncio
from app.data.database import usuarios

routerV= APIRouter( tags=['inicio'])


#3. endpoints de la API
@routerV.get("/")
async def holaMundo():
    return {"message": 'Hola Mundo desde FastAPI'}

@routerV.get("/v1/bienvenidos", tags=['inicio'])
async def bien():
    return {"message": "bienvenidos a mi API con FastAPI"}

@routerV.get("/v1/promedios")
async def promedio():
    await asyncio.sleep(3)  # Simulación de procesamiento, consulta a base de datos, etc.
    return {
            "Calificacion": "10",
            "estatus":"200"
            }
    

@routerV.get("/v1/usuario_o/{id}")
async def consultaUno(id: int):
    await asyncio.sleep(3) 
    return {
        "resultado": f"Usuario consultado correctamente",
        "estatus": "200",
        }
    
    
@routerV.get("/v1/usuario_op/")
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(2) 
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return { "Usuario encontrado":id,"Datos": usuario}
            return {"Mensaje": "Usuario no encontrado"}
    else:
        return { "Aviso": "No se proporcionó ningún ID"}
    
    