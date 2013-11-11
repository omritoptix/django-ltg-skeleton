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

from tastypie.resources import ModelResource, ALL
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import ApiKeyAuthentication
from ticketz_backend_app.models import *
import os
from django.template.loader import get_template
from django.template import Context
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from ticketz_backend_app import settings
from smtplib import SMTPSenderRefused

from tastypie.http import HttpAccepted, HttpApplicationError
from django.conf.urls import url
from tastypie.utils import trailing_slash
from django.utils import simplejson
from tastypie.exceptions import Unauthorized
from tastypie.http import HttpUnauthorized, HttpConflict, HttpCreated, HttpBadRequest, HttpNotFound
from django.contrib import auth
from tastypie.models import ApiKey
from django.utils import simplejson as json
from ticketz_backend_app.forms import UserCreateForm
from django.contrib.auth import authenticate, login
import random

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

class NerdeezResource(ModelResource):
    '''
    abstract class with commone attribute common to all my rest models
    '''
    
    #set read only fields
    class Meta:
        allowed_methods = ['get']
        always_return_data = True
        ordering = ['title']
        
        
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

class NerdeezApiKeyAuthentication(ApiKeyAuthentication):
    def extract_credentials(self, request):
        username, api_key = super(NerdeezApiKeyAuthentication, self).extract_credentials(request)
        if username == None and api_key == None and request.method == 'POST':
            post = simplejson.loads(request.body)
            username = post.get('username')
            api_key = post.get('api_key')
        return username, api_key
            

class NerdeezReadForFreeAuthentication(NerdeezApiKeyAuthentication):
    
    def is_authenticated(self, request, **kwargs):
        '''
        get is allowed without cradentials and all other actions require api key and username
        @return: boolean if authenticated
        '''
        if request.method == 'GET':
            return True
        return super( NerdeezReadForFreeAuthentication, self ).is_authenticated( request, **kwargs )
        
class NerdeezReadForFreeAuthorization( DjangoAuthorization ):
    '''
    Authorizes every authenticated user to perform GET, 
    it will allow post to everyone
    and put/delete if there is owner only he can do it.
    '''

    def read_list(self, object_list, bundle):
        return object_list
    
    def read_detail(self, object_list, bundle):
        return True
    
    def create_detail(self, object_list, bundle):
        return True
    
    def create_list(self, object_list, bundle):
        return object_list
        
        
    def update_detail(self, object_list, bundle):
        return len(object_list) > 0
    
    def update_list(self, object_list, bundle):
        if bundle.request == None:
            raise Unauthorized("You are not allowed to access that resource.")
        
        objects = []
        for obj in object_list:
            if hasattr(obj, 'owner') and (obj.owner() == bundle.request.user.username):
                objects.append(obj)
            if not hasattr(obj, 'owner'):
                objects.append(obj)
        return objects
    
    def delete_list(self, object_list, bundle):
        return self.update_list(object_list, bundle)
    
    def delete_detail(self, object_list, bundle):
        return self.delete_detail(object_list, bundle)
    
class NerdeezOnlyOwnerCanReadAuthorization( NerdeezReadForFreeAuthorization ):
    '''
    Authorizes every authenticated user to perform GET, for all others
    performs NerdeezReadForFreeAuthorization.
    '''
    
    def read_list(self, object_list, bundle):
        list = []
        for obj in object_list:
            if not hasattr(obj, 'owner'):
                list.append(obj)
            if hasattr(obj, 'owner') and obj.owner() == bundle.request.user.username:
                list.append(obj)
                
        return list
    
    def read_detail(self, object_list, bundle):
        return len(self.read_list(object_list, bundle)) > 0

        

#===============================================================================
# end authorization/authentication
#===============================================================================

#===============================================================================
# begin the actual rest api
#===============================================================================

class FlatpageResource(NerdeezResource):
    '''
    the rest api for the flatpage
    '''
    class Meta(NerdeezResource.Meta):
        queryset = FlatPage.objects.all()
        filtering = {
                     'title': ALL,
                     }
     
