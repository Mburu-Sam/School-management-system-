# School Management System

A Django-based school management system with role-based authentication for administrators, teachers, and students.

## Features

- Public homepage with school information and admission application form
- Student sign-up and login for profile access
- Teacher sign-up and login for grade and class overview
- Admin sign-up and login for complete system administration
- CRUD management for students, teachers, subjects, classes, attendance, grades, and fee statements
- Downloadable reports for transcripts, attendance, and fee statements
- Role-based access control to protect dashboards and management functions

## Tech Stack

- Python 3.12+
- Django 5.0.7
- SQLite (default local database)

## Project Structure

- learning/ - app logic, models, forms, views, and templates
- School/ - project settings and URL configuration
- templates/ - shared authentication templates and layout wrappers

## Prerequisites

- Python 3.12+
- Virtual environment (recommended)

## Setup Instructions

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install django==5.0.7
   ```

4. Apply migrations:

   ```bash
   python manage.py migrate
   ```

5. Create an initial admin account (recommended for production use):

   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

7. Open the application in a browser:

   - Homepage: http://127.0.0.1:8000/
   - Login: http://127.0.0.1:8000/accounts/login/
   - Student signup: http://127.0.0.1:8000/student/signup/
   - Teacher signup: http://127.0.0.1:8000/teacher/signup/
   - Admin signup: http://127.0.0.1:8000/admin/signup/
   - Admin panel: http://127.0.0.1:8000/admin/

## Authentication and Authorization Flow

### Admin
- Can sign in with an admin account or a superuser account.
- Has full access to create, update, and delete students, teachers, classes, subjects, attendance, grades, and fee statements.
- Can navigate to all management screens from the dashboard.

### Teacher
- Can sign up through the teacher sign-up page.
- After login, is redirected to the teacher dashboard.
- Can view grades and oversee class-related performance for assigned students.

### Student
- Can sign up through the student sign-up page.
- After login, is redirected to the student dashboard.
- Can update their profile, view attendance, grades, fee statements, and download reports.

## Report Downloads

- Transcript download: /student/transcript/download/
- Attendance report download: /student/attendance/report/download/
- Fee statement report download: /student/fee/report/download/

## Notes

- The default local database is SQLite.
- The login system redirects users to the appropriate dashboard based on role.
- Admin users can manage the full system, while teachers and students have restricted access to their relevant areas.
- Public visitors can apply for admission through the homepage.
