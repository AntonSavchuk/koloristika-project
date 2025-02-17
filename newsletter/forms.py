from django import forms
from .models import Newsletter
from ckeditor_uploader.widgets import CKEditorUploadingWidget

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
