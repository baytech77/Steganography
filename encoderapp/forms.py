from django import forms
from .models import EncodedImage

class EncodeImageForm(forms.ModelForm):
    class Meta:
        model = EncodedImage
        fields = ['cover_image', 'password', 'secret_message']
        widgets = {
            'secret_message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter your secret message here...'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': "Input password to protect your secret message"
            })}
            


