# main.py
from fastapi import FastAPI
from auth import router as auth_router  # Importamos las rutas de auth
from crud_user import router as crud_user_router  # Importamos las rutas de crud_user

app = FastAPI()

# Incluir las rutas de auth
app.include_router(auth_router)

# Incluir las rutas de CRUD de usuarios
app.include_router(crud_user_router)