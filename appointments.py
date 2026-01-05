from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from datetime import date

from app.db.session import get_db
from app.core.appointment_service import AppointmentService
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
    AppointmentDetailResponse,
    AppointmentStatus
)
from app.utils.exceptions import (
    AppointmentConflictError,
    ProviderUnavailableError,
    NotFoundError,
    ValidationError,
    InvalidTransitionError
)

router = APIRouter()


@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def book_appointment(
    appointment: AppointmentCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Book a new appointment.
    
    This endpoint implements:
    - Double-booking prevention via database constraints
    - Provider availability validation
    - Appointment time validation (min 15 min, max 2 hours)
    - Advance booking rules (2 hours minimum, 90 days maximum)
    
    Returns 409 Conflict if time slot is unavailable.
    """
    try:
        return await AppointmentService.book_appointment(db, appointment)
    except (AppointmentConflictError, ProviderUnavailableError, ValidationError) as e:
        raise HTTPException(status_code=e.status_code, detail={
            "error": e.error_code,
            "message": e.message
        })


@router.get("/", response_model=List[AppointmentDetailResponse])
async def list_appointments(
    patient_id: Optional[UUID] = Query(None, description="Filter by patient"),
    provider_id: Optional[UUID] = Query(None, description="Filter by provider"),
    appointment_date: Optional[date] = Query(None, description="Filter by date"),
    status: Optional[AppointmentStatus] = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """
    List appointments with optional filters.
    """
    status_value = status.value if status else None
    appointments = await AppointmentService.list_appointments(
        db, patient_id, provider_id, appointment_date, status_value, skip, limit
    )
    return [AppointmentDetailResponse(**apt) for apt in appointments]


@router.get("/{appointment_id}", response_model=AppointmentDetailResponse)
async def get_appointment(
    appointment_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific appointment by ID with full details.
    """
    appointment = await AppointmentService.get_appointment_with_details(db, appointment_id)
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    return AppointmentDetailResponse(**appointment)


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: UUID,
    appointment_update: AppointmentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an appointment (reschedule, change status, update notes).
    
    Status transitions are validated according to the state machine:
    - scheduled → confirmed, cancelled
    - confirmed → checked_in, cancelled, no_show
    - checked_in → in_progress, cancelled
    - in_progress → completed
    - completed/cancelled/no_show → (terminal states)
    """
    try:
        return await AppointmentService.update_appointment(db, appointment_id, appointment_update)
    except (NotFoundError, ValidationError, InvalidTransitionError, ProviderUnavailableError) as e:
        raise HTTPException(status_code=e.status_code, detail={
            "error": e.error_code,
            "message": e.message
        })


@router.post("/{appointment_id}/cancel", response_model=AppointmentResponse)
async def cancel_appointment(
    appointment_id: UUID,
    reason: str = Query(..., description="Cancellation reason"),
    db: AsyncSession = Depends(get_db)
):
    """
    Cancel an appointment.
    """
    try:
        return await AppointmentService.cancel_appointment(db, appointment_id, reason)
    except (NotFoundError, InvalidTransitionError) as e:
        raise HTTPException(status_code=e.status_code, detail={
            "error": e.error_code,
            "message": e.message
        })


@router.get("/providers/{provider_id}/available-slots")
async def get_available_slots(
    provider_id: UUID,
    date: date = Query(..., description="Date to check availability"),
    slot_duration: int = Query(30, ge=15, le=120, description="Slot duration in minutes"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get available time slots for a provider on a specific date.
    
    Returns list of available time slots based on:
    - Provider's schedule for that day
    - Existing appointments
    - Requested slot duration
    """
    slots = await AppointmentService.get_available_slots(db, provider_id, date, slot_duration)
    return {
        "provider_id": provider_id,
        "date": date,
        "slot_duration_minutes": slot_duration,
        "available_slots": slots
    }

