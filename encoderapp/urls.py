from django.urls import path
from .views import EncodeImageView, DownloadEncodedImageView, DecodeImageView


urlpatterns = [
    path('', EncodeImageView.as_view(), name='encode'),
    path('decode', DecodeImageView.as_view(), name='decode'),
    path('download/<int:pk>', DownloadEncodedImageView.as_view(), name='download_encoded_image'),
]