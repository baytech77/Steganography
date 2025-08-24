from django.views.generic.edit import FormView
from django.views.generic import View
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.core.files.base import ContentFile
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from PIL import Image
import io


from .forms import EncodeImageForm
from utility_function import encode_image
from .models import EncodedImage


class landingView(TemplateView):
    template_name = 'landing.html'

class EncodeImageView(FormView):
    template_name = "encode.html"
    form_class = EncodeImageForm
    success_url = reverse_lazy('encode')
    
    def form_valid(self, form):

        # ensuring each form content are cleaned using pillow
        cover_image = Image.open(form.cleaned_data['cover_image'])
        secret_message = form.cleaned_data['secret_message']
        password = form.cleaned_data['password']

        # encoding messages into image
        encoded_image = encode_image(cover_image, secret_message, password)

        # saving the encoded_image to in-memory file
        img_io = io.BytesIO()
        encoded_image.save(img_io, format='PNG')
        img_content = ContentFile(img_io.getvalue(), 'encodede_image.png')
        
        # saving to database
        encoded_image_instance = EncodedImage(cover_image=form.cleaned_data['cover_image'])
        encoded_image_instance.encoded_image.save('encoded_image.png', img_content)
        #encoded_image_instance.save()


        context = self.get_context_data(form=form)
        context['encoded_image_url'] = encoded_image_instance.encoded_image.url
        context['encoded_image_instance'] = encoded_image_instance
        return self.render_to_response(context)
    
    


class DownloadEncodedImageView(View):
    
    def get(self, request, pk):
        encoded_image_instance = get_object_or_404(EncodedImage, pk=pk)
        if not encoded_image_instance.encoded_image:
            raise Http404("Encoded image not found!!.")
        return FileResponse(encoded_image_instance.encoded_image.open('rb'), as_attachment=True,filename='encoded_image.png')
