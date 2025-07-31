from django.views.generic.edit import FormView
from django.shortcuts import render
from .forms import DecodeImageForm
from PIL import Image

class DecodeImageView(FormView):
    template_name = 'decode.html'
    form_class = DecodeImageForm

    def form_valid(self, form):
        encoded_image = form.cleaned_data['encoded_image']
        img = Image.open(encoded_image)
        pixels = img.load()
        binary_message = ''

        # Extract LSBs from red channel (index 0)
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                pixel = list(pixels[i, j])
                binary_message += str(pixel[0] & 1)

        # Check for null terminator presence
        if '00000000' not in binary_message:
            notification = "The image does not contain an encoded message or was not encoded using this application."
            return self.render_to_response(self.get_context_data(form=form, notification=notification))

        # Extract message up to null terminator
        message = ''
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if byte == '00000000':  # Null terminator found
                break
            message += chr(int(byte, 2))

        if not message.strip():
            notification = "The image does not contain an encoded message or was not encoded using this application."
            return self.render_to_response(self.get_context_data(form=form, notification=notification))

        # Valid message found
        return self.render_to_response(self.get_context_data(form=form, message=message))
