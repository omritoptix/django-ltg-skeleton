'''
contains the forms of our application
Created on April 7, 2014

@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.models import ModelForm
from ltg_backend_app.models import UserProfile

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin forms
#===============================================================================

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=False,max_length=50)
    first_name = forms.CharField(required=False,max_length=30)
    last_name = forms.CharField(required=False,max_length=30)
    password1 = forms.CharField(required=True, max_length=16, min_length=8)
    password2 = forms.CharField(required=True, max_length=16, min_length=8)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email           
          
    class Meta:
        model = User
        fields = ( "username", "email", "first_name", "last_name" )
        
        
class UserProfileForm(ModelForm):
    class Meta:
        model= UserProfile
        fields = ("uuid",)
                
#===============================================================================
# end forms
#===============================================================================