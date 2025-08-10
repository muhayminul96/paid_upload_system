# Django Payment Gateway + File Upload System

A Django-based system where users can upload files **only after completing a payment** via **aamarPay sandbox**.  
Uploaded files are processed in the background using **Celery** to count words.  
Includes REST API endpoints, Bootstrap-based dashboard, activity logging, and Django Admin for inspection.

---

## 🚀 Features
- **JWT Authentication** (Login/Registration)
- **aamarPay Sandbox Payment Integration**
- **File Upload** (only after successful payment)
- **Background Word Count Processing** with Celery
- **Activity Logging**
- **Payment History Tracking**
- **Bootstrap Dashboard UI**
- **Django Admin Panel**

---

## 📦 Requirements
- Python 3.10+
- Django 4+
- Django REST Framework
- SimpleJWT
- Celery
- Redis
- python-docx
- requests

---

## 🔧 Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/aamarpay-django-task.git
cd aamarpay-django-task
```