class UserProfileResource(NerdeezResource):
    class Meta(NerdeezResource.Meta):
        queryset = UserProfile.objects.all()
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezOnlyOwnerCanReadAuthorization()
        allowed_methods = ['get', 'put']
        
class RegionResource(NerdeezResource):
    class Meta(NerdeezResource.Meta):
        queryset = Region.objects.all()
        
class CityResource(NerdeezResource):
    region = fields.ToOneField(RegionResource, 'region', null=True, full=True)
    class Meta(NerdeezResource.Meta):
        queryset = City.objects.all()
        
class UserPrefrenceResource(NerdeezResource):
    user_profile = fields.ToOneField(UserProfileResource, 'user_profile', null=True, full=True)
    city = fields.ToOneField(CityResource, 'city', null=True, full=True)
    region = fields.ToOneField(RegionResource, 'region', null=True, full=True)
    class Meta(NerdeezResource.Meta):
        queryset = UserPrefrence.objects.all()
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezOnlyOwnerCanReadAuthorization()
        allowed_methods = ['get', 'put']
        
class CategoryResource(NerdeezResource):
    class Meta(NerdeezResource.Meta):
        queryset = Category.objects.all()
        
class BusinessResource(NerdeezResource):
    class Meta(NerdeezResource.Meta):
        queryset = Business.objects.all()
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezOnlyOwnerCanReadAuthorization()
        
