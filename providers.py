from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.core.provider_service import ProviderService
from app.schemas.provider import (
    ProviderCreate,
    ProviderUpdate,
    ProviderResponse,
    ProviderScheduleCreate,
    ProviderScheduleResponse
)
from app.utils.exceptions import NotFoundError

router = APIRouter()


@router.post("/", response_model=ProviderResponse, status_code=status.HTTP_201_CREATED)
async def create_provider(
    provider: ProviderCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new provider.
    
    - **first_name**: Provider's first name
    - **last_name**: Provider's last name
    - **specialty**: Medical specialty
    - **license_number**: Medical license number (unique)
    - **email**: Email address
    - **phone**: Phone number
    """
    return await ProviderService.create_provider(db, provider)


@router.get("/", response_model=List[ProviderResponse])
async def list_providers(
    specialty: Optional[str] = Query(None, description="Filter by specialty"),
    is_active: Optional[bool] = Query(True, description="Filter by active status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """
    List all providers with optional filters.
    """
    return await ProviderService.list_providers(db, specialty, is_active, skip, limit)


@router.get("/{provider_id}", response_model=ProviderResponse)
async def get_provider(
    provider_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific provider by ID.
    """
    provider = await ProviderService.get_provider(db, provider_id)
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider not found"
        )
    return provider


@router.patch("/{provider_id}", response_model=ProviderResponse)
async def update_provider(
    provider_id: UUID,
    provider_update: ProviderUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update provider information.
    """
    try:
        return await ProviderService.update_provider(db, provider_id, provider_update)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{provider_id}/schedules", response_model=ProviderScheduleResponse, status_code=status.HTTP_201_CREATED)
async def add_provider_schedule(
    provider_id: UUID,
    schedule: ProviderScheduleCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Add availability schedule for a provider.
    
    - **day_of_week**: 0=Sunday, 1=Monday, ..., 6=Saturday
    - **start_time**: Schedule start time
    - **end_time**: Schedule end time
    - **effective_from**: Date schedule becomes effective
    - **effective_until**: Date schedule ends (optional, null = indefinite)
    """
    if schedule.provider_id != provider_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provider ID in URL must match provider ID in request body"
        )
    
    try:
        return await ProviderService.add_schedule(db, schedule)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{provider_id}/schedules", response_model=List[ProviderScheduleResponse])
async def get_provider_schedules(
    provider_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all schedules for a provider.
    """
    return await ProviderService.get_provider_schedules(db, provider_id)

