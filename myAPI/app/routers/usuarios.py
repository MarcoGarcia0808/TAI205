from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session 
from app.data.db import  get_db
from app. data.usuario import usuario as usuarioDB

routerU= APIRouter(
    prefix="/v1/usuarios", 
    tags= ['CRUD HTTP']
)
    
@routerU.get("/")
async def consultaT(db:Session= Depends(get_db)):
    
    queryUsuarios= db.query(usuarioDB).all()
    return{
        
        "status":"200",
        "total": len(queryUsuarios),
        "data": queryUsuarios
        
    }
    
@routerU.post("/",status_code=status.HTTP_201_CREATED)
async def crea_usuario(usuarioP:crear_usuario, db:Session= Depends(get_db)):
   
    usuarioNuevo= usuarioDB(nombre= usuarioP.nombre, edad= usuarioP.edad)
    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)
    
    return {
        "mensaje": "Usuario creado correctamente",
        "status":"200",
        "usuario": usuarioP
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