class UtilitiesResource(NerdeezResource):
    '''
    the api for things that are not attached to models: 
    - contact us: url: /api/v1/utilities/contact/
    '''
    
    class Meta(NerdeezResource.Meta):
        allowed_methods = ['post']
      
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/contact%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('contact'), name="api_contact"),
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r"^(?P<resource_name>%s)/register%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('register'), name="api_register"),
            url(r"^(?P<resource_name>%s)/forgot-password%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('forgot_password'), name="api_forgot_password"),
        ]
        
    def contact(self, request=None, **kwargs):
        '''
        will send the message to our mail
        '''
        #get params
        post = simplejson.loads(request.body)
        message = post.get('message')
        mail = post.get('mail')
        admin_mail = settings.ADMIN_MAIL
        
        t = get_template('emails/contact_us_email.html')
        html = t.render(Context({'mail': mail, 'message': message}))
        text_content = strip_tags(html)
        msg = EmailMultiAlternatives(u'Nerdeez contact us', text_content, settings.FROM_EMAIL_ADDRESS, [admin_mail])
        msg.attach_alternative(html, "text/html")
        try:
            msg.send()
        except SMTPSenderRefused, e:
            return self.create_response(request, {
                    'success': False,
                    'message': 'Failed to send the email',
                    }, HttpApplicationError )
        
        return self.create_response(request, {
                    'success': True,
                    'message': 'Successfully sent your message',
                    }, HttpAccepted )
        
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
        
        #get the params
        post = simplejson.loads(request.body)
        password = post.get('password')
        email = post.get('email')
        
        #get the user with that email address
        try:
            user = User.objects.get(email=email)
        except:
            return self.create_response(request, {
                    'success': False,
                    'message': 'Invalid email or password',
                    }, HttpUnauthorized )
        
        user = auth.authenticate(username=user.username, password=password)
        if user is None:
            return self.create_response(request, {
                    'success': False,
                    'message': 'Invalid email or password',
                    }, HttpUnauthorized )
        if not user.is_active:
            return self.create_response(request, {
                    'success': False,
                    'message': 'Account not activated',
                    }, HttpUnauthorized )
                    
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        
        #successfull login delete all the old api key of the user and create a new one
        api_keys = ApiKey.objects.filter(user=user)
        api_keys.delete()
        api_key, created = ApiKey.objects.get_or_create(user=user)
        api_key.save()

        ur = UserProfileResource()
        ur_bundle = ur.build_bundle(obj=user.profile, request=request)
        return self.create_response(request, {
                    'success': True,
                    'message': 'Successfully logged in',
                    "user_profile": json.loads(ur.serialize(None, ur.full_dehydrate(ur_bundle), 'application/json')),
                    'api_key': api_key.key,
                    'username': user.username
                    }, HttpAccepted )
        
    def register(self, request=None, **kwargs):
        '''
        will try and register the user
        we expect here an email and a password sent as post params
        @return:    201 if user is created
                    500 failed to send emails
                    409 conflict with existing account
        '''
        
        #get params
        post = simplejson.loads(request.body)
        email = post.get('email')
        business_id = post.get('business_id')
        phone = post.get('phone')
        address = post.get('address')
        city = post.get('city')
        title = post.get('title')
        
        #create the username
        api_key = ApiKey()
        username = api_key.generate_key()[0:30]
        password = api_key.generate_key()[0:30]
        
        #set the request post to contain email password and username
        post_values = {}
        post_values['username'] = username
        post_values['password1'] = password
        post_values['password2'] = password
        post_values['email'] = email
        
        #is the email already exists?
        try:
            user = User.objects.get(email=email)
            return self.create_response(request, {
                    'success': False,
                    'message': 'User with this mail address already exists',
                    }, HttpConflict )
        except:
            pass
        
        #validation success
        user_form = UserCreateForm(post_values)
        if user_form.is_valid():
            
            #create the user
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username,
                                password=password)
            login(request, user)
            user.is_active = False
            user.save()
            
            #create the business 
            business = Business()
            business.title = title
            business.business_id = business_id
            business.phone = phone
            if city != None:
                business.city = City.objects.get(id=city)
            business.address = address
            business.user_profile = user.profile
            business.save()
            
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
            
            #return the status code
            return self.create_response(request, {
                    'success': True,
                    'message': 'Successfully created the account, Account pending approval',
                    }, HttpCreated )
            
        #validation failed    
        else:
            return self.create_response(request, {
                    'success': False,
                    'message': [(k, v[0]) for k, v in user_form.errors.items()],
                    }, HttpBadRequest )
            
    def forgot_password(self, request=None, **kwargs):
        '''
        api for the user to create a new password
        return 200 on success
        return 401 on unuthorized (account not activated)
        return 404 on account not found
        return 500 if failed to send mail
        '''
        post = simplejson.loads(request.body)
        email = post.get('email')
        
        #get the profile for that mail
        try:
            user = User.objects.get(email=email)
            user_profile = user.profile
        except:
            return self.create_response(request, {
                    'success': False,
                    'message': "Account with that mail doesn't exist",
                    }, HttpNotFound)
        
        #if the user is not activated by admin yet
        if not user.is_active:
            return self.create_response(request, {
                    'success': False,
                    'message': "Account not activated",
                    }, HttpUnauthorized)
            
        #set the new password
        api_key = ApiKey()
        pass_length = random.randint(8, 15)
        password = api_key.generate_key()[0:pass_length]
        user.set_password(password)
        user.save()
        
        #semd mail to the business about the account activation
        if is_send_grid():
            t = get_template('emails/confirm_approve_business.html')
            html = t.render(Context({'admin_mail': settings.ADMIN_MAIL, 'admin_phone': settings.ADMIN_PHONE, 'provider_url': settings.PROVIDER_URL, 'password': password}))
            text_content = strip_tags(html)
            msg = EmailMultiAlternatives('2Nite Registration', text_content, settings.FROM_EMAIL_ADDRESS, [user.email])
            msg.attach_alternative(html, "text/html")
            try:
                msg.send()
            except SMTPSenderRefused, e:
                return self.create_response(request, {
                    'success': False,
                    'message': "Failed to send the mail",
                    }, HttpApplicationError)
        
        #success
        return self.create_response(request, {
                    'success': True,
                    'message': "Your new password was sent to your mail",
                    }, HttpAccepted)
            
        
                    
#===============================================================================
# end teh actual rest api
#===============================================================================