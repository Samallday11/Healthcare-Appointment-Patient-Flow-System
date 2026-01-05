from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.db.session import get_db
from app.core.patient_service import PatientService
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from app.utils.exceptions import NotFoundError

router = APIRouter()


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient: PatientCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new patient.
    
    - **first_name**: Patient's first name
    - **last_name**: Patient's last name
    - **date_of_birth**: Date of birth (YYYY-MM-DD)
    - **email**: Email address (optional)
    - **phone**: Phone number
    - **insurance_id**: Insurance policy number (optional)
    """
    return await PatientService.create_patient(db, patient)


@router.get("/", response_model=List[PatientResponse])
async def list_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None, description="Search by name, email, or phone"),
    db: AsyncSession = Depends(get_db)
):
    """
    List all patients with optional search and pagination.
    """
    return await PatientService.list_patients(db, skip, limit, search)


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific patient by ID.
    """
    patient = await PatientService.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    return patient


@router.patch("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: UUID,
    patient_update: PatientUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update patient information.
    """
    try:
        return await PatientService.update_patient(db, patient_id, patient_update)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
    patient_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a patient (use with caution in production).
    """
    try:
        await PatientService.delete_patient(db, patient_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    
