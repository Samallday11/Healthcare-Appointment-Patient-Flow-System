from sqlalchemy import (
    Column, String, Date, Time, Boolean, Text, Integer,
    ForeignKey, CheckConstraint, Index, TIMESTAMP, text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base import Base


class Patient(Base):
    __tablename__ = "patients"
    
    patient_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    phone = Column(String(20), nullable=False)
    address = Column(Text, nullable=True)
    insurance_id = Column(String(50), nullable=True)
    emergency_contact_name = Column(String(200), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), onupdate=datetime.now)
    
    # Relationships
    appointments = relationship("Appointment", back_populates="patient")
    visits = relationship("Visit", back_populates="patient")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("date_of_birth < CURRENT_DATE", name="valid_dob"),
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
            name="valid_email"
        ),
        Index("idx_patients_email", "email"),
        Index("idx_patients_phone", "phone"),
        Index("idx_patients_last_name", "last_name"),
    )


class Provider(Base):
    __tablename__ = "providers"
    
    provider_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    specialty = Column(String(100), nullable=False)
    license_number = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), onupdate=datetime.now)
    
    # Relationships
    schedules = relationship("ProviderSchedule", back_populates="provider")
    appointments = relationship("Appointment", back_populates="provider")
    visits = relationship("Visit", back_populates="provider")
    
    # Constraints
    __table_args__ = (
        Index("idx_providers_specialty", "specialty"),
        Index("idx_providers_active", "is_active"),
    )


class ProviderSchedule(Base):
    __tablename__ = "provider_schedules"
    
    schedule_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.provider_id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0=Sunday, 6=Saturday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    effective_from = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    effective_until = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    
    # Relationships
    provider = relationship("Provider", back_populates="schedules")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("day_of_week BETWEEN 0 AND 6", name="valid_day"),
        CheckConstraint("end_time > start_time", name="valid_time_range"),
        CheckConstraint(
            "effective_until IS NULL OR effective_until >= effective_from",
            name="valid_date_range"
        ),
        Index("idx_provider_schedules_provider", "provider_id"),
        Index("idx_provider_schedules_day", "day_of_week"),
        Index("idx_provider_schedules_provider_day", "provider_id", "day_of_week"),
    )


class Appointment(Base):
    __tablename__ = "appointments"
    
    appointment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.provider_id"), nullable=False)
    appointment_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(String(20), nullable=False, default="scheduled")
    appointment_type = Column(String(50), default="routine")
    notes = Column(Text, nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), onupdate=datetime.now)
    
    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    provider = relationship("Provider", back_populates="appointments")
    visit = relationship("Visit", back_populates="appointment", uselist=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "status IN ('scheduled', 'confirmed', 'checked_in', 'in_progress', 'completed', 'cancelled', 'no_show')",
            name="valid_status"
        ),
        CheckConstraint("end_time > start_time", name="valid_time_slot"),
        CheckConstraint(
            "appointment_date >= CURRENT_DATE OR status IN ('completed', 'cancelled', 'no_show')",
            name="no_past_appointments"
        ),
        Index("idx_appointments_patient", "patient_id"),
        Index("idx_appointments_provider", "provider_id"),
        Index("idx_appointments_date", "appointment_date"),
        Index("idx_appointments_status", "status"),
        Index("idx_appointments_provider_date", "provider_id", "appointment_date", "start_time"),
        Index("idx_appointments_patient_date", "patient_id", "appointment_date"),
    )


class Visit(Base):
    __tablename__ = "visits"
    
    visit_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    appointment_id = Column(UUID(as_uuid=True), ForeignKey("appointments.appointment_id"), unique=True, nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.provider_id"), nullable=False)
    visit_date = Column(Date, nullable=False)
    chief_complaint = Column(Text, nullable=True)
    diagnosis = Column(Text, nullable=True)
    treatment_plan = Column(Text, nullable=True)
    prescriptions = Column(JSONB, nullable=True)
    notes = Column(Text, nullable=True)
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), onupdate=datetime.now)
    
    # Relationships
    appointment = relationship("Appointment", back_populates="visit")
    patient = relationship("Patient", back_populates="visits")
    provider = relationship("Provider", back_populates="visits")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "(NOT follow_up_required) OR (follow_up_required AND follow_up_date IS NOT NULL)",
            name="valid_follow_up"
        ),
        Index("idx_visits_patient", "patient_id"),
        Index("idx_visits_provider", "provider_id"),
        Index("idx_visits_date", "visit_date"),
        Index("idx_visits_follow_up", "follow_up_date", postgresql_where=text("follow_up_required = TRUE")),
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    table_name = Column(String(50), nullable=False)
    record_id = Column(UUID(as_uuid=True), nullable=False)
    action = Column(String(20), nullable=False)
    old_data = Column(JSONB, nullable=True)
    new_data = Column(JSONB, nullable=True)
    changed_by = Column(UUID(as_uuid=True), nullable=True)
    changed_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    ip_address = Column(INET, nullable=True)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("action IN ('INSERT', 'UPDATE', 'DELETE')", name="valid_action"),
        Index("idx_audit_table_record", "table_name", "record_id"),
        Index("idx_audit_changed_at", "changed_at"),
        Index("idx_audit_changed_by", "changed_by"),
    )
