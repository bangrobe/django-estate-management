from django.urls import path
from .views import ApartmentCreateAPIView, ApartmentDetailAPIView

urlpatterns = [
    path('add/', ApartmentCreateAPIView.as_view(), name='apartments-create'),
    path('my-apartment/', ApartmentDetailAPIView.as_view(), name='apartments-detail'),
]