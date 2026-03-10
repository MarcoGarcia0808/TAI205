from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
import asyncio
from pydantic import BaseModel, Field 
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets




##API para gestionar reservas de hotel

app = FastAPI(
    title="API Examen 2DO",
    description="Marco Antonio Resendiz Garcia",
    version="1.0"
)

security = HTTPBasic()


tipo_habitacion=('sencilla', 'doble','suite')

##validaciones para campos: huesped minimo 5 caracteres, fecha de entrada no menor a fecha actual, fecha de salida mayor que fecha de entrada, estancia

class Reserva(BaseModel):
    id: int
    huesped: str = Field(..., min_length=5)
    tipo_habitacion: str = Field(..., regex="^(sencilla|doble|suite)$") 
    
    
class FechaSalida(BaseModel):
    dia: int = Field(..., gt=0, lt=32)
    mes: int = Field(..., gt=0, lt=13)
    año: int = Field(..., gt=2026)
    
    

    
class FechaEntrada(BaseModel):
    dia: int = Field(..., gt=0, lt=32)
    mes: int = Field(..., gt=0, lt=13)
    año: int = Field(..., gt=2026)
    
    
    
class Huesped(BaseModel):
    nombre: str = Field(..., min_length=5)
    apellido: str = Field(..., min_length=5)
    
class estancia(BaseModel):
    dias: int = Field(..., gt=0, lt=8)











##endpoint crear reserva protegido con usuario: hotel y contraseña: r2026 y que puedas elegir entre habitacion:sencilla, doble o suite, la estancia no debe ser mayor a 7 días

@app.post("/reservas", status_code=status.HTTP_201_CREATED)
async def crear_reserva(reserva: dict, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "hotel")
    correct_password = secrets.compare_digest(credentials.password, "r2026")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return {"message": "Reserva creada exitosamente", "reserva": reserva}
    



##endpoint listar reserva



##endpoint Consultar reserva
@app.get()

##confirmar reserva

@app.()


##cancelar reserva debe estar protegido por usuario: hotel y contraseña: r2026
@app.post()
