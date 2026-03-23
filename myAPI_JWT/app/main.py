#1. importaciones
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
import asyncio
from pydantic import BaseModel, Field 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta


#2. Inicialización de la aplicación
app = FastAPI(title="Mi primer API JWT", 
              description="Marco Antonio Resendiz Garcia",
              version="2.0.0"
              )

#BD ficticia

usuarios=[
    {"id":1, "nombre":"Marco", "edad":"21"},
    {"id":2, "nombre":"Ana", "edad":"22"},
    {"id":3, "nombre":"Luis", "edad":"23"},
]


SECRET_KEY = "mi_clave_super_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
 

def crear_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def validar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")

        if usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return usuario

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

class crear_usuario(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juanita")
    edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")
    
#3. endpoints de la API
@app.get("/", tags=['inicio'])
async def holaMundo():
    return {"message": 'Hola Mundo desde FastAPI'}

@app.get("/v1/bienvenidos", tags=['inicio'])
async def bien():
    return {"message": "bienvenidos a mi API con JWT"}

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
async def consultaT():
    return{
        
        "status":"200",
        "total": len(usuarios),
        "data": usuarios
        
    }
    
    
@app.get("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def obtener_usuario(id: int):
    for usr in usuarios:
        if usr["id"] == id:
            return usr
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    
    
    
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "Marco2" or form_data.password != "12345":
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    token = crear_token({"sub": form_data.username})
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }
    
@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualiza_usuario(id: int, datos: dict, usuario: str = Depends(validar_token)):
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


@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def elimina_usuario(id: int, usuario: str = Depends(validar_token)):

    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            eliminado = usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado por {usuario}",
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )
    
@app.post("/v1/usuarios/", tags=["CRUD HTTP"], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="El id ya existe")

    usuarios.append(usuario.dict())

    return {
        "mensaje": "Usuario creado correctamente",
        "usuario": usuario
    }