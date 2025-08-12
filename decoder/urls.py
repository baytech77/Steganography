from django.urls import path
from .views import DecodeImageView


urlpatterns = [
    path('', DecodeImageView.as_view(), name='decode'),
]