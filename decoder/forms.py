from django import forms


class DecodeImageForm(forms.Form):
    encoded_image = forms.ImageField(label='Select Encoded Image')
    password = forms.CharField(widget=forms.PasswordInput, help_text="input password used to encode the secret message")