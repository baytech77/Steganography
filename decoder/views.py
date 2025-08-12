from django.views.generic.edit import FormView
from django.shortcuts import render
from .forms import DecodeImageForm
from PIL import Image

from utility_function import decode_image
from .forms import DecodeImageForm

class DecodeImageView(FormView):
    template_name = 'decode.html'
    form_class = DecodeImageForm

    def form_valid(self, form):
        encoded_image = Image.open(form.cleaned_data['encoded_image'])
        decoded_message = decode_image(encoded_image)

        context = self.get_context_data(form=form)
        if decoded_message == None:
            context['decode_error'] = "This image is not encoded by this app!!"
            context['decoded_message'] = None
        else:
            context['decoded_message'] = decoded_message
            context['decode_error'] = None
        return self.render_to_response(context)