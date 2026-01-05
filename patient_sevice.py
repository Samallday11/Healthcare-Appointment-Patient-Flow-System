from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from uuid import UUID

from app.db.models import Patient
from app.schemas.patient import PatientCreate, PatientUpdate
from app.utils.exceptions import NotFoundError


class PatientService:
    """Business logic for patient management."""
    
    @staticmethod
    async def create_patient(
        db: AsyncSession,
        patient_data: PatientCreate
    ) -> Patient:
        """Create a new patient."""
        patient = Patient(**patient_data.model_dump())
        db.add(patient)
        await db.commit()
        await db.refresh(patient)
        return patient
    
    @staticmethod
    async def get_patient(
        db: AsyncSession,
        patient_id: UUID
    ) -> Optional[Patient]:
        """Get patient by ID."""
        result = await db.execute(
            select(Patient).where(Patient.patient_id == patient_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def list_patients(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> List[Patient]:
        """List patients with optional search."""
        query = select(Patient)
        
        if search:
            search_filter = f"%{search}%"
            query = query.where(
                (Patient.first_name.ilike(search_filter)) |
                (Patient.last_name.ilike(search_filter)) |
                (Patient.email.ilike(search_filter)) |
                (Patient.phone.ilike(search_filter))
            )
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def update_patient(
        db: AsyncSession,
        patient_id: UUID,
        patient_data: PatientUpdate
    ) -> Patient:
        """Update patient information."""
        patient = await PatientService.get_patient(db, patient_id)
        
        if not patient:
            raise NotFoundError("Patient not found")
        
        # Update only provided fields
        update_data = patient_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(patient, field, value)
        
        await db.commit()
        await db.refresh(patient)
        return patient
    
    @staticmethod
    async def delete_patient(
        db: AsyncSession,
        patient_id: UUID
    ) -> bool:
        """Delete a patient (soft delete recommended in production)."""
        patient = await PatientService.get_patient(db, patient_id)
        
        if not patient:
            raise NotFoundError("Patient not found")
        
        await db.delete(patient)
        await db.commit()
        return True
    
    
