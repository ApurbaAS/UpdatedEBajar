from django import forms
from .models import user_clients
from validate_email_address import validate_email
from django.core.mail import EmailMessage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site




class UserClientForm(forms.ModelForm):
    
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    contact_number = forms.IntegerField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Contact Number'}))
    
    
    class Meta:
        model = user_clients.User_Client
        fields = ('first_name', 'last_name', 'email', 'contact_number', 'password')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'exampleInputEmail1'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'exampleInputEmail1'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'id': 'exampleInputEmail1'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'exampleInputNumber'}),
            
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                      'id': 'exampleInputPassword1',
                    'placeholder': 'password: (8 char,A,a,@)',
                }),
            }
        labels = {
            'password': '',  # Remove the label for the password field
            }                          


    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if not validate_email(email):
            raise forms.ValidationError('Invalid email address.')
        
        if user_clients.User_Client.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address already in use.')
        
        current_site = get_current_site(self.request)
        verification_link = f'http://{current_site.domain}/verify-email/?email={email}'
    
        self.send_verification_email(verification_link)
        
        return email 



    def send_verification_email(self, verification_link):
        email = self.cleaned_data.get('email')
        subject = 'Email Verification'
        message = f'Click the following link to verify your email: {verification_link}'
        from_email = 'Apurba007100@gmail.com'
        to_email = email
        email = EmailMessage(subject, message, from_email, [to_email])
        email.send()
    

    
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError('Password must contain at least 8 characters.')

        has_uppercase = False
        has_lowercase = False
        has_punctuation = False

        for char in password:
            if char.isupper():
                has_uppercase = True
            elif char.islower():
                has_lowercase = True
            elif char in "@#$%&_!":
                has_punctuation = True

        if not has_uppercase:
            raise forms.ValidationError('Password must contain at least one uppercase letter.')

        if not has_lowercase:
            raise forms.ValidationError('Password must contain at least one lowercase letter.')

        if not has_punctuation:
            raise forms.ValidationError('Password must contain at least one of the following punctuation characters: @#$%&_!')

        return password
    
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserClientForm, self).__init__(*args, **kwargs)
    
        if self.instance.pk:
            # If it is, make the password field read-only
            self.fields['password'].widget.attrs['readonly'] = True    
        