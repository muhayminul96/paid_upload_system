from django.contrib import admin
from .models import FileUpload, PaymentTransaction, ActivityLog

class ReadOnlyAdminMixin:

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

@admin.register(FileUpload)
class FileUploadAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'filename', 'word_count', 'status', 'upload_time')
    readonly_fields = ('user', 'filename','file', 'word_count', 'status', 'upload_time')

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'transaction_id', 'amount', 'status', 'timestamp')
    readonly_fields = ('user', 'transaction_id', 'amount','gateway_response', 'status', 'timestamp')

@admin.register(ActivityLog)
class ActivityLogAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'metadata', 'timestamp')
    readonly_fields = ('user', 'action', 'metadata', 'timestamp')
