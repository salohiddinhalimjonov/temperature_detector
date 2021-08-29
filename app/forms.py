from django.forms import ModelForm
from .models import AboutUrl
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

class ChangePassword(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'style':'width:500px;'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'style':'width:500px;'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'style':'width:500px;'}))


class UserRegisterForm(UserCreationForm):
    CHOICES = (('Male', 'Male'),
               ('Female', 'Female'))
    gender = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class':'form-control', 'style':'width:150px;'}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control', 'style':'width:500px;'}))
    image = forms.ImageField(label='Image',required=False, widget = forms.ClearableFileInput(
            attrs = {'class': 'form-control mb-2', 'placeholder':
        'IMAGE','style':'width:500px;'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'style':'width:500px;'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'style':'width:500px;'}))
    password1 = forms.CharField(label='Enter Password',widget=forms.PasswordInput(attrs={'class':'form-control', 'style': 'width:500px;'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control', 'style': 'width:500px;'}))
    class Meta:
        model = CustomUser
        fields = [ 'email', 'first_name', 'last_name','image', 'gender', 'password1', 'password2']

class UrlForm(ModelForm):
    UrlChoices = (
        ('Important', 'Important'),
        ('Almost Important', 'Almost Important'),
        ('Not Important', 'Not Important')
    )
    original_url = forms.URLField(label="Enter the Url", widget=forms.TextInput( attrs={'class': 'form-control','placeholder':'example.com', 'style': 'width: 500px;'}))
    choices = forms.ChoiceField( choices=UrlChoices, label="Select a choice", widget=forms.Select(attrs={'class':'form-control', 'style': 'width: 500px;'}))
    description = forms.CharField( label="Enter the Description", widget=forms.Textarea( attrs={'rows':10, 'class': 'form-control' ,'placeholder':'Enter the Description', 'style': 'width: 500px;'}))
    title = forms.CharField(label="Enter the Title", widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 500px;', 'placeholder': 'Title'}))
    class Meta:
        model = AboutUrl
        fields = ['original_url', 'title', 'description','choices', ]

    def clean(self):
        super(UrlForm, self).clean()
        original_url = self.cleaned_data.get('original_url')
        title = self.cleaned_data.get('title')
        if len(original_url) < 20:
            self._errors['original_url'] = self.error_class(['Minimum 10 characters are required!'])

        if len(title) < 2:
            self._errors['title'] = self.error_class(['Minimum 2 characters are required!'])

        return self.cleaned_data
