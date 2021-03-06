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
from ltg_backend_app.models import LtgModel, LtgUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField

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
    password = forms.CharField(required=True, min_length=8)
              
    class Meta:
        model = LtgUser
        exclude = ['username']
        
        
class ResetPasswordForm(forms.Form):
    password = forms.CharField(max_length=16,min_length=8)
    
    
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = LtgUser
        fields = ('email','first_name','last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = LtgUser
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
    
#===============================================================================
# end forms
#===============================================================================