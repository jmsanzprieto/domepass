from fastapi import APIRouter, HTTPException, Depends, Header
from pathlib import Path
import json
import bcrypt
import jwt
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from utils import load_users,save_user_crud, get_user_by_id, verify_jwt_token


# USERS_FILE = Path("users.json")
# SECRET_KEY = "mi_secreto_jwt"  # Cambia esta clave a algo más seguro

router = APIRouter()



@router.get("/usuarios")
async def get_users(token: str = Depends(verify_jwt_token)):
    """Obtiene la lista de todos los usuarios, solo si el token es válido."""
    users = load_users()
    if not users:
        raise HTTPException(status_code=404, detail="No hay usuarios registrados.")
    return users

@router.get("/usuarios/{user_id}")
async def get_user(user_id: int, token: str = Depends(verify_jwt_token)):
    """Obtiene los datos de un usuario por su ID, solo si el token es válido."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return user

@router.put("/usuarios/{user_id}")
async def update_user(user_id: int, username: str = None, email: str = None, password: str = None, token: str = Depends(verify_jwt_token)):
    """Actualiza los datos de un usuario existente, solo si el token es válido."""
    users = load_users()
    user = get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    if username:
        user["username"] = username
    if email:
        user["email"] = email
    if password:
        user["password"] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    save_user_crud(users)
    return {"message": "Usuario actualizado exitosamente", "user": user}

@router.delete("/usuarios/{user_id}")
async def delete_user(user_id: int, token: str = Depends(verify_jwt_token)):
    """Elimina un usuario por su ID, solo si el token es válido."""
    users = load_users()
    user = get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    users = [u for u in users if u["id"] != user_id]
    save_user_crud(users)
    return {"message": "Usuario eliminado exitosamente", "user": user}
