from ckeditor_uploader.widgets import CKEditorUploadingWidget
from allauth.account.models import EmailAddress
from django import forms

from .models import Newsletter, Subscription

class NewsletterForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget()) 
    
    class Meta:
        model = Newsletter
        fields = ['title', 'content', 'font_size', 'text_color', 'background_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}), 
            'font_size': forms.NumberInput(attrs={'class': 'form-control', 'min': 10, 'max': 50}),
            'text_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'background_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Subscription.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже подписан на обновления.")
        return email