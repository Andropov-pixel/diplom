from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.crud.server import (
    create_server,
    get_servers,
    get_server,
    update_server,
    delete_server
)
from app.schemas.server import Server, ServerCreate, ServerUpdate
from app.core.dependencies import get_current_user, get_current_superuser
from app.services.monitoring_service import monitor_server

router = APIRouter()


@router.get("/servers", response_model=List[Server])
async def list_servers(
        skip: int = 0,
        limit: int = 100,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if current_user.is_superuser:
        return await get_servers(db, skip=skip, limit=limit)
    return await get_servers(db, skip=skip, limit=limit, owner_id=current_user.id)


@router.post("/servers", response_model=Server)
async def create_new_server(
        server_in: ServerCreate,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    return await create_server(db, server_in, owner_id=current_user.id)


@router.get("/servers/{server_id}", response_model=Server)
async def get_server_by_id(
        server_id: int,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    server = await get_server(db, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    if not current_user.is_superuser and server.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return server


@router.put("/servers/{server_id}", response_model=Server)
async def update_server_by_id(
        server_id: int,
        server_in: ServerUpdate,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    server = await get_server(db, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    if not current_user.is_superuser and server.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return await update_server(db, server, server_in)


@router.delete("/servers/{server_id}")
async def delete_server_by_id(
        server_id: int,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    server = await get_server(db, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    if not current_user.is_superuser and server.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    await delete_server(db, server)
    return {"message": "Server deleted successfully"}


@router.post("/servers/{server_id}/monitor")
async def start_monitoring(
        server_id: int,
        background_tasks: BackgroundTasks,
        current_user=Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    server = await get_server(db, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    if not current_user.is_superuser and server.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    background_tasks.add_task(monitor_server, db, server, current_user)
    return {"message": "Monitoring started"}