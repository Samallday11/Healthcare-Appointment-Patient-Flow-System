Healthcare Appointment and Patient Flow System

This project is a backend system for managing healthcare appointments, patient records, provider availability, and clinical visits. I built it to demonstrate how real world backend systems handle scheduling, data integrity, and concurrent access to shared resources.

The focus of this project is not UI. It is on database design, transaction safety, and building APIs that behave correctly under realistic constraints.

Why I Built This

Healthcare scheduling is a good example of a problem where mistakes are costly. Providers cannot be double booked, records must remain consistent, and changes need to be traceable. I wanted a project that reflects those requirements and shows how they are enforced at the database and service layers rather than relying only on application logic.

This project is intended to be readable and reviewable by engineers looking at my GitHub.

What This Project Demonstrates

This system shows practical backend skills including:

Advanced SQL design using PostgreSQL with a fully normalized schema and strong referential integrity
Database level enforcement of scheduling rules using constraints rather than only application checks
Safe handling of concurrent appointment requests using transactional logic
Clear separation between database access, business logic, and API layers
RESTful API design using FastAPI with request and response validation

System Architecture
Database Layer
PostgreSQL with a normalized schema, constraints to prevent invalid data, triggers for audit logging, and views for analytics

Service Layer
Business logic for appointment scheduling, provider availability checks, and status transitions

API Layer
FastAPI endpoints with validation, error handling, and OpenAPI documentation

Database Design Overview

The core tables in the system include:

patients for demographic and contact information
providers for healthcare providers and specialties
provider_schedules for recurring weekly availability
appointments for scheduled visits with conflict prevention
visits for post appointment clinical records
audit_logs for tracking changes over time

To prevent double booking, the database uses an exclusion constraint that blocks overlapping appointment times for the same provider even when requests occur concurrently.

EXCLUDE USING gist (
    provider_id WITH =,
    appointment_date WITH =,
    tsrange(start_time, end_time) WITH &&
)
WHERE (status NOT IN ('cancelled', 'no_show'));


This approach keeps scheduling rules enforced at the database level rather than relying only on application code.

API Overview

The API exposes endpoints for managing patients, providers, and appointments.

Patients
POST /api/v1/patients
GET /api/v1/patients
GET /api/v1/patients/{id}
PATCH /api/v1/patients/{id}

Providers
POST /api/v1/providers
GET /api/v1/providers
GET /api/v1/providers/{id}

Appointments
POST /api/v1/appointments
PATCH /api/v1/appointments/{id}
GET /api/v1/appointments

Interactive API documentation is available at http://localhost:8000/docs
 when the application is running.

Running the Project Locally

Requirements include Python 3.11 or newer and PostgreSQL 14 or newer. Docker can be used to run PostgreSQL locally.

Clone the repository and configure environment variables.

git clone <your-repo-url>
cd healthcare-system
cp .env.example .env


Start the database and apply the schema.

docker-compose up -d postgres
docker exec -i healthcare_postgres psql -U postgres -d healthcare_db < db/schema.sql
docker exec -i healthcare_postgres psql -U postgres -d healthcare_db < db/seed.sql


Install dependencies and run the API.

pip install -r requirements.txt
uvicorn app.main:app --reload

Project Structure
healthcare-system/
app/        API and service logic
db/         SQL schema, seed data, and migrations
docs/       SRS and design documentation
tests/      Automated tests

What a Reviewer Should Look At

If you are reviewing this project, the most important parts are:

The database schema and constraints in db/schema.sql
How appointment scheduling is handled in the service layer
How transactions are used to guarantee consistency
The API layer and how validation and errors are handled

Future Improvements

  Authentication and role based access control
  More detailed analytics and reporting
  Background jobs for reminders
  Performance testing under concurrent load

Author

  Samuel Tilahun
  Backend focused software engineering student with an interest in databases, healthcare systems, and backend architecture
