from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.shortcuts import render
from .forms import EncodeImageForm
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .models import EncodedImage
from django.urls import reverse_lazy, reverse
from django.views import View
from PIL import Image
import os
import uuid
# Create your views here.




class EncodeImageView(FormView):
    template_name = 'encode.html'
    form_class = EncodeImageForm
    success_url = reverse_lazy('encode')

    def form_valid(self, form):
        try:
            # Create model instance without saving to DB yet
            encoded_image_instance = form.save(commit=False)
            
            # Generate unique filename using UUID
            unique_id = uuid.uuid4().hex[:8]
            original_filename = form.cleaned_data['cover_image'].name
            base_name, ext = os.path.splitext(original_filename)
            encoded_filename = f"{base_name}_encoded_{unique_id}{ext}"
            
            # Process image using Pillow
            cover_image = form.cleaned_data['cover_image']
            secret_message = form.cleaned_data['secret_message']
            
            # Convert message to binary with null terminator
            binary_message = ''.join(format(ord(char), '08b') for char in secret_message) + '00000000'
            
            # Open and process image
            img = Image.open(cover_image)
            pixels = img.load()
            data_index = 0
            
            # LSB Encoding logic
            for i in range(img.size[0]):
                for j in range(img.size[1]):
                    if data_index < len(binary_message):
                        pixel = list(pixels[i, j])
                        # Modify only the red channel (index 0)
                        pixel[0] = pixel[0] & ~1 | int(binary_message[data_index])
                        pixels[i, j] = tuple(pixel)
                        data_index += 1
                    else:
                        break
                if data_index >= len(binary_message):
                    break
            
            # Save encoded image to media directory
            encoded_dir = os.path.join('media', 'encoded_images')
            os.makedirs(encoded_dir, exist_ok=True)
            encoded_path = os.path.join(encoded_dir, encoded_filename)
            img.save(encoded_path)
            
            # Update model instance
            encoded_image_instance.encoded_image.name = f"encoded_images/{encoded_filename}"
            encoded_image_instance.save()
            
            # Redirect to download page with new instance's PK
            return redirect(reverse('download_encoded_image', 
                                args=[encoded_image_instance.pk])) 
            
        except Exception as e:
            # Handle errors gracefully
            form.add_error(None, f"Encoding failed: {str(e)}")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supported_formats'] = ['PNG', 'BMP']  # Lossless formats for LSB
        return context
       

class DownloadEncodedImageView(FormView):
    def get(self, request, pk, *args, **kwargs):
        encoded_image_instance = get_object_or_404(EncodedImage, pk=pk)
        if not encoded_image_instance.encoded_image:
            raise Http404("Encoded image not found.")
        file_handle = encoded_image_instance.encoded_image.open()
        filename = os.path.basename(encoded_image_instance.encoded_image.name)
        return FileResponse(
            file_handle,
            as_attachment=True,
            filename=filename
        )