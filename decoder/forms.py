from django import forms


class DecodeImageForm(forms.Form):
    encoded_image = forms.ImageField(label='Select Encoded Image')
