from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, text, func
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from datetime import date, time, datetime, timedelta
from uuid import UUID

from app.db.models import Appointment, Patient, Provider, ProviderSchedule, Visit
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentStatus,
    AppointmentResponse,
    AppointmentDetailResponse
)
from app.utils.exceptions import (
    AppointmentConflictError,
    ProviderUnavailableError,
    NotFoundError,
    ValidationError,
    InvalidTransitionError
)


# State machine for appointment status transitions
ALLOWED_TRANSITIONS = {
    'scheduled': ['confirmed', 'cancelled'],
    'confirmed': ['checked_in', 'cancelled', 'no_show'],
    'checked_in': ['in_progress', 'cancelled'],
    'in_progress': ['completed'],
    'completed': [],
    'cancelled': [],
    'no_show': []
}


class AppointmentService:
    """Business logic for appointment management."""
    
    @staticmethod
    async def check_provider_schedule(
        db: AsyncSession,
        provider_id: UUID,
        appointment_date: date,
        start_time: time,
        end_time: time
    ) -> bool:
        """Check if provider has availability for the requested time."""
        day_of_week = appointment_date.weekday()
        # Adjust: Python's weekday() is 0=Monday, SQL uses 0=Sunday
        sql_day_of_week = (day_of_week + 1) % 7
        
        result = await db.execute(
            select(ProviderSchedule)
            .where(
                and_(
                    ProviderSchedule.provider_id == provider_id,
                    ProviderSchedule.day_of_week == sql_day_of_week,
                    ProviderSchedule.effective_from <= appointment_date,
                    or_(
                        ProviderSchedule.effective_until.is_(None),
                        ProviderSchedule.effective_until >= appointment_date
                    ),
                    ProviderSchedule.start_time <= start_time,
                    ProviderSchedule.end_time >= end_time
                )
            )
        )
        
        return result.scalar_one_or_none() is not None
    
    @staticmethod
    async def validate_appointment_time(
        appointment_date: date,
        start_time: time,
        end_time: time
    ):
        """Validate appointment timing constraints."""
        MIN_DURATION = timedelta(minutes=15)
        MAX_DURATION = timedelta(hours=2)
        MIN_ADVANCE = timedelta(hours=2)
        MAX_ADVANCE = timedelta(days=90)
        
        # Calculate duration
        start_dt = datetime.combine(appointment_date, start_time)
        end_dt = datetime.combine(appointment_date, end_time)
        duration = end_dt - start_dt
        
        if duration < MIN_DURATION:
            raise ValidationError("Appointment must be at least 15 minutes")
        
        if duration > MAX_DURATION:
            raise ValidationError("Appointment cannot exceed 2 hours")
        
        # Check advance booking window
        now = datetime.now()
        if start_dt < now + MIN_ADVANCE:
            raise ValidationError("Must book at least 2 hours in advance")
        
        if start_dt > now + MAX_ADVANCE:
            raise ValidationError("Cannot book more than 90 days ahead")
    
    @staticmethod
    async def book_appointment(
        db: AsyncSession,
        appointment_data: AppointmentCreate
    ) -> Appointment:
        """
        Book a new appointment with full validation and concurrency safety.
        """
        # Validate timing
        await AppointmentService.validate_appointment_time(
            appointment_data.appointment_date,
            appointment_data.start_time,
            appointment_data.end_time
        )
        
        # Check provider schedule
        has_schedule = await AppointmentService.check_provider_schedule(
            db,
            appointment_data.provider_id,
            appointment_data.appointment_date,
            appointment_data.start_time,
            appointment_data.end_time
        )
        
        if not has_schedule:
            raise ProviderUnavailableError(
                "Provider is not available at the requested time"
            )
        
        # Check for conflicts (belt-and-suspenders with DB constraint)
        conflict = await db.execute(
            select(Appointment)
            .where(
                and_(
                    Appointment.provider_id == appointment_data.provider_id,
                    Appointment.appointment_date == appointment_data.appointment_date,
                    Appointment.status.not_in(['cancelled', 'no_show']),
                    or_(
                        and_(
                            Appointment.start_time < appointment_data.end_time,
                            Appointment.end_time > appointment_data.start_time
                        )
                    )
                )
            )
        )
        
        if conflict.scalar_one_or_none():
            raise AppointmentConflictError("Time slot is already booked")
        
        # Create appointment
        appointment = Appointment(
            patient_id=appointment_data.patient_id,
            provider_id=appointment_data.provider_id,
            appointment_date=appointment_data.appointment_date,
            start_time=appointment_data.start_time,
            end_time=appointment_data.end_time,
            appointment_type=appointment_data.appointment_type.value,
            notes=appointment_data.notes,
            status='scheduled'
        )
        
        db.add(appointment)
        
        try:
            await db.commit()
            await db.refresh(appointment)
            return appointment
        except IntegrityError as e:
            await db.rollback()
            error_msg = str(e.orig)
            if "appointments_provider_id" in error_msg or "exclude" in error_msg.lower():
                raise AppointmentConflictError(
                    "Time slot was just booked by another user"
                )
            raise
    
    @staticmethod
    async def get_appointment(
        db: AsyncSession,
        appointment_id: UUID
    ) -> Optional[Appointment]:
        """Get appointment by ID."""
        result = await db.execute(
            select(Appointment).where(Appointment.appointment_id == appointment_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_appointment_with_details(
        db: AsyncSession,
        appointment_id: UUID
    ) -> Optional[dict]:
        """Get appointment with patient and provider details."""
        query = text("""
            SELECT 
                a.*,
                p.first_name || ' ' || p.last_name AS patient_name,
                pr.first_name || ' ' || pr.last_name AS provider_name,
                pr.specialty AS provider_specialty
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN providers pr ON a.provider_id = pr.provider_id
            WHERE a.appointment_id = :appointment_id
        """)
        
        result = await db.execute(query, {"appointment_id": str(appointment_id)})
        row = result.mappings().one_or_none()
        
        return dict(row) if row else None
    
    @staticmethod
    async def list_appointments(
        db: AsyncSession,
        patient_id: Optional[UUID] = None,
        provider_id: Optional[UUID] = None,
        appointment_date: Optional[date] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[dict]:
        """List appointments with filters."""
        query = text("""
            SELECT 
                a.*,
                p.first_name || ' ' || p.last_name AS patient_name,
                pr.first_name || ' ' || pr.last_name AS provider_name,
                pr.specialty AS provider_specialty
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN providers pr ON a.provider_id = pr.provider_id
            WHERE 1=1
            {patient_filter}
            {provider_filter}
            {date_filter}
            {status_filter}
            ORDER BY a.appointment_date DESC, a.start_time DESC
            LIMIT :limit OFFSET :skip
        """)
        
        filters = {
            'patient_filter': f"AND a.patient_id = :patient_id" if patient_id else "",
            'provider_filter': f"AND a.provider_id = :provider_id" if provider_id else "",
            'date_filter': f"AND a.appointment_date = :appointment_date" if appointment_date else "",
            'status_filter': f"AND a.status = :status" if status else ""
        }
        
        query_str = query.text.format(**filters)
        
        params = {'skip': skip, 'limit': limit}
        if patient_id:
            params['patient_id'] = str(patient_id)
        if provider_id:
            params['provider_id'] = str(provider_id)
        if appointment_date:
            params['appointment_date'] = appointment_date
        if status:
            params['status'] = status
        
        result = await db.execute(text(query_str), params)
        rows = result.mappings().all()
        
        return [dict(row) for row in rows]
    
    @staticmethod
    async def update_appointment_status(
        db: AsyncSession,
        appointment_id: UUID,
        new_status: AppointmentStatus,
        cancellation_reason: Optional[str] = None
    ) -> Appointment:
        """Update appointment status with validation."""
        # Get appointment with lock
        result = await db.execute(
            select(Appointment)
            .where(Appointment.appointment_id == appointment_id)
            .with_for_update()
        )
        appointment = result.scalar_one_or_none()
        
        if not appointment:
            raise NotFoundError("Appointment not found")
        
        # Validate transition
        if new_status.value not in ALLOWED_TRANSITIONS.get(appointment.status, []):
            raise InvalidTransitionError(
                f"Cannot transition from {appointment.status} to {new_status.value}"
            )
        
        # Validate cancellation reason
        if new_status == AppointmentStatus.CANCELLED and not cancellation_reason:
            raise ValidationError("Cancellation reason is required")
        
        # Update status
        appointment.status = new_status.value
        if cancellation_reason:
            appointment.cancellation_reason = cancellation_reason
        
        # Auto-create visit if completed
        if new_status == AppointmentStatus.COMPLETED:
            existing_visit = await db.execute(
                select(Visit).where(Visit.appointment_id == appointment_id)
            )
            if not existing_visit.scalar_one_or_none():
                visit = Visit(
                    appointment_id=appointment_id,
                    patient_id=appointment.patient_id,
                    provider_id=appointment.provider_id,
                    visit_date=appointment.appointment_date
                )
                db.add(visit)
        
        await db.commit()
        await db.refresh(appointment)
        return appointment
    
    @staticmethod
    async def update_appointment(
        db: AsyncSession,
        appointment_id: UUID,
        update_data: AppointmentUpdate
    ) -> Appointment:
        """Update appointment details (reschedule, update notes, etc)."""
        appointment = await AppointmentService.get_appointment(db, appointment_id)
        
        if not appointment:
            raise NotFoundError("Appointment not found")
        
        # If rescheduling, validate new time
        if any([update_data.appointment_date, update_data.start_time, update_data.end_time]):
            new_date = update_data.appointment_date or appointment.appointment_date
            new_start = update_data.start_time or appointment.start_time
            new_end = update_data.end_time or appointment.end_time
            
            await AppointmentService.validate_appointment_time(new_date, new_start, new_end)
            
            # Check provider availability
            has_schedule = await AppointmentService.check_provider_schedule(
                db, appointment.provider_id, new_date, new_start, new_end
            )
            if not has_schedule:
                raise ProviderUnavailableError("Provider not available at new time")
            
            appointment.appointment_date = new_date
            appointment.start_time = new_start
            appointment.end_time = new_end
        
        # Update other fields
        if update_data.notes is not None:
            appointment.notes = update_data.notes
        
        if update_data.status:
            return await AppointmentService.update_appointment_status(
                db, appointment_id, update_data.status, update_data.cancellation_reason
            )
        
        await db.commit()
        await db.refresh(appointment)
        return appointment
    
    @staticmethod
    async def cancel_appointment(
        db: AsyncSession,
        appointment_id: UUID,
        reason: str
    ) -> Appointment:
        """Cancel an appointment."""
        return await AppointmentService.update_appointment_status(
            db, appointment_id, AppointmentStatus.CANCELLED, reason
        )
    
    @staticmethod
    async def get_available_slots(
        db: AsyncSession,
        provider_id: UUID,
        date: date,
        slot_duration: int = 30
    ) -> List[dict]:
        """Get available time slots for a provider on a specific date."""
        query = text("""
            SELECT * FROM get_available_slots(
                :provider_id::uuid,
                :date::date,
                :duration::interval
            )
        """)
        
        result = await db.execute(
            query,
            {
                "provider_id": str(provider_id),
                "date": date,
                "duration": f"{slot_duration} minutes"
            }
        )
        
        slots = result.mappings().all()
        return [{"start_time": str(slot['start_time']), "end_time": str(slot['end_time'])} for slot in slots]
