# -*- coding: utf-8 -*-
'''
Tastypie will play with this file to create a rest server
Created on March 15, 2013

@author: Yariv Katz & Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app import settings
from tastypie.resources import ModelResource, Resource
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
from ltg_backend_app.forms import UserCreateForm, UserProfileForm,\
    AnonymousUserCreateForm, AnonymousUserProfileForm
from ltg_backend_app.models import UserProfile, Tutor
from django.core.exceptions import ObjectDoesNotExist
from tastypie.authentication import ApiKeyAuthentication, Authentication
from ltg_backend_app.ltg_api.api_auth import LtgApiKeyAuthentication
from tastypie.bundle import Bundle
import requests
from ltg_backend_app.ltg_api.hubspot_client import HubSpotClient
from tastypie.validation import FormValidation
import uuid
from tastypie.authorization import Authorization
from django.contrib.auth import login, authenticate





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
    
    @staticmethod
    def mail_authenticate(email=None, password=None):
        """ 
        Authenticate a user based on email address.
        @param email
        @param passwrod
        @return: the user if authenticated 
        """
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return authenticate(username = user.username,password = password)
        except User.DoesNotExist:
            return None 
    
        
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

class UserResource(ModelResource):
    '''
    resource for our user model
    '''
    class Meta:
        resource_name = 'user'
        excludes = ['password']
        allowed_methods = ['post']
        include_resource_uri = False
        always_return_data = True
        validation = FormValidation(form_class=UserCreateForm)
        authentication = Authentication()
        authorization = Authorization()
        queryset = User.objects.all()

    def obj_create(self, bundle , **kwargs):
        # get username and password
        bundle.data['username'] = bundle.data.get('username',uuid.uuid4().hex[:30])
        bundle.data['password1'] = bundle.data.get('password',uuid.uuid4().hex[:16])
        bundle.data['password2'] = bundle.data['password1']
        # create the object 
        bundle = super(UserResource, self).obj_create(bundle)
        # set the new password
        bundle.obj.set_password(bundle.data['password1'])
        bundle.obj.save()
        # return the api_key in the response
        bundle.data['api_key'] = bundle.obj.api_key.key
        # del the extra bundle fields so it won't be included in the response
        del bundle.data['password1']
        del bundle.data['password2']

        return bundle
    
    
class AnonymousUserResource(UserResource):
    '''
    resource for anonymous user creation
    '''
    class Meta(UserResource.Meta):
        validation = FormValidation(form_class=AnonymousUserCreateForm)
    
class UserProfileResource(LtgResource):
    '''
    resource for our user profile model
    '''
    user = fields.ToOneField(UserResource,'user')
    class Meta:
        allowed_methods = ['post']
        include_resource_uri = True
        always_return_data = True
        validation = FormValidation(form_class=UserProfileForm)
        authentication = Authentication()
        authorization = Authorization()
        queryset = UserProfile.objects.all()
    
        
class AnonymousUserProfileResource(UserProfileResource):
    '''
    resource for anonymous user profile creation
    '''  
    class Meta(UserProfileResource.Meta):
        validation = FormValidation(form_class=AnonymousUserProfileForm)
        
    def hydrate(self,bundle):
        bundle.obj.is_anonymous = True
        return super(AnonymousUserProfileResource,self).hydrate(bundle)

class TutorResource(Resource):
    '''
    will return all tutors by using hubspot api as it's data source.
    '''
    id = fields.CharField(attribute='id',null=True)
    first_name = fields.CharField(attribute='first_name',null=True)
    last_name = fields.CharField(attribute='last_name', null=True)
    file_upload = fields.CharField(attribute='file_upload', null=True)
    email = fields.CharField(attribute='image_url', null=True)
    skype_id = fields.CharField(attribute='skype_id', null=True)
    tutor_description = fields.CharField(attribute='tutor_description', null=True)
    tutor_rate = fields.CharField(attribute='tutor_rate', null=True)
    tutor_video = fields.CharField(attribute='tutor_video', null=True)
    tutor_speciality = fields.CharField(attribute='tutor_speciality', null=True)
    tutor_groups = fields.CharField(attribute='tutor_groups', null=True)
    country = fields.CharField(attribute='country', null=True)

    class Meta:
        resource_name = 'tutor'
        allowed_methods = ['get']
        object_class = Tutor
        authentication = Authentication()
        
    def _client(self):
        #define our api client
        return HubSpotClient(settings.HUBSPOT_API_KEY)
        
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}
    
        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj['id']
    
        return kwargs
    
    def obj_get(self, request=None, **kwargs):
        result = self._client().get_contact(kwargs['pk'])
        return Tutor(**result)
    
    def get_object_list(self, request):
        list_id = request.GET.get('list_id',settings.HUBSPOT_LIST_ID)
        contact_list = self._client().get_contact_list(list_id)
        
        results = []
        for result in contact_list:
            tutor = Tutor(**result)
            results.append(tutor)
     
        return results
    
    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)
    
    def dehydrate(self,bundle):
        updated_data = {}
        # remove null fields
        for key in bundle.data:
            if (bundle.data[key] is not None):
                updated_data[key] = bundle.data[key]
        
        bundle.data = updated_data
        return super(TutorResource, self).dehydrate(bundle)    
        
        
class UtilitiesResource(LtgResource):
    '''
    the api for things that are not attached to models: 
    - contact us: url: /api/v1/utilities/contact/
    '''
    
    class Meta(LtgResource.Meta):
        allowed_methods = ['post']
        authentication = Authentication()
        
        
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r"^(?P<resource_name>%s)/register%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('register'), name="api_register"),
            url(r"^(?P<resource_name>%s)/skip-register%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('skip_register'), name="api_skip_register"),
            url(r"^(?P<resource_name>%s)/forgot-password%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('forgot_password'), name="api_forgot_password"),
            url(r"^(?P<resource_name>%s)/register-facebook%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('register_facebook'), name="api_register_facebook"),
            url(r"^(?P<resource_name>%s)/send-email%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('send_email'), name="api_send_email"),
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
        # get the params
        post = simplejson.loads(request.body)
        password = post.get('password','')
        email = post.get('email','')
        
        # try to login the user using it's mail
        user = self.mail_authenticate(email=email, password=password)
        if (user):
            if user.is_active and not user.profile.is_anonymous:
                login(request, user)
                # get the user api key
                api_key, created = ApiKey.objects.get_or_create(user=user)
                if (created):
                    api_key.save()                    
                return self.create_response(request, {
                    'success': True,
                    'message':'Successfully logged in!',
                    'username':user.username,
                    'api_key':api_key.key
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'message': 'Account is not active',
                    }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'Invalid email or password',
                }, HttpUnauthorized )
            
            
    def skip_register(self, request=None, **kwargs):
        '''
        will check if the user which skipped registration is already registered
        by it's uuid. if not , it will register him.
        '''       
        # get params
        post = simplejson.loads(request.body)
        try:
            # check if user is already registered
            user_profile = UserProfile.objects.get(uuid = post.get('uuid'),is_anonymous=True)
            return self.create_response(request, {
                 'success': True,
                 'message': "User created successfully",
                 'username':user_profile.user.username,
                 'api_key':user_profile.user.api_key.key,
                 },)  
            
        except UserProfile.DoesNotExist:
            # register the user
            return self.register(request,user_resource = AnonymousUserResource(), user_profile_resource = AnonymousUserProfileResource()) 
                 

    def register(self, request=None, user_resource = UserResource(), user_profile_resource = UserProfileResource(), **kwargs):
        '''
        will try and register the user. 
        @param user_resource : the resource which we will use to create the user (either UserResource or AnonymnousUserResource)
        @param user_profile_resource : the resource which we will use to create the user profile (either UserProfileResource or AnonymnousProfileUserResource) 
        @return success: will return a 201 code with the following object.
        {
            success: <Boolean>,
            message: <String>
        } 
        '''
        # get params
        post = simplejson.loads(request.body)
        # build bundle of user resource
        user = user_resource.obj_create(user_resource.build_bundle(data=post))
        try:
            # update the post dict with the user we just created
            post['user'] = user_resource.get_resource_uri(user)
            # build bundle of user profile resource
            user_profile_resource.obj_create(bundle=user_profile_resource.build_bundle(data=post))
          
        except Exception as e:
            user.obj.delete()
            raise e
                    
        return self.create_response(request, {
                     'success': True,
                     'message': "User created successfully",
                     'username':user.obj.username,
                     'api_key':user.obj.api_key.key,
                     }, HttpCreated)            
        
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
            
    def send_email(self, request=None, **kwargs):
        '''
        will send mail to info@ltgexam.com from the application users.
        @param username: the requesting user username
        @param api_key: the requesting user api_key
        @param subject: the subject of the mail
        @param message: the body of the mail
        @return:
            accepted - 202 if mail was successfully sent
        '''
        #get the post params
        post = simplejson.loads(request.body)
        message = post.get('message', "No Message Spcified")
        subject = post.get('subject', "No Subject Specified")
        
        #authenticate the user
        LtgApiKeyAuthentication().is_authenticated(request)
            
        # if user is not anonymous set 'from email' it with it's mail
        if (not request.user.is_anonymous() and request.user.email):
            from_email = request.user.email
        # else set 'from email' with it's uuid.
        else:
            try:
                from_email ='anonymous@uuid-' + str(request.user.profile.uuid) + '.com'
            except:
                from_email = 'anonymous@ltg-user.com'
                                    
        #send the mail
        if is_send_grid():
            t = get_template('emails/contact_us_email.html')
            html = t.render(Context({'message':message}))
            text_content = strip_tags(html)
            msg = EmailMultiAlternatives('Contact-Us: ' + subject, text_content, from_email, [settings.ADMIN_MAIL])
            msg.attach_alternative(html, "text/html")
            try:
                msg.send()
            except SMTPSenderRefused:
                return self.create_response(request, {
                    'success': False,
                    'message': 'Failed to send mail',
                    }, HttpApplicationError )
            
            return self.create_response(request, {
                'success': True,
                'message': 'email was successfully sent',
                }, HttpAccepted )
            
        else:
            return self.create_response(request, {
                'success': False,
                'message': 'mail server not defined',
                }, HttpApplicationError )
            
        
#===============================================================================
# end the actual rest api
#===============================================================================