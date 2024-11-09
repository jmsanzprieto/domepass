import json
from fastapi import APIRouter, HTTPException, Depends, Header
from datetime import datetime, timedelta
import bcrypt
import jwt
from pathlib import Path
from fastapi.security import OAuth2PasswordBearer

USERS_FILE = Path("users.json")
SECRET_KEY = "mi_secreto_jwt"  # Cambia esta clave a algo más seguro
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def save_user(user_data):
    """Guarda un nuevo usuario en el archivo JSON."""
    users = load_users()
    users.append(user_data)
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)

def load_users():
    """Carga la lista de usuarios desde el archivo JSON."""
    if USERS_FILE.is_file():
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    return []

def get_next_id(users):
    """Obtiene el siguiente ID disponible para un nuevo usuario."""
    if users:
        last_id = max(user["id"] for user in users)
        return last_id + 1
    return 1

def create_jwt_token(unique_id, email):
    """Genera un JWT con unique_id y email, válido por 1 hora."""
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {
        "unique_id": unique_id,
        "email": email,
        "exp": expiration
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def hash_password(password: str):
    """Hashea la contraseña utilizando bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(stored_password: str, password: str) -> bool:
    """Verifica si la contraseña proporcionada coincide con la almacenada."""
    return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))



def save_user_crud(users):
    """Guarda la lista de usuarios en el archivo JSON."""
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)

def get_user_by_id(user_id: int):
    """Busca un usuario por ID."""
    users = load_users()
    return next((u for u in users if u["id"] == user_id), None)

def verify_jwt_token(token: str = Depends(oauth2_scheme)):
    """Verifica el JWT y extrae los datos del usuario."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload  # Retorna el payload que contiene los datos del usuario
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido.")
