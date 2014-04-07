'''
contains the form for nerdeez
Created on June 21, 2013

@author: Yariv Katz
@version: 1.0
@copyright: nerdeez.com
'''

#===============================================================================
# begin imports
#===============================================================================

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin forms
#===============================================================================

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=50, min_length=5)
    first_name = forms.CharField(required=True, max_length=30, min_length=2)
    last_name = forms.CharField(required=True, max_length=30, min_length=2)
    password1 = forms.CharField(required=True, max_length=16, min_length=8)
    password2 = forms.CharField(required=True, max_length=16, min_length=8)
    class Meta:
        model = User
        fields = ( "username", "email", "first_name", "last_name" )
        
#===============================================================================
# end forms
#===============================================================================