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

from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import ApiKeyAuthentication
import os

from django.conf.urls import url
from tastypie.utils import trailing_slash
from django.utils import simplejson
from tastypie.exceptions import Unauthorized
from django.core.urlresolvers import resolve, get_script_prefix
from ltg_backend_app.ltg_forms.user_create import UserCreateForm
from django.contrib.auth.models import User
from tastypie.http import HttpConflict, HttpBadRequest, HttpCreated
from tastypie.models import ApiKey
from django.template.loader import get_template


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
    
    #set read only fields
    class Meta:
        allowed_methods = ['get']
        always_return_data = True
        read_only_fields = ['creation_date', 'modified_data']
        invisible_fields = []
        
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
    
    def hydrate(self, bundle):
        read_only_fields = self.Meta.read_only_fields
        for field in read_only_fields:
            if field in bundle.data:
                del bundle.data[field]
        return super(LtgResource, self).hydrate(bundle)
    
    def dehydrate(self, bundle):
        invisible_fields = self.Meta.invisible_fields
        for field in invisible_fields:
            if field in bundle.data:
                print field
                del bundle.data[field]
        return super(LtgResource, self).dehydrate(bundle)
        
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
# begin authorization/authentication
#===============================================================================

class LtgApiKeyAuthentication(ApiKeyAuthentication):
    def extract_credentials(self, request):
        username, api_key = super(LtgApiKeyAuthentication, self).extract_credentials(request)
        if username == None and api_key == None and (request.method == 'POST' or request.method == 'PUT'):
            post = simplejson.loads(request.body)
            username = post.get('username')
            api_key = post.get('api_key')
        return username, api_key
            

class LtgReadForFreeAuthentication(LtgApiKeyAuthentication):
    
    def is_authenticated(self, request, **kwargs):
        '''
        get is allowed without cradentials and all other actions require api key and username
        @return: boolean if authenticated
        '''
        if request.method == 'GET':
            return True
        return super( LtgReadForFreeAuthentication, self ).is_authenticated( request, **kwargs )
        
class LtgReadForFreeAuthorization( DjangoAuthorization ):
    '''
    Authorizes every authenticated user to perform GET, 
    it will allow post to everyone
    and put/delete if there is owner only he can do it.
    '''
    
    def owner_auth(self, bundle):
        '''
        gets a bundle and return true if the current user is the owner
        @param Object bundle: tastypie bundle object
        @return: true if owner raise Unauthorized if not
        '''
        obj = bundle.obj
        if hasattr(obj, 'owner') and (obj.owner() == bundle.request.user.username or bundle.request.user.username in obj.owner()):
            return True
        else:
            raise Unauthorized('you are not auth to modify this record');
        
    def read_detail(self, object_list, bundle):
        return True
    
    def create_detail(self, object_list, bundle):
        return True
    
    def create_list(self, object_list, bundle):
        return object_list
    
    def update_detail(self, object_list, bundle):
        return self.owner_auth(bundle)
    
    def delete_detail(self, object_list, bundle):
        return self.owner_auth(bundle)
    
class LtgOnlyOwnerCanReadAuthorization( LtgReadForFreeAuthorization ):
    '''
    Authorizes every authenticated owner to perform GET, for all others
    performs NerdeezReadForFreeAuthorization.
    '''
    
    def read_detail(self, object_list, bundle):
        return self.owner_auth(bundle)

        

#===============================================================================
# end authorization/authentication
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
        will try and register the user will except the following post params
        @param first_name: 
        @param last_name: 
        @param email: 
        @param password: 
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
        
        #create the username
        api_key = ApiKey()
        username = api_key.generate_key()[0:30]
        
        #check if the user exists with this mail
        if User.objects.filter(email=email).count() > 0:
            return self.create_response(request, {
                         'success': False,
                         'message': "Duplicate email",
                         }, HttpConflict)
            
        #check validation and create the user
        create_form = UserCreateForm({
                                      'username': username,
                                      'email': email,
                                      'password1': password, 
                                      'password2': password, 
                                      'first_name': first_name, 
                                      'last_name': last_name, 
        })
        if create_form.is_valid():
            create_form.save()
            
            #send the mail
            #send the verification mail
            if is_send_grid():
                t = get_template('emails/register_approval_mail.html')
                html = t.render(Context({'admin_mail': settings.ADMIN_MAIL, 'admin_phone': settings.ADMIN_PHONE}))
                text_content = strip_tags(html)
                msg = EmailMultiAlternatives('2Nite Registration', text_content, settings.FROM_EMAIL_ADDRESS, [email])
                msg.attach_alternative(html, "text/html")
                try:
                    msg.send()
                except SMTPSenderRefused, e:
                    return self.create_response(request, {
                        'success': False,
                        'message': 'Failed to send mail',
                        }, HttpApplicationError )
                    
                #send the admin mail that he should activate the business
                t = get_template('emails/admin_new_business_mail.html')
                html = t.render(Context({}))
                text_content = strip_tags(html)
                msg = EmailMultiAlternatives('Business approval', text_content, settings.FROM_EMAIL_ADDRESS, [settings.ADMIN_MAIL])
                msg.attach_alternative(html, "text/html")
                try:
                    msg.send()
                except SMTPSenderRefused, e:
                    pass
            
            return self.create_response(request, {
                         'success': True,
                         'message': "User created successfully",
                         }, HttpCreated)
        else:
            return self.create_response(request, {
                         'success': False,
                         'message': "Bad params passed",
                         'errors': create_form.errors
                         }, HttpBadRequest)
            
        
        
            
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