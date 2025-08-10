import os
import requests, json
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import FileUpload, PaymentTransaction, ActivityLog
from .serializers import FileUploadSerializer, PaymentTransactionSerializer, ActivityLogSerializer
from django.utils.crypto import get_random_string
from .tasks import process_file_word_count
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    url = "https://sandbox.aamarpay.com/jsonpost.php"

    # Generate unique transaction ID
    tran_id = f"TXN{get_random_string(8)}"
    success_url = request.build_absolute_uri("/api/payment/success/")

    # Store the transaction in DB as pending
    PaymentTransaction.objects.create(
        user=request.user,
        transaction_id=tran_id,
        amount=100.0,
        status='pending',
        gateway_response={}
    )


    payload = json.dumps({
        "store_id": "aamarpaytest",
        "tran_id": tran_id,
        "success_url": success_url,
        "fail_url": request.build_absolute_uri("/api/payment/fail/"),
        "cancel_url": request.build_absolute_uri("/api/payment/cancel/"),
        "amount": "100.0",
        "currency": "BDT",
        "signature_key": settings.AMARPAY_SIGNATURE_KEY,
        "desc": "File Upload Payment",
        "cus_name": request.user.username,
        "cus_email": request.user.email or 'test@mail.com',
        "cus_add1": "Dhaka",
        "cus_city": "Dhaka",
        "cus_country": "Bangladesh",
        "cus_phone": "+8801700",
        "type": "json"
    })
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, headers=headers, data=payload).json()
    # If API returns a payment URL, redirect user to it
    if response.get("result"):
        try:
            transaction = PaymentTransaction.objects.get(transaction_id=tran_id)
            transaction.status = 'success'
            transaction.gateway_response = dict(response)
            transaction.save()

            # Log the activity for the correct user
            ActivityLog.objects.create(
                user=transaction.user,
                action="Payment Successful",
                metadata={"transaction_id": tran_id}
            )

            transaction_serialized = PaymentTransactionSerializer(transaction).data

            return Response({
                "message": "Payment recorded successfully",
                "transaction": transaction_serialized
            })

        except PaymentTransaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=404)
    else:
        return Response({"error": "Payment initiation failed", "details": resp_data}, status=400)


# @api_view(['GET'])
# def payment_success(request):
#     print(request.data)
#     tran_id = request.GET.get('mer_txnid')
#     amount = request.GET.get('amount')
#     status_param = request.GET.get('pay_status', 'Success')
#
#     try:
#         transaction = PaymentTransaction.objects.get(transaction_id=tran_id)
#         transaction.status = 'success'
#         transaction.gateway_response = dict(request.GET)
#         transaction.save()
#
#         # Log the activity for the correct user
#         ActivityLog.objects.create(
#             user=transaction.user,
#             action="Payment Successful",
#             metadata={"transaction_id": tran_id}
#         )
#
#         return Response({"message": "Payment recorded successfully"})
#
#     except PaymentTransaction.DoesNotExist:
#         return Response({"error": "Transaction not found"}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    file_obj = request.FILES.get('file')
    if not file_obj:
        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    filename = file_obj.name
    upload_instance = FileUpload.objects.create(
        user=request.user,
        file=file_obj,
        filename=filename,
        status="processing"
    )

    # Trigger Celery task
    process_file_word_count.delay(upload_instance.id)

    ActivityLog.objects.create(
        user=request.user,
        action="File Uploaded",
        metadata={"filename": filename}
    )

    return Response(FileUploadSerializer(upload_instance).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_files(request):
    files = FileUpload.objects.filter(user=request.user)
    return Response(FileUploadSerializer(files, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_activity(request):
    logs = ActivityLog.objects.filter(user=request.user)
    return Response(ActivityLogSerializer(logs, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_transactions(request):
    transactions = PaymentTransaction.objects.filter(user=request.user)
    return Response(PaymentTransactionSerializer(transactions, many=True).data)
