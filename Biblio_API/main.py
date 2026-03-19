from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import Literal
from datetime import datetime




app = FastAPI(title="API Biblioteca Digital")

libros = []
prestamos = []


##seguridad HTTP Basic

class Libro(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    autor: str
    año: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1)
    estado: Literal["disponible", "prestado"] = "disponible"

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2)
    correo: EmailStr

class Prestamo(BaseModel):
    nombre_libro: str
    usuario: Usuario



@app.post("/libros", status_code=201)
async def registrar_libro(libro: Libro):

    for l in libros:
        if l["nombre"].lower() == libro.nombre.lower():
            raise HTTPException(status_code=400, detail="request")

    libros.append(libro.dict())
    return {"mensaje": "Create"}


@app.get("/libros")
async def listar_libros():
    return [l for l in libros if l["estado"] == "disponible"]



@app.get("/libros/{nombre}")
async def buscar_libro(nombre: str):

    for libro in libros:
        if libro["nombre"].lower() == nombre.lower():
            return libro

    raise HTTPException(status_code=400, detail="Request")



@app.post("/prestamos")
async def registrar_prestamo(prestamo: Prestamo):

    for libro in libros:
        if libro["nombre"].lower() == prestamo.nombre_libro.lower():

            if libro["estado"] == "prestado":
                raise HTTPException(
                    status_code=409,
                    detail="Conflict"
                )

            libro["estado"] = "prestado"
            prestamos.append(prestamo.dict())
            return {"mensaje": "Conflict"}


    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.put("/devolver/{nombre}", status_code=200)
async def devolver_libro(nombre: str):

    for libro in libros:
        if libro["nombre"].lower() == nombre.lower():
            libro["estado"] = "disponible"
            return {"mensaje": "OK"}

    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.delete("/prestamos/{nombre}")
async def eliminar_prestamo(nombre: str):

    for i, prestamo in enumerate(prestamos):
        if prestamo["nombre_libro"].lower() == nombre.lower():
            prestamos.pop(i)
            return {"mensaje": "Registro eliminado"}

    raise HTTPException(
        status_code=409,
        detail="El libro no existe, haz que elija otro"
    )