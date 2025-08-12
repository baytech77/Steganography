from django.urls import path
from .views import EncodeImageView, DownloadEncodedImageView, landingView


urlpatterns = [
    path('', landingView.as_view(), name='landing'),
    path('encode', EncodeImageView.as_view(), name='encode'),
    path('download/<int:pk>', DownloadEncodedImageView.as_view(), name='download_encoded_image'),
]