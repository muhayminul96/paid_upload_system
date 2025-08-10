# Django Payment Gateway + File Upload System

A Django-based system where users can upload files **only after completing a payment** via **aamarPay sandbox**.  
Uploaded files are processed in the background using **Celery** to count words.  
Includes REST API endpoints, Bootstrap-based dashboard, activity logging, and Django Admin for inspection.

---

## Features
- **JWT Authentication** (Login/Registration)
- **aamarPay Sandbox Payment Integration**
- **File Upload** (only after successful payment)
- **Background Word Count Processing** with Celery
- **Activity Logging**
- **Payment History Tracking**
- **Bootstrap Dashboard UI**
- **Django Admin Panel**

---

## Requirements
- Python 3.10+
- Django 4+
- Django REST Framework
- SimpleJWT
- Celery
- Redis
- python-docx
- requests

---

## Installation & Setup

### Clone the repository
```bash
git clone https://github.com/muhayminul96/paid_upload_system.git
cd aamarpay-django-task
```

### Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt

```


### Run migrations
```bash
python manage.py migrate

```


### Create a superuser

```bash
python manage.py createsuperuser
```
## Running the Project

### Start Redis server

```bash
redis-server

```

### Start Celery worker

```bash
celery -A paid_upload_system worker -l info

```

### Start Django development server

```bash
python manage.py runserver

```



