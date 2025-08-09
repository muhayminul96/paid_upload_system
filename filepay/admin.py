from django.contrib import admin
from .models import FileUpload, ActivityLog, PaymentTransaction

# Register your models here.

site = admin.AdminSite(name='file pay')

admin.site.register(ActivityLog)
admin.site.register(FileUpload)
admin.site.register(PaymentTransaction)
