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

from django.contrib.auth.models import User
from django import forms
from django.forms.models import ModelForm
from ltg_backend_app.models import UserProfile, UserConceptScore, Attempt,\
    UserScore, UserSectionScore, LtgModel

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin forms
#===============================================================================

class LtgModelForm(ModelForm):
    '''
    all custom models will inherit from this form
    '''
    creation_date = forms.DateTimeField(required=False)
    
    class Meta:
        model = LtgModel

class UserForm(ModelForm):
    '''
    form for creating a user
    '''
    first_name = forms.CharField(required=True,max_length=30)
    email = forms.EmailField(required=True,max_length=50,min_length=5)
    last_name = forms.CharField(required=True,max_length=30)
    password = forms.CharField(required=True,max_length=16,min_length=8)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email           
          
    class Meta:
        model = User
        fields = ( "username", "email", "first_name", "last_name" )
        
class AnonymousUserCreateForm(UserForm):
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
    
    class Meta(UserForm.Meta):
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
        
class AttemptForm(LtgModelForm):
    '''
    form for creating attempt
    '''
    attempt = forms.IntegerField()
    answer = forms.IntegerField(max_value=4)
        
class UserScoreForm(LtgModelForm):
    '''
    class for creating user score
    
    - didn't assign it to a specific model since causes trouble with the tastypie obj_create and the foreign keys (i.e user_profile).
    
    - date added as char field since django doesn't support iso-8601 date format , which is what tastypie receives, and thus
    raises an error of the date not being valid.
    '''
    date = forms.CharField(required=True)
        
class UserSectionScoreForm(UserScoreForm):
    '''
    class for creating user section score
    '''
        
class UserConceptScoreForm(UserScoreForm):
    '''
    form for creating user concept score
    ''' 

#===============================================================================
# end forms
#===============================================================================