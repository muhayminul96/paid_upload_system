from django.urls import path
from . import views

urlpatterns = [
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.list_files, name='list_files'),
    path('activity/', views.list_activity, name='list_activity'),
    path('transactions/', views.list_transactions, name='list_transactions'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
