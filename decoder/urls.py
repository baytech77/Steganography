from django.urls import path
from .views import DecodeImageView


urlpatterns = [
    path('decode/', DecodeImageView.as_view(), name='decode'),
]