# -*- coding: utf-8 -*-
'''
Tastypie will play with this file to create a rest server
Created on Jun 20, 2013

@author: Yariv Katz
@version: 1.0
@copyright: nerdeez.com
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app import settings
from tastypie.resources import ModelResource
import os
from django.conf.urls import url
from tastypie.utils import trailing_slash
from django.utils import simplejson
from django.core.urlresolvers import resolve, get_script_prefix
from django.contrib.auth.models import User
from tastypie.http import *
from tastypie.models import ApiKey
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.core.mail.message import EmailMultiAlternatives
from smtplib import SMTPSenderRefused
from django.template.context import Context
import logging
from tastypie import fields
from django.core.exceptions import ValidationError
from ltg_backend_app.forms import UserCreateForm, UserProfileForm
from ltg_backend_app.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist




#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin constants
#===============================================================================

API_URL = '/api/v1/'

#===============================================================================
# end constants
#===============================================================================


#===============================================================================
# begin abstract resources
#===============================================================================

class LtgResource(ModelResource):
    '''
    abstract class with commone attribute common to all my rest models
    '''
    creation_date = fields.DateTimeField(attribute='creation_date',readonly=True)
    modified_data = fields.DateTimeField(attribute='modified_data',readonly=True)
    
    #set read only fields
    class Meta:
        allowed_methods = ['get']
        always_return_data = True
        
    @staticmethod
    def get_pk_from_uri(uri):
        '''
        gets a uri and return the pk from the url
        @param uri: the url
        @return: string the pk 
        '''
        
        prefix = get_script_prefix()
        chomped_uri = uri
    
        if prefix and chomped_uri.startswith(prefix):
            chomped_uri = chomped_uri[len(prefix)-1:]
    
        try:
            view, args, kwargs = resolve(chomped_uri)
        except:
            return 0
    
        return kwargs['pk']

        
#===============================================================================
# end abstract resources
#===============================================================================

#===============================================================================
# begin global function
#===============================================================================

def is_send_grid():
    '''
    determine if i can send mails in this server
    @return: True if i can
    '''
    return 'SENDGRID_USERNAME' in os.environ


#===============================================================================
# end global function
#===============================================================================

#===============================================================================
# begin globals
#===============================================================================

# set global logger to be root logger
logger = logging.getLogger()

#===============================================================================
# end globals
#===============================================================================


#===============================================================================
# begin the actual rest api
#===============================================================================

        
    
        
class UtilitiesResource(LtgResource):
    '''
    the api for things that are not attached to models: 
    - contact us: url: /api/v1/utilities/contact/
    '''
    
    class Meta(LtgResource.Meta):
        allowed_methods = ['post']
        
        
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r"^(?P<resource_name>%s)/register%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('register'), name="api_register"),
            url(r"^(?P<resource_name>%s)/forgot-password%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('forgot_password'), name="api_forgot_password"),
            url(r"^(?P<resource_name>%s)/register-facebook%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('register_facebook'), name="api_register_facebook"),
        ]
        
    def login(self, request=None, **kwargs):
        '''
        login request is sent here
        @param password: the user password 
        @param email: the user email 
        @return: 401 if login failed with a disctionary with a message, if success will return the following object
        {
            'success': True,
            'message': 'Successfully logged in',
            "user_profile": <The user profile object>,
            'api_key': <the api key of the user valid for a day>,
            'username': <the username of the password>
        }
        '''
        pass
    
    def register(self, request=None, **kwargs):
        '''
        will try and register the user will expect the following post params
        @param first_name: 
        @param last_name: 
        @param email: 
        @param password:
        @param uuid: 
        @return success: will return a 201 code with the following object 
        {
            success: <Boolean>,
            message: <String>
        } 
        '''
        #get params
        post = simplejson.loads(request.body)
        email = post.get('email', None)
        password = post.get('password', None)
        first_name = post.get('first_name', None)
        last_name = post.get('last_name', None)
        uuid = post.get('uuid', None)
        
        #check if there is a user connected to this uuid, if so return it with it's api key and username
        try:
            if (email is None and uuid is not None):
                user = UserProfile.objects.get(uuid=uuid).user
                return self.create_response(request, {
                         'success': True,
                         'message': 'Successfully logged in',
                         'username':user.username,
                         'api_key':user.api_key.key,
                         }, HttpAccepted)
            
        except ObjectDoesNotExist:
            pass
        
        #create the username
        api_key = ApiKey()
        username = api_key.generate_key()[0:30]
        
        #if email is none, it's an anonymous user. generate a password
        if (email is None):
            password = api_key.generate_key()[0:16]

        try:               
            #create user form
            user_create_form = UserCreateForm({
                                          'username': username,
                                          'email': email,
                                          'password1': password, 
                                          'password2': password, 
                                          'first_name': first_name, 
                                          'last_name': last_name, 
                                          })
            #validate the form
            if not user_create_form.is_valid():
                raise ValidationError(user_create_form.errors)
            #create user profile form 
            user_profile_form = UserProfileForm({
                                                'uuid':uuid,
            })   
            #validate the user profile form
            if not user_profile_form.is_valid():
                raise ValidationError((user_profile_form.errors))
            
            #create the user and save it
            user = user_create_form.save()
            #create the user profile but don't save it yet
            user_profile = user_profile_form.save(commit=False)
            #attach the user to user profile
            user_profile.user = user
            user_profile.save()
                    
            return self.create_response(request, {
                         'success': True,
                         'message': "User created successfully",
                         'username':user.username,
                         'api_key':user.api_key.key,
                         }, HttpCreated)

        # handle exceptions
        except ValidationError as e:
            return self.create_response(request, {
                 'success': False,
                 'errors': e.message_dict,
                 }, HttpBadRequest)
            
        except:
            return self.create_response(request, {
                 'success': False,
                 'errors': 'could not register user',
                 }, HttpApplicationError)
        
            
        
    def forgot_password(self, request=None, **kwargs):
        '''
        api for the user to create a new password
        return 200 on success
        return 401 on unuthorized (account not activated)
        return 404 on account not found
        return 500 if failed to send mail
        '''
        pass
        
        
    def register_facebook(self, request=None, **kwargs):
        '''
        api for user facebook registration will get the following post params
        @param facebook_user_id: the users id on facebook 
        @param facebook_access_token: the users token on facebook 
        @param uuid: device uuid
        @return  
                 success - 201 if created containing the following details
                 {
                     success: true
                     message: 'registered a new device'
                     api_key: 'api key for the user'
                     username: 'username of the user',
                     'phone_profile': '<profile object>'  
                 }
                 success - 202 if user exists containing the following details
                 {
                     success: true
                     message: 'user is already registered'
                     api_key: 'api key for the user'
                     username: 'username of the user'
                     'phone_profile': '<profile object>'    
                 }
        '''
        
        pass
            
            
        
#===============================================================================
# end teh actual rest api
#===============================================================================