# domepass

# FastAPI User Management API

Esta es una API construida con FastAPI que permite registrar, autenticar y gestionar usuarios. Ofrece funcionalidad para registrar un nuevo usuario, iniciar sesión, obtener la lista de usuarios, actualizar usuarios y eliminar usuarios. Todo ello con seguridad basada en JWT (JSON Web Tokens).

## Requisitos

- Python 3.8 o superior
- FastAPI
- Uvicorn (para ejecutar el servidor)
- Pydantic
- Bcrypt
- JWT

## Instalación

1. Clona el repositorio en tu máquina local:

   ```bash
   git clone https://github.com/tu-usuario/fastapi-user-management.git
   cd fastapi-user-management
   ```

2. Crea un entorno virtual y activa el entorno:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/macOS
   venv\Scripts\activate     # En Windows
   ```

3. Instala las dependencias del proyecto:

   ```bash
   pip install -r requirements.txt
   ```

## Endpoints

### 1. Registro de Usuario

- **URL**: `/registro`
- **Método**: `POST`
- **Descripción**: Registra un nuevo usuario con su nombre de usuario, correo electrónico y contraseña.
- **Cuerpo**:
  ```json
  {
    "username": "nuevo_usuario",
    "email": "usuario@ejemplo.com",
    "password": "contraseña_segura"
  }
  ```

- **Respuesta**:
  ```json
  {
    "message": "Usuario registrado exitosamente",
    "user_id": 1,
    "unique_id": "uuid-generado"
  }
  ```

### 2. Login de Usuario

- **URL**: `/login`
- **Método**: `POST`
- **Descripción**: Inicia sesión con el nombre de usuario y la contraseña.
- **Cuerpo**:
  ```json
  {
    "username": "usuario",
    "password": "contraseña_segura"
  }
  ```

- **Respuesta**:
  ```json
  {
    "access_token": "jwt-token-aqui",
    "token_type": "bearer"
  }
  ```

### 3. Obtener Lista de Usuarios

- **URL**: `/usuarios`
- **Método**: `GET`
- **Descripción**: Devuelve la lista de todos los usuarios registrados. Solo accesible con un token válido.
- **Headers**:
  ```plaintext
  Authorization: Bearer <jwt-token>
  ```

- **Respuesta**:
  ```json
  [
    {
      "id": 1,
      "unique_id": "uuid-1",
      "username": "usuario1",
      "email": "usuario1@ejemplo.com"
    },
    {
      "id": 2,
      "unique_id": "uuid-2",
      "username": "usuario2",
      "email": "usuario2@ejemplo.com"
    }
  ]
  ```

### 4. Obtener Usuario por ID

- **URL**: `/usuarios/{user_id}`
- **Método**: `GET`
- **Descripción**: Devuelve los datos de un usuario específico por su ID. Solo accesible con un token válido.
- **Headers**:
  ```plaintext
  Authorization: Bearer <jwt-token>
  ```

- **Respuesta**:
  ```json
  {
    "id": 1,
    "unique_id": "uuid-1",
    "username": "usuario1",
    "email": "usuario1@ejemplo.com"
  }
  ```

### 5. Actualizar Usuario

- **URL**: `/usuarios/{user_id}`
- **Método**: `PUT`
- **Descripción**: Actualiza los datos de un usuario existente. Solo accesible con un token válido.
- **Headers**:
  ```plaintext
  Authorization: Bearer <jwt-token>
  ```

- **Cuerpo**:
  ```json
  {
    "username": "nuevo_nombre",
    "email": "nuevo_correo@ejemplo.com",
    "password": "nueva_contraseña"
  }
  ```

- **Respuesta**:
  ```json
  {
    "message": "Usuario actualizado exitosamente",
    "user": {
      "id": 1,
      "unique_id": "uuid-1",
      "username": "nuevo_nombre",
      "email": "nuevo_correo@ejemplo.com"
    }
  }
  ```

### 6. Eliminar Usuario

- **URL**: `/usuarios/{user_id}`
- **Método**: `DELETE`
- **Descripción**: Elimina un usuario por su ID. Solo accesible con un token válido.
- **Headers**:
  ```plaintext
  Authorization: Bearer <jwt-token>
  ```

- **Respuesta**:
  ```json
  {
    "message": "Usuario eliminado exitosamente",
    "user": {
      "id": 1,
      "unique_id": "uuid-1",
      "username": "usuario1",
      "email": "usuario1@ejemplo.com"
    }
  }
  ```

## Seguridad

- **JWT**: Todos los endpoints protegidos requieren un token JWT válido para acceder. El token se obtiene al iniciar sesión en la ruta `/login`.
  
## Archivos Importantes

- **auth.py**: Contiene las rutas para registro de usuario y login.
- **crud_user.py**: Contiene las rutas CRUD para gestionar usuarios.
- **utils.py**: Utilidades para manejo de contraseñas, JWT y gestión de usuarios (cargar, guardar, etc.).

## Ejecutar la API

Para iniciar el servidor, ejecuta:

```bash
uvicorn main:app --reload
```

Esto iniciará el servidor en `http://127.0.0.1:8000`.

## Pruebas

Puedes probar la API utilizando herramientas como [Postman](https://www.postman.com/) o [Swagger UI](http://127.0.0.1:8000/docs), que está habilitada por defecto con FastAPI.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un "issue" o un "pull request" con cualquier mejora o sugerencia.

---

¡Gracias por utilizar esta API! 🚀