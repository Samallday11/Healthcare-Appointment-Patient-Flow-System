INSERT INTO patients (patient_id, first_name, last_name, date_of_birth, email, phone, insurance_id, address, emergency_contact_name, emergency_contact_phone) VALUES
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'John', 'Doe', '1985-03-15', 'john.doe@email.com', '+12025551001', 'INS001', '123 Main St, Springfield, IL', 'Mary Doe', '+12025551101'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'Jane', 'Smith', '1990-07-22', 'jane.smith@email.com', '+12025551002', 'INS002', '456 Oak Ave, Springfield, IL', 'Tom Smith', '+12025551102'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'Michael', 'Johnson', '1978-11-03', 'michael.j@email.com', '+12025551003', 'INS003', '789 Pine Rd, Springfield, IL', 'Lisa Johnson', '+12025551103'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14', 'Emily', 'Williams', '1995-02-18', 'emily.w@email.com', '+12025551004', 'INS004', '321 Elm St, Springfield, IL', 'Robert Williams', '+12025551104'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15', 'David', 'Brown', '1982-09-27', 'david.brown@email.com', '+12025551005', 'INS005', '654 Maple Dr, Springfield, IL', 'Sarah Brown', '+12025551105'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', 'Sarah', 'Davis', '1988-05-10', 'sarah.davis@email.com', '+12025551006', 'INS006', '987 Cedar Ln, Springfield, IL', 'Mike Davis', '+12025551106'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a17', 'Christopher', 'Miller', '1975-12-30', 'chris.miller@email.com', '+12025551007', 'INS007', '147 Birch Ave, Springfield, IL', 'Anna Miller', '+12025551107'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a18', 'Jessica', 'Wilson', '1992-08-14', 'jessica.wilson@email.com', '+12025551008', 'INS008', '258 Spruce St, Springfield, IL', 'James Wilson', '+12025551108'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', 'Daniel', 'Moore', '1980-04-25', 'daniel.moore@email.com', '+12025551009', 'INS009', '369 Willow Rd, Springfield, IL', 'Karen Moore', '+12025551109'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a20', 'Ashley', 'Taylor', '1998-01-07', 'ashley.taylor@email.com', '+12025551010', 'INS010', '741 Aspen Dr, Springfield, IL', 'Mark Taylor', '+12025551110');

INSERT INTO providers (provider_id, first_name, last_name, specialty, license_number, email, phone, is_active) VALUES
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a21', 'Sarah', 'Martinez', 'Cardiology', 'LIC-CARD-001', 'dr.martinez@healthcare.com', '+12025552001', TRUE),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 'Robert', 'Chen', 'Primary Care', 'LIC-PRIM-002', 'dr.chen@healthcare.com', '+12025552002', TRUE),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a23', 'Lisa', 'Anderson', 'Pediatrics', 'LIC-PEDI-003', 'dr.anderson@healthcare.com', '+12025552003', TRUE),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a24', 'James', 'Taylor', 'Orthopedics', 'LIC-ORTH-004', 'dr.taylor@healthcare.com', '+12025552004', TRUE),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a25', 'Maria', 'Garcia', 'Dermatology', 'LIC-DERM-005', 'dr.garcia@healthcare.com', '+12025552005', TRUE),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a26', 'William', 'Lee', 'Neurology', 'LIC-NEUR-006', 'dr.lee@healthcare.com', '+12025552006', TRUE),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a27', 'Jennifer', 'White', 'Psychiatry', 'LIC-PSYCH-007', 'dr.white@healthcare.com', '+12025552007', TRUE),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a28', 'David', 'Harris', 'Ophthalmology', 'LIC-OPHT-008', 'dr.harris@healthcare.com', '+12025552008', TRUE);

-- Dr. Martinez (Cardiology) - Monday, Wednesday, Friday
INSERT INTO provider_schedules (provider_id, day_of_week, start_time, end_time, effective_from) VALUES
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a21', 1, '08:00:00', '17:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a21', 3, '08:00:00', '17:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a21', 5, '08:00:00', '17:00:00', '2025-01-01');

