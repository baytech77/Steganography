from django.views.generic.edit import FormView
from django.shortcuts import render
from .forms import DecodeImageForm
from PIL import Image

from utility_function import decode_image, decode_image2
from .forms import DecodeImageForm

class DecodeImageView(FormView):
    template_name = 'decode.html'
    form_class = DecodeImageForm


    def form_valid(self, form):
        encoded_image = Image.open(form.cleaned_data['encoded_image'])
        password = form.cleaned_data['password']
        decoded_message, error = decode_image(encoded_image, password)

        context = self.get_context_data(form=form)
        if error:
            context['decode_error'] = error
            context['decoded_message'] = None
        else:
            context['decoded_message'] = decoded_message
            context['decode_error'] = None
        return self.render_to_response(context)
    



class DecodeImageView2(FormView):
    template_name = 'decode.html'
    form_class = DecodeImageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('password_required', False)
        context.setdefault('decode_error', None)
        context.setdefault('extracted_message', None)
        return context
    

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            encoded_image = Image.open(form.cleaned_data['encoded_image'])
            password = form.cleaned_data.get('password')

            if not password:
                decoded_message, error = decode_image2(encoded_image, check_only=True)
                if error:
                    return self.render_to_response(self.get_context_data(form=form,
                                                                         decode_error=error,
                                                                         password_required=False,
                                                                         extracted_message=None
                                                                           ))
                else:
                    return self.render_to_response(self.get_context_data(form=form,
                                                                            decode_error=None,
                                                                            password_required=True,
                                                                            extracted_message=None
                                                                            ))
            
            decoded_message, error = decode_image2(encoded_image, password=password, check_only=False)
            if error:
                return self.render_to_response(self.get_context_data(form=form,
                                                                        decode_error=error,
                                                                        password_required=True,
                                                                        extracted_message=None
                                                                        ))
            else:
                return self.render_to_response(self.get_context_data(form=form,
                                                                        decode_error=None,
                                                                        password_required=True,
                                                                        extracted_message=decoded_message
                                                                        ))
            
        else:
            return self.form_invalid(form)