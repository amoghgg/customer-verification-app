# api/urls.py
from django.urls import path
from . import views
print("DEBUG views.py content:", dir(views))
urlpatterns = [
    path('customer-details/', views.customer_details),
    path('confirm-delivery/', views.confirm_delivery),
]
