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
    '''
    form for creating a user
    '''
    email = forms.EmailField(required=True,max_length=50,min_length=5)
    first_name = forms.CharField(required=True,max_length=30)
    last_name = forms.CharField(required=True,max_length=30)
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
        
class AnonymousUserCreateForm(UserCreateForm):
    '''
    form for creating anonymous user
    '''
    email = forms.EmailField(required=False,max_length=50)
    first_name = forms.CharField(required=False,max_length=30)
    last_name = forms.CharField(required=False,max_length=30)
    
    def clean_email(self):
        '''
        will check that email field were not supplied
        '''
        email = self.cleaned_data.get('email')
        if (email):
            raise forms.ValidationError(u'You are not allowed to update email on skip-register action')
        return email    
    
    class Meta(UserCreateForm.Meta):
        model = User
        
class UserProfileForm(ModelForm):
    '''
    form for creating a user profile
    '''
    class Meta:
        model = UserProfile
        fields = ("uuid","is_anonymous")
        
class AnonymousUserProfileForm(UserProfileForm):
    '''
    form for creating anonymous user profile
    ''' 
    class Meta(UserProfileForm.Meta):
        model = UserProfile
#===============================================================================
# end forms
#===============================================================================