-- Dr. Chen (Primary Care) - Monday through Friday
INSERT INTO provider_schedules (provider_id, day_of_week, start_time, end_time, effective_from) VALUES
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 1, '08:00:00', '17:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 2, '08:00:00', '17:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 3, '08:00:00', '17:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 4, '08:00:00', '17:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', 5, '08:00:00', '17:00:00', '2025-01-01');

-- Dr. Anderson (Pediatrics) - Tuesday, Thursday
INSERT INTO provider_schedules (provider_id, day_of_week, start_time, end_time, effective_from) VALUES
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a23', 2, '09:00:00', '16:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a23', 4, '09:00:00', '16:00:00', '2025-01-01');

-- Dr. Taylor (Orthopedics) - Monday, Wednesday, Friday
INSERT INTO provider_schedules (provider_id, day_of_week, start_time, end_time, effective_from) VALUES
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a24', 1, '10:00:00', '18:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a24', 3, '10:00:00', '18:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a24', 5, '10:00:00', '18:00:00', '2025-01-01');

-- Dr. Garcia (Dermatology) - Monday through Thursday
INSERT INTO provider_schedules (provider_id, day_of_week, start_time, end_time, effective_from) VALUES
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a25', 1, '08:00:00', '17:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a25', 2, '08:00:00', '17:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a25', 3, '08:00:00', '17:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a25', 4, '08:00:00', '17:00:00', '2025-01-01');

-- Dr. Lee (Neurology) - Tuesday, Thursday, Friday
INSERT INTO provider_schedules (provider_id, day_of_week, start_time, end_time, effective_from) VALUES
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a26', 2, '09:00:00', '16:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a26', 4, '09:00:00', '16:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a26', 5, '09:00:00', '16:00:00', '2025-01-01');

-- Dr. White (Psychiatry) - Monday through Thursday
INSERT INTO provider_schedules (provider_id, day_of_week, start_time, end_time, effective_from) VALUES
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a27', 1, '10:00:00', '18:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a27', 2, '10:00:00', '18:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a27', 3, '10:00:00', '18:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a27', 4, '10:00:00', '18:00:00', '2025-01-01');

-- Dr. Harris (Ophthalmology) - Monday, Wednesday, Friday
INSERT INTO provider_schedules (provider_id, day_of_week, start_time, end_time, effective_from) VALUES
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a28', 1, '08:00:00', '16:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a28', 3, '08:00:00', '16:00:00', '2025-01-01'),
('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a28', 5, '08:00:00', '16:00:00', '2025-01-01');

-- Future appointments (upcoming)
INSERT INTO appointments (patient_id, provider_id, appointment_date, start_time, end_time, status, appointment_type, notes) VALUES
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a21', CURRENT_DATE + INTERVAL '7 days', '09:00:00', '09:30:00', 'scheduled', 'routine', 'Annual cardiac checkup'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', CURRENT_DATE + INTERVAL '3 days', '10:00:00', '10:30:00', 'confirmed', 'routine', 'Physical examination'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a24', CURRENT_DATE + INTERVAL '5 days', '14:00:00', '14:45:00', 'scheduled', 'follow_up', 'Follow-up for knee pain'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a25', CURRENT_DATE + INTERVAL '10 days', '11:00:00', '11:30:00', 'scheduled', 'consultation', 'Skin consultation'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', CURRENT_DATE + INTERVAL '2 days', '09:00:00', '09:30:00', 'confirmed', 'routine', 'Blood pressure check'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a26', CURRENT_DATE + INTERVAL '14 days', '10:00:00', '10:45:00', 'scheduled', 'consultation', 'Headache consultation'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a17', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a27', CURRENT_DATE + INTERVAL '8 days', '15:00:00', '15:45:00', 'scheduled', 'routine', 'Mental health checkup'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a18', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a28', CURRENT_DATE + INTERVAL '6 days', '09:30:00', '10:00:00', 'confirmed', 'routine', 'Eye examination');

