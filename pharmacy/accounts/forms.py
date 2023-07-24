from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField



class UserCreationForm(forms.ModelForm):
    password1=forms.CharField(label='password',widget=forms.PasswordInput)
    password2=forms.CharField(label='confirm password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields =('email','full_name')

    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] !=cd['password2']:
            raise forms.ValidationError('password must match')
        return cd['password2']

    def save(self, commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField()

    class Meta:
        model=User
        fields=('email','password','full_name')

    def clean_password(self):
         return self.initial["password"]

class UserLoginForm(forms.Form):
    email=forms.EmailField(label='ایمیل',widget=forms.EmailInput(attrs={'class':'form-control'}))
    password=forms.CharField(label='پسورد',widget=forms.PasswordInput(attrs={'class':'form-control'}))

class UserRegisterForm(forms.Form):
    email=forms.EmailField(label='ایمیل',widget=forms.EmailInput(attrs={'class':'form-control'}))
    full_name=forms.CharField(label='نام کامل',widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(label='پسورد',widget=forms.PasswordInput(attrs={'class':'form-control'}))

class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('full_name','phone_number')

