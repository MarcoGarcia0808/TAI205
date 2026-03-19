import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import status, HTTPException, Depends


##Seguridad HTTP Basic
security = HTTPBasic()

def verificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):
    userAuth = secrets.compare_digest(credentials.username, "Marco")
    passAuth = secrets.compare_digest(credentials.password, "12345")

    if not(userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    return credentials.username