-- Past completed appointments
INSERT INTO appointments (appointment_id, patient_id, provider_id, appointment_date, start_time, end_time, status, appointment_type, notes) VALUES
('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a31', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', CURRENT_DATE - INTERVAL '30 days', '09:00:00', '09:30:00', 'completed', 'routine', 'Annual physical'),
('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a32', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a21', CURRENT_DATE - INTERVAL '15 days', '10:00:00', '10:45:00', 'completed', 'routine', 'Heart check'),
('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a33', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a24', CURRENT_DATE - INTERVAL '45 days', '14:00:00', '14:30:00', 'completed', 'consultation', 'Initial orthopedic consultation'),
('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a34', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a25', CURRENT_DATE - INTERVAL '20 days', '13:00:00', '13:30:00', 'completed', 'follow_up', 'Acne follow-up'),
('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a35', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', CURRENT_DATE - INTERVAL '60 days', '11:00:00', '11:30:00', 'completed', 'routine', 'Wellness visit'),
('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a36', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a17', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a26', CURRENT_DATE - INTERVAL '35 days', '14:30:00', '15:15:00', 'completed', 'consultation', 'Migraine evaluation'),
('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a37', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', CURRENT_DATE - INTERVAL '10 days', '10:00:00', '10:30:00', 'completed', 'routine', 'Vaccination'),
('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a38', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a20', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a23', CURRENT_DATE - INTERVAL '25 days', '09:30:00', '10:00:00', 'completed', 'routine', 'Pediatric checkup');

-- Past cancelled appointments
INSERT INTO appointments (patient_id, provider_id, appointment_date, start_time, end_time, status, appointment_type, cancellation_reason) VALUES
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a24', CURRENT_DATE - INTERVAL '12 days', '16:00:00', '16:30:00', 'cancelled', 'routine', 'Patient conflict'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a18', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a25', CURRENT_DATE - INTERVAL '18 days', '14:00:00', '14:30:00', 'cancelled', 'consultation', 'Provider emergency');

-- Past no-show appointments
INSERT INTO appointments (patient_id, provider_id, appointment_date, start_time, end_time, status, appointment_type) VALUES
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a23', CURRENT_DATE - INTERVAL '7 days', '15:00:00', '15:30:00', 'no_show', 'routine'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a27', CURRENT_DATE - INTERVAL '22 days', '11:00:00', '11:45:00', 'no_show', 'consultation');

INSERT INTO visits (appointment_id, patient_id, provider_id, visit_date, chief_complaint, diagnosis, treatment_plan, prescriptions, notes, follow_up_required, follow_up_date) VALUES
('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a31', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', CURRENT_DATE - INTERVAL '30 days', 
 'Annual checkup', 
 'Patient in good health. Blood pressure slightly elevated.', 
 'Continue current medications. Monitor blood pressure at home. Increase physical activity to 30 minutes daily.', 
 '{"medications": [{"name": "Lisinopril", "dosage": "10mg", "frequency": "once daily"}]}'::jsonb,
 'Patient reports feeling well overall. Family history of hypertension noted.',
 TRUE, 
 CURRENT_DATE + INTERVAL '335 days'),

('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a32', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a21', CURRENT_DATE - INTERVAL '15 days', 
 'Chest discomfort', 
 'Mild hypertension, no acute cardiac issues detected', 
 'Started on antihypertensive medication. Lifestyle modifications recommended: reduce sodium intake, increase exercise, stress management.', 
 '{"medications": [{"name": "Amlodipine", "dosage": "5mg", "frequency": "once daily"}]}'::jsonb,
 'EKG normal. Patient counseled on warning signs of cardiac emergency.',
 TRUE, 
 CURRENT_DATE + INTERVAL '75 days'),

('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a33', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a24', CURRENT_DATE - INTERVAL '45 days', 
 'Chronic knee pain', 
 'Osteoarthritis of the right knee', 
 'Physical therapy 3x per week for 6 weeks. NSAIDs for pain management. Consider knee brace for support.',
 '{"medications": [{"name": "Ibuprofen", "dosage": "400mg", "frequency": "as needed, max 3x daily"}]}'::jsonb,
 'X-ray shows moderate joint space narrowing. Patient educated on exercises and weight management.',
 TRUE, 
 CURRENT_DATE + INTERVAL '45 days'),

('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a34', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a25', CURRENT_DATE - INTERVAL '20 days', 
 'Acne follow-up', 
 'Acne vulgaris - improving', 
 'Continue current topical treatment. Good progress noted.',
 '{"medications": [{"name": "Tretinoin Cream", "dosage": "0.025%", "frequency": "nightly"}]}'::jsonb,
 'Skin showing improvement. Patient compliant with treatment regimen.',
 TRUE, 
 CURRENT_DATE + INTERVAL '70 days'),

('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a35', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', CURRENT_DATE - INTERVAL '60 days', 
 'Wellness visit', 
 'Healthy adult, all vitals within normal limits', 
 'Continue healthy lifestyle. No changes needed.',
 NULL,
 'Patient reports good diet and regular exercise. All lab results normal.',
 TRUE, 
 CURRENT_DATE + INTERVAL '305 days'),

('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a36', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a17', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a26', CURRENT_DATE - INTERVAL '35 days', 
 'Severe headaches', 
 'Migraine without aura', 
 'Prescribed preventive medication. Advised to keep headache diary. Identify and avoid triggers.',
 '{"medications": [{"name": "Topiramate", "dosage": "25mg", "frequency": "twice daily"}, {"name": "Sumatriptan", "dosage": "50mg", "frequency": "as needed for acute attacks"}]}'::jsonb,
 'MRI scheduled to rule out other causes. Patient educated on migraine management.',
 TRUE, 
 CURRENT_DATE + INTERVAL '55 days'),

('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a37', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', CURRENT_DATE - INTERVAL '10 days', 
 'Vaccination', 
 'Routine immunization', 
 'Annual flu vaccine administered. No adverse reactions.',
 NULL,
 'Patient tolerated vaccination well. No contraindications noted.',
 FALSE, 
 NULL),

('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a38', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a20', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a23', CURRENT_DATE - INTERVAL '25 days', 
 'Well-child visit', 
 'Healthy child, growth and development appropriate for age', 
 'Continue current diet and activities. Ensure adequate sleep.',
 NULL,
 'Height and weight at 60th percentile. Developmental milestones met.',
 TRUE, 
 CURRENT_DATE + INTERVAL '155 days');

-- Display summary of inserted data
SELECT 'Patients:' AS entity, COUNT(*) AS count FROM patients
UNION ALL
SELECT 'Providers:', COUNT(*) FROM providers
UNION ALL
SELECT 'Provider Schedules:', COUNT(*) FROM provider_schedules
UNION ALL
SELECT 'Appointments:', COUNT(*) FROM appointments
UNION ALL
SELECT 'Visits:', COUNT(*) FROM visits
UNION ALL
SELECT 'Audit Logs:', COUNT(*) FROM audit_logs;

-- Display appointment status breakdown
SELECT 
    status,
    COUNT(*) AS count
FROM appointments
GROUP BY status
ORDER BY count DESC;

-- Display upcoming appointments
SELECT 
    a.appointment_date,
    a.start_time,
    pt.first_name || ' ' || pt.last_name AS patient,
    pr.first_name || ' ' || pr.last_name AS provider,
    pr.specialty,
    a.status
FROM appointments a
JOIN patients pt ON a.patient_id = pt.patient_id
JOIN providers pr ON a.provider_id = pr.provider_id
WHERE a.appointment_date >= CURRENT_DATE
ORDER BY a.appointment_date, a.start_time
LIMIT 10;

