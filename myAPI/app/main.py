#1. importaciones
from fastapi import FastAPI, status, HTTPException
from typing import Optional
import asyncio

#2. Inicialización de la aplicación
app = FastAPI(title="Mi primer API", 
              description="Marco Antonio Resendiz Garcia",
              version="1.0.0"
              )

#BD ficticia

usuarios=[
    {"id":1, "nombre":"Marco", "edad":"21"},
    {"id":2, "nombre":"Ana", "edad":"22"},
    {"id":3, "nombre":"Luis", "edad":"23"},
]

#3. endpoints de la API
@app.get("/", tags=['inicio'])
async def holaMundo():
    return {"message": 'Hola Mundo desde FastAPI'}

@app.get("/v1/bienvenidos", tags=['inicio'])
async def bien():
    return {"message": "bienvenidos a mi API con FastAPI"}

@app.get("/v1/promedios", tags=['Calificaciones'])
async def promedio():
    await asyncio.sleep(3)  # Simulación de procesamiento, consulta a base de datos, etc.
    return {
            "Calificacion": "10",
            "estatus":"200"
            }
    
@app.get("/v1/usuario_o/{id}", tags=['parametros'])
async def consultaUno(id: int):
    await asyncio.sleep(3) 
    return {
        "resultado": f"Usuario consultado correctamente",
        "estatus": "200",
        }
    
    
@app.get("/v1/usuario_op/", tags=['parametro opcional'])
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(2) 
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return { "Usuario encontrado":id,"Datos": usuario}
            return {"Mensaje": "Usuario no encontrado"}
    else:
        return { "Aviso": "No se proporcionó ningún ID"}
    
@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def consultaT ():
    return{
        
        "status":"200",
        "total": len(usuarios),
        "data": usuarios
        
    }
    
@app.post("/v1/usuarios/}", tags=['CRUD HTTP'])
async def crea_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return {
        "mensaje": "Usuario creado correctamente",
        "status":"200",
        "usuario": usuario
    }
    
@app.put("/v1/usuarios/", tags=['CRUD HTTP'])
async def actualiza_usuario(id: int, datos: dict):

    for usuario in usuarios:
        if usuario["id"] == id:
            usuario.update(datos)
            return {
                "mensaje": "Usuario actualizado correctamente",
                "status": "200",
                "usuario": usuario
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


# DELETE - Eliminar usuario
@app.delete("/v1/usuarios/", tags=['CRUD HTTP'])
async def elimina_usuario(id: int):

    for index, usuario in enumerate(usuarios):
        if usuario["id"] == id:
            eliminado = usuarios.pop(index)
            return {
                "mensaje": "Usuario eliminado correctamente",
                "status": "200",
                "usuario_eliminado": eliminado
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )