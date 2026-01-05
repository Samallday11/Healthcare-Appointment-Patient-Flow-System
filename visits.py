from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.core.visit_service import VisitService
from app.schemas.visit import VisitCreate, VisitUpdate, VisitResponse
from app.utils.exceptions import NotFoundError, ValidationError

router = APIRouter()


@router.post("/", response_model=VisitResponse, status_code=status.HTTP_201_CREATED)
async def create_visit(
    visit: VisitCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a visit record after appointment completion.
    
    - **appointment_id**: ID of completed appointment
    - **chief_complaint**: Patient's primary concern
    - **diagnosis**: Medical diagnosis
    - **treatment_plan**: Recommended treatment
    - **prescriptions**: Medications prescribed (JSON)
    - **follow_up_required**: Whether follow-up is needed
    - **follow_up_date**: Date for follow-up (if required)
    """
    try:
        return await VisitService.create_visit(db, visit)
    except (NotFoundError, ValidationError) as e:
        raise HTTPException(status_code=e.status_code, detail={
            "error": e.error_code,
            "message": e.message
        })


@router.get("/", response_model=List[VisitResponse])
async def list_visits(
    patient_id: Optional[UUID] = Query(None, description="Filter by patient"),
    provider_id: Optional[UUID] = Query(None, description="Filter by provider"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """
    List visit records with optional filters.
    """
    return await VisitService.list_visits(db, patient_id, provider_id, skip, limit)


@router.get("/{visit_id}", response_model=VisitResponse)
async def get_visit(
    visit_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific visit record by ID.
    """
    visit = await VisitService.get_visit(db, visit_id)
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit not found"
        )
    return visit


@router.patch("/{visit_id}", response_model=VisitResponse)
async def update_visit(
    visit_id: UUID,
    visit_update: VisitUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update visit record (add notes, diagnosis, prescriptions, etc).
    """
    try:
        return await VisitService.update_visit(db, visit_id, visit_update)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail={
            "error": e.error_code,
            "message": e.message
        })
    
    
