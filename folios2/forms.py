from django.contrib.auth.models import User
from .models import *
from django import forms

class UserForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput)
    
    
    class Meta:
        
        model = User
        
        fields = ['username', 'email', 'password']
        
        
class PortfolioForm(forms.ModelForm):
    
    
    class Meta:
        
        model = Portfolio
        
        fields = ['name', 'created', 'start_date', 'end_date', 'user']
        

