from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

routerU= APIRouter(
    prefix="/v1/usuarios", 
    tags= ['CRUD HTTP']
)
    
@routerU.get("/")
async def consultaT():
    return{
        
        "status":"200",
        "total": len(usuarios),
        "data": usuarios
        
    }
    
@routerU.post("/",status_code=status.HTTP_201_CREATED)
async def crea_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
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
    
@routerU.put("/{id}", status_code=status.HTTP_200_OK)
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


@routerU.delete("/{id}", status_code=status.HTTP_200_OK)
async def elimina_usuario(id: int, userAuth: str = Depends(verificar_peticion)):

    for index, usuario in enumerate(usuarios):
        if usuario["id"] == id:
            usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado por {userAuth}",
                
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )