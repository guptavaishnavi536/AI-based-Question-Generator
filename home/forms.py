from django import forms
from django.contrib.auth.models import User
from .models import Queries, Login, Signup, QnA
from . import models

class QueriesForm(forms.ModelForm):
    class Meta:
        model = Queries
        fields = ['Username','email','query']
        
class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['username','psw']
        
class SignupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ['username','email', 'psw']
        
class QnAForm(forms.ModelForm):
    class Meta:
        model = QnA
        fields = ['pdf']