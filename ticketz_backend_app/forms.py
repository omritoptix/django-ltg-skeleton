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
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ( "username", "email" )
        
#===============================================================================
# end forms
#===============================================================================