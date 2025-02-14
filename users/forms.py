from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.hashers import check_password

from .models import User


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Введите логин',
            'password': 'Введите пароль',
        }


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Логин',
            'email': 'Электронная почта',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
    
    def email_clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот e-mail уже используется.')
        return email
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        existing_users = User.objects.all()
        for user in existing_users:
            if check_password(password, user.password):
                raise forms.ValidationError('Этот пароль уже существует. Попробуйте другой.')
        return password
    
class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'image', 
            'first_name',
            'last_name',
            'email',
        )

    image = forms.ImageField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()