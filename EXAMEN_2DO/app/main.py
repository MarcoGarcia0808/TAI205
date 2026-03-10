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

reservas = []

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
    



##endpoint listar reserva con opcion de filtrar por tipo de habitacion y fecha de entrada
@app.get("/reservas")
async def listar_reservas(tipo_habitacion: Optional[str] = None, fecha_entrada: Optional[str] = None):

    
    if tipo_habitacion:
        reservas = [reserva for reserva in reservas if reserva["tipo_habitacion"] == tipo_habitacion]
    
    if fecha_entrada:
        reservas = [reserva for reserva in reservas if reserva["fecha_entrada"] == fecha_entrada]
    
    return {"reservas": reservas}



##endpoint Consultar reserva
@app.get("/reservas/{reserva_id}")
async def consultar_reserva(reserva_id: int):   
    reservas = []
    
    reserva = next((reserva for reserva in reservas if reserva["id"] == reserva_id), None)
    
    if reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    return {"reserva": reserva}

##endpoint para confirmar reserva, debe estar protegido por usuario: hotel y contraseña: r2026
@app.post("/reservas/{reserva_id}/confirmar")
async def confirmar_reserva(reserva_id: int, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "hotel")
    correct_password = secrets.compare_digest(credentials.password, "r2026")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return {"message": f"Reserva {reserva_id} confirmada exitosamente"}

##cancelar reserva debe estar protegido por usuario: hotel y contraseña: r2026
@app.delete("/reservas/{reserva_id}")
async def cancelar_reserva(reserva_id: int, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "hotel")
    correct_password = secrets.compare_digest(credentials.password, "r2026")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return {"message": f"Reserva {reserva_id} cancelada exitosamente"}

