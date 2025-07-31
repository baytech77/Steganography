from django.urls import path
from .views import EncodeImageView, DownloadEncodedImageView


urlpatterns = [
    path('', EncodeImageView.as_view(), name='encode'),
    path('download/<int:pk>', DownloadEncodedImageView.as_view(), name='download_encoded_image'),
]