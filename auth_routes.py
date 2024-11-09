from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils import save_user, load_users, get_next_id, create_jwt_token
import bcrypt
import uuid

# Crear un router para autenticación
router = APIRouter()

class User(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/registro")
async def register(user: User):
    """Ruta para registrar un nuevo usuario con la contraseña hasheada y comprobación de correo."""
    users = load_users()

    # Verifica si el correo ya existe
    if any(u["email"] == user.email for u in users):
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")

    # Hashear la contraseña
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Genera un ID único y un unique_id para el usuario
    user_id = get_next_id(users)
    unique_id = str(uuid.uuid4())

    # Guarda el usuario con los datos adicionales
    user_data = {
        "id": user_id,
        "unique_id": unique_id,
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    }
    save_user(user_data)

    return {"message": "Usuario registrado exitosamente", "user_id": user_id, "unique_id": unique_id}

@router.post("/login")
async def login(user_login: UserLogin):
    users = load_users()

    # Busca el usuario por nombre
    user = next((u for u in users if u["username"] == user_login.username), None)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos.")

    # Verifica la contraseña
    if not bcrypt.checkpw(user_login.password.encode('utf-8'), user["password"].encode('utf-8')):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos.")

    # Genera el JWT con unique_id y email
    token = create_jwt_token(user["unique_id"], user["email"])
    return {"access_token": token, "token_type": "bearer"}
