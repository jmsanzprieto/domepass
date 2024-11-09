from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils import load_services, save_services, hash_password, get_next_service_id

router = APIRouter()

class Service(BaseModel):
    nombre_servicio: str
    pass_servicio: str
    id_usuario: int

class ServiceUpdate(BaseModel):
    nombre_servicio: str = None
    pass_servicio: str = None

# Ruta para crear un nuevo servicio
@router.post("/servicios")
async def create_service(service: Service):
    """Crea un nuevo servicio para un usuario con su contraseña hasheada."""
    services = load_services()

    # Generar el ID del servicio
    service_id = get_next_service_id(services)

    # Hashear la contraseña del servicio
    hashed_pass_servicio = hash_password(service.pass_servicio)

    # Crear el servicio
    new_service = {
        "id_servicio": service_id,
        "id_usuario": service.id_usuario,
        "nombre_servicio": service.nombre_servicio,
        "pass_servicio": hashed_pass_servicio
    }

    # Guardar el nuevo servicio
    services.append(new_service)
    save_services(services)

    return {"message": "Servicio creado exitosamente", "id_servicio": service_id}


# Ruta para obtener todos los servicios de un usuario
@router.get("/servicios/{id_usuario}")
async def get_services(id_usuario: int):
    """Obtiene todos los servicios de un usuario especificado por id_usuario."""
    services = load_services()

    user_services = [service for service in services if service["id_usuario"] == id_usuario]

    if not user_services:
        raise HTTPException(status_code=404, detail="No se encontraron servicios para este usuario.")

    return user_services

# Ruta para obtener un servicio por su ID, solo si el usuario es el creador
@router.get("/servicios/{id_servicio}/{id_usuario}")
async def get_service(id_servicio: int, id_usuario: int):
    """Obtiene un servicio específico de un usuario por id_servicio."""
    services = load_services()

    # Buscar el servicio
    service = next((s for s in services if s["id_servicio"] == id_servicio and s["id_usuario"] == id_usuario), None)

    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado o no pertenece a este usuario.")

    return service

# Ruta para actualizar un servicio
@router.put("/servicios/{id_servicio}/{id_usuario}")
async def update_service(id_servicio: int, id_usuario: int, service_update: ServiceUpdate):
    """Actualiza un servicio específico de un usuario por id_servicio."""
    services = load_services()

    # Buscar el servicio
    service = next((s for s in services if s["id_servicio"] == id_servicio and s["id_usuario"] == id_usuario), None)

    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado o no pertenece a este usuario.")

    # Actualizar los datos
    if service_update.nombre_servicio:
        service["nombre_servicio"] = service_update.nombre_servicio
    if service_update.pass_servicio:
        service["pass_servicio"] = hash_password(service_update.pass_servicio)

    # Guardar los cambios
    save_services(services)

    return {"message": "Servicio actualizado exitosamente", "service": service}

# Ruta para eliminar un servicio
@router.delete("/servicios/{id_servicio}/{id_usuario}")
async def delete_service(id_servicio: int, id_usuario: int):
    """Elimina un servicio específico de un usuario por id_servicio."""
    services = load_services()

    # Buscar el servicio
    service = next((s for s in services if s["id_servicio"] == id_servicio and s["id_usuario"] == id_usuario), None)

    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado o no pertenece a este usuario.")

    # Eliminar el servicio
    services = [s for s in services if s["id_servicio"] != id_servicio]

    # Guardar los cambios
    save_services(services)

    return {"message": "Servicio eliminado exitosamente", "service": service}
