from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from uuid import UUID

from app.db.models import Visit, Appointment
from app.schemas.visit import VisitCreate, VisitUpdate
from app.utils.exceptions import NotFoundError, ValidationError


class VisitService:
    """Business logic for visit management."""
    
    @staticmethod
    async def create_visit(
        db: AsyncSession,
        visit_data: VisitCreate
    ) -> Visit:
        """Create a new visit record."""
        # Verify appointment exists and is completed
        result = await db.execute(
            select(Appointment).where(
                Appointment.appointment_id == visit_data.appointment_id
            )
        )
        appointment = result.scalar_one_or_none()
        
        if not appointment:
            raise NotFoundError("Appointment not found")
        
        if appointment.status != 'completed':
            raise ValidationError("Can only create visits for completed appointments")
        
        # Check if visit already exists
        existing = await db.execute(
            select(Visit).where(Visit.appointment_id == visit_data.appointment_id)
        )
        if existing.scalar_one_or_none():
            raise ValidationError("Visit record already exists for this appointment")
        
        visit = Visit(
            appointment_id=visit_data.appointment_id,
            patient_id=appointment.patient_id,
            provider_id=appointment.provider_id,
            visit_date=appointment.appointment_date,
            **visit_data.model_dump(exclude={'appointment_id'})
        )
        
        db.add(visit)
        await db.commit()
        await db.refresh(visit)
        return visit
    
    @staticmethod
    async def get_visit(
        db: AsyncSession,
        visit_id: UUID
    ) -> Optional[Visit]:
        """Get visit by ID."""
        result = await db.execute(
            select(Visit).where(Visit.visit_id == visit_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def list_visits(
        db: AsyncSession,
        patient_id: Optional[UUID] = None,
        provider_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Visit]:
        """List visits with filters."""
        query = select(Visit)
        
        if patient_id:
            query = query.where(Visit.patient_id == patient_id)
        
        if provider_id:
            query = query.where(Visit.provider_id == provider_id)
        
        query = query.order_by(Visit.visit_date.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def update_visit(
        db: AsyncSession,
        visit_id: UUID,
        visit_data: VisitUpdate
    ) -> Visit:
        """Update visit record."""
        visit = await VisitService.get_visit(db, visit_id)
        
        if not visit:
            raise NotFoundError("Visit not found")
        
        update_data = visit_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(visit, field, value)
        
        await db.commit()
        await db.refresh(visit)
        return visit
    
    
