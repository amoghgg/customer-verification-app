# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from api import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('upload-proof/', views.upload_proof_video),  # include() expects a URLconf, not a module
]
