# Childminder Registration System

A Django-based childminder registration system for Ready Kids CMA. This application allows childminders to submit registration applications and administrators to review submissions through a dashboard.

## Features

- Multi-section registration form covering:
  - Personal details
  - Address history
  - Premises information
  - Childcare service details
  - Training qualifications
  - Employment history
  - Household members
  - Suitability declarations
  - Legal consent and declaration
- Admin dashboard with application statistics
- Django admin panel for detailed application management
- PostgreSQL-compatible data models

## Tech Stack

- **Backend**: Django 5.2
- **Database**: SQLite (default, configurable for PostgreSQL)
- **Frontend**: HTML5, CSS3 (Django templates)
- **Python**: 3.11+

## Project Structure

```
cma_project/
├── config/                 # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── applications/           # Main application
│   ├── models.py          # Data models
│   ├── forms.py           # Form definitions
│   ├── views.py           # View logic
│   ├── admin.py           # Admin configuration
│   ├── urls.py            # URL routing
│   └── templates/
│       ├── base.html
│       └── applications/
│           ├── register.html
│           └── dashboard.html
├── manage.py
└── db.sqlite3
```

## Installation & Setup

### 1. Clone the repository

```bash
cd /path/to/cma_project
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install django
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

## Usage

### For Applicants

1. Navigate to `http://localhost:8000/register/`
2. Fill out the multi-section registration form
3. Submit the application

### For Administrators

1. **Dashboard**: Visit `http://localhost:8000/dashboard/` to view:
   - Total applications count
   - Submitted vs. draft applications
   - Application list with status badges

2. **Django Admin**: Visit `http://localhost:8000/admin/` to:
   - View detailed application information
   - Edit or delete applications
   - Manage all related data (addresses, employment, household members, etc.)

## Database Models

- **Application**: Core model tracking application status and timestamps
- **PersonalDetails**: Applicant personal information
- **AddressEntry**: Address history (5-year requirement)
- **Premises**: Childcare premises details
- **ChildcareService**: Service and age group information
- **Training**: Training qualifications and certifications
- **EmploymentEntry**: Employment history
- **HouseholdMember**: Household members at premises
- **Reference**: Professional references
- **Suitability**: Suitability declarations and DBS information
- **Declaration**: Legal consent and signatures

## Development Notes

- All models use UUIDs for primary keys
- Status tracking: `DRAFT`, `SUBMITTED`
- Timestamps automatically tracked via `created_at` and `updated_at`
- Form validation handled through Django ModelForms
- FormSets used for one-to-many relationships

## Configuration

### Database

The default configuration uses SQLite. To use PostgreSQL:

1. Install `psycopg2`: `pip install psycopg2-binary`
2. Update `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cma_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Static Files

For production deployment:

```bash
python manage.py collectstatic
```

## Testing

Run Django's built-in checks:

```bash
python manage.py check
```

## License

Proprietary - Ready Kids CMA

## Support

For issues or questions, contact the development team.
