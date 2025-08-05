from django.urls import path
from . import views  # Only import views, not individual view functions

urlpatterns = [
    path('customer-details/', views.customer_details),
    path('confirm-delivery/', views.confirm_delivery),
    path('upload-proof-video/', views.upload_proof_video),
]
