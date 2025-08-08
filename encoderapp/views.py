from django.views.generic.edit import FormView
from django.views.generic import View
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.core.files.base import ContentFile
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from PIL import Image
import io
import os

from .forms import EncodeImageForm, DecodeImageForm
from .utility_function import encode_image, decode_image
from .models import EncodedImage


class EncodeImageView(FormView):
    template_name = "encode.html"
    form_class = EncodeImageForm
    success_url = reverse_lazy('encode')

    def form_valid(self, form):

        # Create model instance without saving to DB yet
        #encoded_image_instance = form.save(commit=False)
        
        # Generate unique filename using UUID
        #unique_id = uuid.uuid4().hex[:8]
        #original_filename = form.cleaned_data['cover_image'].name
        #base_name, ext = os.path.splitext(original_filename)
        #encoded_filename = f"{base_name}_encoded_{unique_id}{ext}"



        # ensuring each form content are cleaned using pillow
        cover_image = Image.open(form.cleaned_data['cover_image'])
        secret_message = form.cleaned_data['secret_message']

        # encoding messages into image
        encoded_image = encode_image(cover_image, secret_message)

        # saving the encoded_image to in-memory file
        img_io = io.BytesIO()
        encoded_image.save(img_io, format='PNG')
        img_content = ContentFile(img_io.getvalue(), 'encodede_image.png')
        
        # saving to database
        encoded_image_instance = EncodedImage(cover_image=form.cleaned_data['cover_image'])
        encoded_image_instance.encoded_image.save('encoded_image.png', img_content)
        encoded_image_instance.save()


        context = self.get_context_data(form=form)
        context['encoded_image_url'] = encoded_image_instance.encoded_image.url
        context['encoded_image_instance'] = encoded_image_instance
        return self.render_to_response(context)
    


class DecodeImageView(FormView):
    template_name = 'decode.html'
    form_class = DecodeImageForm

    def form_valid(self, form):
        encoded_image = Image.open(form.cleaned_data['encoded_image'])
        decoded_message = decode_image(encoded_image)

        context = self.get_context_data(form=form)
        context['decoded_message'] = decoded_message
        return self.render_to_response(context)
    


class DownloadEncodedImageView(View):

    def get(self, request, pk):
        encoded_image_instance = get_object_or_404(EncodedImage, pk=pk)
        if not encoded_image_instance.encoded_image:
            raise Http404("Encoded image not found!!.")
        return FileResponse(encoded_image_instance.encoded_image.open('rb'), as_attachment=True,filename='encoded_image.png')