CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "btree_gist"; -- Required for EXCLUDE constraints

-- Patients Table
CREATE TABLE patients (
    patient_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20) NOT NULL,
    address TEXT,
    insurance_id VARCHAR(50),
    emergency_contact_name VARCHAR(200),
    emergency_contact_phone VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT valid_dob CHECK (date_of_birth < CURRENT_DATE),
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

COMMENT ON TABLE patients IS 'Patient demographic and contact information';
COMMENT ON COLUMN patients.insurance_id IS 'Health insurance policy number';

-- Providers Table
CREATE TABLE providers (
    provider_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE providers IS 'Healthcare providers (doctors, nurses, specialists)';
COMMENT ON COLUMN providers.is_active IS 'Whether provider is currently accepting appointments';

-- Provider Schedules Table
CREATE TABLE provider_schedules (
    schedule_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    provider_id UUID NOT NULL REFERENCES providers(provider_id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    effective_from DATE NOT NULL DEFAULT CURRENT_DATE,
    effective_until DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT valid_day CHECK (day_of_week BETWEEN 0 AND 6),
    CONSTRAINT valid_time_range CHECK (end_time > start_time),
    CONSTRAINT valid_date_range CHECK (effective_until IS NULL OR effective_until >= effective_from)
);

COMMENT ON TABLE provider_schedules IS 'Recurring weekly availability schedules for providers';
COMMENT ON COLUMN provider_schedules.day_of_week IS '0=Sunday, 1=Monday, ..., 6=Saturday';
COMMENT ON COLUMN provider_schedules.effective_until IS 'NULL means schedule continues indefinitely';

-- Appointments Table
CREATE TABLE appointments (
    appointment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    provider_id UUID NOT NULL REFERENCES providers(provider_id) ON DELETE CASCADE,
    appointment_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'scheduled',
    appointment_type VARCHAR(50) DEFAULT 'routine',
    notes TEXT,
    cancellation_reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT valid_status CHECK (
        status IN ('scheduled', 'confirmed', 'checked_in', 'in_progress', 'completed', 'cancelled', 'no_show')
    ),
    CONSTRAINT valid_time_slot CHECK (end_time > start_time),
    CONSTRAINT no_past_appointments CHECK (
        appointment_date >= CURRENT_DATE OR status IN ('completed', 'cancelled', 'no_show')
    ),
    
    -- CRITICAL: Prevent overlapping appointments for same provider
    -- This is the PRIMARY defense against double-booking
    EXCLUDE USING gist (
        provider_id WITH =,
        appointment_date WITH =,
        tsrange(
            (appointment_date + start_time)::timestamp,
            (appointment_date + end_time)::timestamp,
            '[)'
        ) WITH &&
    ) WHERE (status NOT IN ('cancelled', 'no_show'))
);

COMMENT ON TABLE appointments IS 'Scheduled appointments between patients and providers';
COMMENT ON CONSTRAINT appointments_provider_id_appointment_date_tsrange_excl ON appointments 
    IS 'Prevents double-booking: ensures no overlapping appointments for the same provider';

-- Visits Table
CREATE TABLE visits (
    visit_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    appointment_id UUID UNIQUE NOT NULL REFERENCES appointments(appointment_id) ON DELETE CASCADE,
    patient_id UUID NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    provider_id UUID NOT NULL REFERENCES providers(provider_id) ON DELETE CASCADE,
    visit_date DATE NOT NULL,
    chief_complaint TEXT,
    diagnosis TEXT,
    treatment_plan TEXT,
    prescriptions JSONB,
    notes TEXT,
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT valid_follow_up CHECK (
        (NOT follow_up_required) OR (follow_up_required AND follow_up_date IS NOT NULL)
    )
);

COMMENT ON TABLE visits IS 'Post-appointment visit records with clinical documentation';
COMMENT ON COLUMN visits.prescriptions IS 'Structured prescription data in JSON format';

-- Audit Logs Table
CREATE TABLE audit_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name VARCHAR(50) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(20) NOT NULL,
    old_data JSONB,
    new_data JSONB,
    changed_by UUID,
    changed_at TIMESTAMPTZ DEFAULT NOW(),
    ip_address INET,
    
    CONSTRAINT valid_action CHECK (action IN ('INSERT', 'UPDATE', 'DELETE'))
);

COMMENT ON TABLE audit_logs IS 'Immutable audit trail for sensitive operations';

-- Patient Indexes
CREATE INDEX idx_patients_last_name ON patients(last_name);
CREATE INDEX idx_patients_email ON patients(email) WHERE email IS NOT NULL;
CREATE INDEX idx_patients_phone ON patients(phone);
CREATE INDEX idx_patients_dob ON patients(date_of_birth);

-- Provider Indexes
CREATE INDEX idx_providers_specialty ON providers(specialty);
CREATE INDEX idx_providers_active ON providers(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_providers_license ON providers(license_number);

-- Provider Schedule Indexes
CREATE INDEX idx_schedules_provider ON provider_schedules(provider_id);
CREATE INDEX idx_schedules_day ON provider_schedules(day_of_week);
CREATE INDEX idx_schedules_provider_day ON provider_schedules(provider_id, day_of_week);
CREATE INDEX idx_schedules_dates ON provider_schedules(effective_from, effective_until);

-- Appointment Indexes (CRITICAL for performance)
CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_appointments_provider ON appointments(provider_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_appointments_patient_date ON appointments(patient_id, appointment_date DESC);
CREATE INDEX idx_appointments_provider_date ON appointments(provider_id, appointment_date, start_time);
CREATE INDEX idx_appointments_provider_status ON appointments(provider_id, status) 
    WHERE status IN ('scheduled', 'confirmed');

-- Visit Indexes
CREATE INDEX idx_visits_appointment ON visits(appointment_id);
CREATE INDEX idx_visits_patient ON visits(patient_id);
CREATE INDEX idx_visits_provider ON visits(provider_id);
CREATE INDEX idx_visits_date ON visits(visit_date DESC);
CREATE INDEX idx_visits_follow_up ON visits(follow_up_date) 
    WHERE follow_up_required = TRUE;

-- Audit Log Indexes
CREATE INDEX idx_audit_table_record ON audit_logs(table_name, record_id);
CREATE INDEX idx_audit_changed_at ON audit_logs(changed_at DESC);
CREATE INDEX idx_audit_changed_by ON audit_logs(changed_by);
CREATE INDEX idx_audit_action ON audit_logs(action);

-- Function: Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at triggers
CREATE TRIGGER update_patients_updated_at 
    BEFORE UPDATE ON patients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_providers_updated_at 
    BEFORE UPDATE ON providers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_appointments_updated_at 
    BEFORE UPDATE ON appointments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_visits_updated_at 
    BEFORE UPDATE ON visits
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function: Audit appointment changes
CREATE OR REPLACE FUNCTION audit_appointment_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO audit_logs(table_name, record_id, action, new_data)
        VALUES ('appointments', NEW.appointment_id, 'INSERT', row_to_json(NEW)::jsonb);
        RETURN NEW;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO audit_logs(table_name, record_id, action, old_data, new_data)
        VALUES ('appointments', NEW.appointment_id, 'UPDATE', 
                row_to_json(OLD)::jsonb, row_to_json(NEW)::jsonb);
        RETURN NEW;
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO audit_logs(table_name, record_id, action, old_data)
        VALUES ('appointments', OLD.appointment_id, 'DELETE', row_to_json(OLD)::jsonb);
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_appointments
    AFTER INSERT OR UPDATE OR DELETE ON appointments
    FOR EACH ROW EXECUTE FUNCTION audit_appointment_changes();


-- Function: Check provider availability
CREATE OR REPLACE FUNCTION check_provider_availability(
    p_provider_id UUID,
    p_appointment_date DATE,
    p_start_time TIME,
    p_end_time TIME
)
RETURNS BOOLEAN AS $$
DECLARE
    schedule_exists BOOLEAN;
BEGIN
-- Check if provider has a schedule for this day/time
    SELECT EXISTS(
        SELECT 1 
        FROM provider_schedules ps
        WHERE ps.provider_id = p_provider_id
        AND ps.day_of_week = EXTRACT(DOW FROM p_appointment_date)
        AND ps.effective_from <= p_appointment_date
        AND (ps.effective_until IS NULL OR ps.effective_until >= p_appointment_date)
        AND ps.start_time <= p_start_time
        AND ps.end_time >= p_end_time
    ) INTO schedule_exists;
    
    RETURN schedule_exists;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION check_provider_availability IS 
    'Verifies provider has scheduled availability for the requested date/time';

-- Function: Get available time slots
CREATE OR REPLACE FUNCTION get_available_slots(
    p_provider_id UUID,
    p_date DATE,
    p_slot_duration INTERVAL DEFAULT '30 minutes'
)
RETURNS TABLE(start_time TIME, end_time TIME) AS $$
DECLARE
    schedule_start TIME;
    schedule_end TIME;
    current_slot TIME;
BEGIN
    -- Get provider schedule for this day
    SELECT ps.start_time, ps.end_time
    INTO schedule_start, schedule_end
    FROM provider_schedules ps
    WHERE ps.provider_id = p_provider_id
    AND ps.day_of_week = EXTRACT(DOW FROM p_date)
    AND ps.effective_from <= p_date
    AND (ps.effective_until IS NULL OR ps.effective_until >= p_date)
    LIMIT 1;
    
    IF schedule_start IS NULL THEN
        RETURN;
    END IF;
    
    -- Generate time slots
    current_slot := schedule_start;
    
    WHILE current_slot + p_slot_duration <= schedule_end LOOP
        -- Check if slot is available
        IF NOT EXISTS (
            SELECT 1 FROM appointments a
            WHERE a.provider_id = p_provider_id
            AND a.appointment_date = p_date
            AND a.status NOT IN ('cancelled', 'no_show')
            AND (
                (a.start_time < current_slot + p_slot_duration AND a.end_time > current_slot)
            )
        ) THEN
            RETURN QUERY SELECT current_slot, current_slot + p_slot_duration;
        END IF;
        
        current_slot := current_slot + p_slot_duration;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_available_slots IS 
    'Returns all available time slots for a provider on a given date';

-- View: Provider Utilization
CREATE OR REPLACE VIEW provider_utilization AS
SELECT 
    p.provider_id,
    p.first_name || ' ' || p.last_name AS provider_name,
    p.specialty,
    COUNT(a.appointment_id) AS total_appointments,
    COUNT(CASE WHEN a.status = 'completed' THEN 1 END) AS completed_appointments,
    COUNT(CASE WHEN a.status = 'no_show' THEN 1 END) AS no_shows,
    COUNT(CASE WHEN a.status = 'cancelled' THEN 1 END) AS cancellations,
    ROUND(
        COUNT(CASE WHEN a.status = 'completed' THEN 1 END)::NUMERIC / 
        NULLIF(COUNT(a.appointment_id), 0) * 100, 
        2
    ) AS no_show_rate
FROM appointments
WHERE appointment_date >= CURRENT_DATE - INTERVAL '1 year'
GROUP BY DATE_TRUNC('month', appointment_date)
ORDER BY month DESC;

COMMENT ON VIEW no_show_analysis IS 
    'Monthly no-show rates for the past year';


