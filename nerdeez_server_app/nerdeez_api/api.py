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
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authentication import Authentication,ApiKeyAuthentication
from nerdeez_server_app.models import *
from django.contrib.auth.models import User
import os
from django.template.loader import get_template
from django.template import Context
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from nerdeez_server_app import settings
from smtplib import SMTPSenderRefused
from tastypie import http
from tastypie.exceptions import ImmediateHttpResponse
from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpAccepted,\
    HttpCreated, HttpApplicationError, HttpBadRequest,HttpConflict, HttpNotFound
from django.conf.urls import url
from tastypie.utils import trailing_slash
from django.utils import simplejson
from django.contrib import auth
from tastypie.models import ApiKey
from nerdeez_server_app.forms import *
from django.utils import simplejson as json
import base64, hmac, hashlib
from nerdeez_server_app import settings
from django_facebook.connect import connect_user
import fb
from twython import Twython
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
from tastypie.constants import ALL_WITH_RELATIONS
from django.core.urlresolvers import resolve, get_script_prefix
import nerdeez_server_app
from tastypie.exceptions import Unauthorized

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
#         authentication = Authentication()
#         authorization = Authorization()
        ordering = ['title']
        excludes = ['search_index']
        
    def obj_update(self, bundle, skip_errors=False, **kwargs):
        '''
        deal with likes and dislikes
        '''
        
        if 'like' in bundle.data:
            bundle.data['like'] = bundle.obj.like + 1
        if 'dislike' in bundle.data:
            bundle.data['dislike'] = bundle.obj.dislike + 1
            
        return super(NerdeezResource, self).obj_update(bundle, skip_errors=skip_errors, **kwargs)
        
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

def fb_request_decode(signed_request):
    '''
    will get the data from a facebook signed request
    @param signed_request: 
    @return: Object the decoded data 
    '''
    
    fb_app_secret = settings.FACEBOOK_APP_SECRET
    s = [s.encode('ascii') for s in signed_request.split('.')]

    fb_sig = base64.urlsafe_b64decode(s[0] + '=')
    fb_data = json.loads(base64.urlsafe_b64decode(s[1]))
    fb_hash = hmac.new(fb_app_secret, s[1], hashlib.sha256).digest()

    sig_match = False
    if fb_sig == fb_hash:
        sig_match = True

    auth = False
    if 'user_id' in fb_data:
        auth = True

    return {
        'fb_sig' : fb_sig,
        'fb_data' : fb_data,
        'fb_hash' : fb_hash,
        'sig_match' : sig_match,
        'auth' : auth,
    }
    

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
            if hasattr(obj, 'owner') and obj.owner() == bundle.request.user:
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

class SchoolGroupResource(NerdeezResource):
    '''
    resource for school groups like university, faculty, search
    '''
    
    parent =  fields.ToOneField('self', 'parent', full=True, null=True)
    hws = fields.ToManyField('nerdeez_server_app.nerdeez_api.api.HwResource', 'hws', full=True, null=True)
    class Meta(NerdeezResource.Meta):
        allowed_methods = ['get', 'post', 'put']
        queryset = SchoolGroup.objects.all()
        filtering = {
                     'school_type': ['exact'],
                     'parent': ALL_WITH_RELATIONS,
                     'id': ['exact']
                     }
        ordering = ['grade', 'title']
        authentication = NerdeezReadForFreeAuthentication()
        authorization = NerdeezReadForFreeAuthorization()
        
    def get_object_list(self, request):
        '''
        search group logic
        '''
        ids = []
        if request.GET.get('search') != None:
            return self.Meta.object_class.search(request.GET.get('search'))
        else:
            return super(SchoolGroupResource, self).get_object_list(request)       
        
        
class FlatpageResource(NerdeezResource):
    '''
    the rest api for the flatpage
    '''
    class Meta(NerdeezResource.Meta):
        queryset = Flatpage.objects.all()
        filtering = {
                     'title': ALL,
                     }
     
class UserProfileResource(NerdeezResource):
#     school_groups = fields.ToManyField(SchoolGroupResource, 'school_groups', full=True)
    enrolls = fields.ToManyField('nerdeez_server_app.nerdeez_api.api.EnrollResource', 'enrolls', full=True)
    
    class Meta(NerdeezResource.Meta):
        queryset = UserProfile.objects.all()
        excludes = ['email_hash', 'twitter_oauth_token', 'twitter_oauth_token_secret']
        ordering = ['enrolls']
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezOnlyOwnerCanReadAuthorization()
        
        
class EnrollResource(NerdeezResource):
    user = fields.ToOneField(UserProfileResource, 'user')
    school_group = fields.ToOneField(SchoolGroupResource, 'school_group', full=True, null=True)
    class Meta(NerdeezResource.Meta):
        queryset = Enroll.objects.all()
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezOnlyOwnerCanReadAuthorization()
        allowed_methods = ['post', 'get']
        
    def obj_create(self, bundle, **kwargs):
        '''
        if the enrollment exist then modify the last entered
        else then create a new enrollment
        '''
        bundle.data['user'] = API_URL + 'userprofile/' + str(bundle.request.user.profile.id) + '/'
        schoolgroup_id = get_pk_from_uri(bundle.data['school_group'])
        try:
            enroll = Enroll.objects.get(user=bundle.request.user.profile,school_group__id=schoolgroup_id)
        except:
            return super(EnrollResource, self).obj_create(bundle, **kwargs)
        enroll.last_entered = datetime.datetime.now().replace(microsecond=0)
        enroll.save()
        bundle.obj = enroll
        return bundle
    
class HwResource(NerdeezResource):
    school_group = fields.ToOneField(SchoolGroupResource, 'school_group')
    files = fields.ToManyField('nerdeez_server_app.nerdeez_api.api.FileResource', 'files', full=True, null=True)
    
    class Meta(NerdeezResource.Meta):
        queryset = Hw.objects.all()
        allowed_methods = ['post', 'get', 'put']
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezReadForFreeAuthorization()
        
        
class FileResource(NerdeezResource):
    hw = fields.ToOneField(HwResource, 'hw', null=True)
    
    class Meta(NerdeezResource.Meta):
        queryset = File.objects.all()
        allowed_methods = ['post', 'get', 'put']
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezReadForFreeAuthorization()
            
        
        
    
        
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
            url(r"^(?P<resource_name>%s)/verify-email%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('verify_email'), name="api_verify_email"),
            url(r"^(?P<resource_name>%s)/is-login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('is_login'), name="api_is_login"),
            url(r"^(?P<resource_name>%s)/logout%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name="api_logout"),
            url(r"^(?P<resource_name>%s)/fb-login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('fb_login'), name="api_fb_login"),
            url(r"^(?P<resource_name>%s)/twitter-login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('twitter_login'), name="api_twitter_login"),
            url(r"^(?P<resource_name>%s)/twitter-login-callback%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('twitter_login_callback'), name="api_twitter_login_callback"),
            url(r"^(?P<resource_name>%s)/change-password%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('change_password'), name="api_change_password"),
            url(r"^(?P<resource_name>%s)/forget-password%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('forget_password'), name="api_forget_password"),
            url(r"^(?P<resource_name>%s)/reset-password%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('reset_password'), name="api_reset_password"),
        ]
        
    def contact(self, request=None, **kwargs):
        '''
        will send the message to our mail
        '''
        #get params
        post = simplejson.loads(request.body)
        message = post.get('message')
        mail = post.get('mail')
        admin_mail = os.environ['ADMIN_MAIL']
        
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
        @return: 401 if login failed with a disctionary with a message, or 200 with the api key and password
        '''
        
        #get the params
        post = simplejson.loads(request.body)
        password = post.get('password')
        email = post.get('email')
        remember_me = post.get('remember_me')
        
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

        #if the user set the remeber me then the sessions should expire in 1 week
#         if remember_me:
#             request.session.set_expiry(60*60*24*7)
#         else:
#             request.session.set_expiry(60*60*24)
                
        #store cradentials in session
#         request.session['api_key'] = api_key.key
#         request.session['username'] = user.username
        
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
        password = post.get('password')
        email = post.get('email')
        
        #create the username
        api_key = ApiKey()
        username = api_key.generate_key()[0:30]
        
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
            
            #creathe the email hash
            email_hash = api_key.generate_key()
            user_profile = user.profile
            user_profile.email_hash = email_hash
            user_profile.save()
            
            #send the verification mail
            if is_send_grid():
                user.is_active = False
                user.save()
                t = get_template('emails/verify_email_mail.html')
                html = t.render(Context({'hash': user_profile.email_hash, 'url': os.environ['CLIENT_SITE_URL'] + '#/verify-email/', 'email': email}))
                text_content = strip_tags(html)
                msg = EmailMultiAlternatives('Nerdeez account activation', text_content, settings.FROM_EMAIL_ADDRESS, [email])
                msg.attach_alternative(html, "text/html")
                try:
                    msg.send()
                except SMTPSenderRefused, e:
                    return self.create_response(request, {
                        'success': False,
                        'message': 'Failed to send activation mail',
                        }, HttpApplicationError )
            
            #return the status code
            return self.create_response(request, {
                    'success': True,
                    'message': 'Successfully created the account, Verification mail was sent to your mail address',
                    }, HttpCreated )
            
        #validation failed    
        else:
            return self.create_response(request, {
                    'success': False,
                    'message': [(k, v[0]) for k, v in user_form.errors.items()],
                    }, HttpBadRequest )
                    
    def verify_email(self, request=None, **kwargs):
        '''
        verify the email hash and mark the user as active will get as post the following params
        @param: email
        @param: hash
        @returns: 400 if this is a bad request, or 200 for success
        '''
        
        #get the params
        post = simplejson.loads(request.body)
        hash = post.get('hash')
        email = post.get('email')
        
        #find the user with this email address
        try:
            user = User.objects.get(email=email)
        except:
            return self.create_response(request, {
                    'success': False,
                    'message': 'Email verification failed',
                    }, HttpBadRequest )
        
        #check that the hash match
        user_profile = user.profile
        if user_profile.email_hash == hash:
            user.is_active = True
            user.save()
            return self.create_response(request, {
                    'success': True,
                    'message': 'Account is now activated',
                    })
        else:
            return self.create_response(request, {
                    'success': False,
                    'message': 'Email verification failed',
                    }, HttpBadRequest )
            
        
    def fb_login(self, request=None, **kwargs):
        '''
        will login the user using facebook
        '''
        
        #get the params
        post = simplejson.loads(request.body)
        access_token = post.get('access_token')
        signed_request = post.get('signed_request')
        
        #get the email of the user
        fb_decode = fb_request_decode(signed_request)
        fb_user_id = fb_decode['fb_data']['user_id']
        facebook=fb.graph.api(access_token)
        object=facebook.get_object(cat="single", id=fb_user_id, fields=[ ] )
        email = object['email']
        
        #find the user
        try:
            user = User.objects.get(email=email)
        except:
            #create the user object
            api_key = ApiKey()
            username = api_key.generate_key()[0:30]
            password = api_key.generate_key()[0:30]
            user = User()
            user.username = username
            user.email = email
            user.is_active = True
            user.password = password
            user.save()
            
        #delete all the old api keys
        api_keys = ApiKey.objects.filter(user=user)
        api_keys.delete()
        
        #create a new api key
        api_key, created = ApiKey.objects.get_or_create(user=user)
        api_key.save()
        
        ur = UserProfileResource()
        ur_bundle = ur.build_bundle(obj=user.profile, request=request)
        return self.create_response(request, {
                    'is_logged_in': True,
                    'message': 'The user is logged in',
                    'api_key': api_key.key,
                    'username': user.username,
                    'user_profile': json.loads(ur.serialize(None, ur.full_dehydrate(ur_bundle), 'application/json'))
                    })
        
    def twitter_login(self, request=None, **kwargs):
        '''
        used to login the user via twitter 
        '''
        twitter = Twython(settings.TWITTER_KEY, settings.TWITTER_SECRET)
        auth = twitter.get_authentication_tokens(callback_url=os.environ.get('CLIENT_SITE_URL', 'http://nerdeez.com/#/login/') )
        request.session['OAUTH_TOKEN'] = auth['oauth_token']
        request.session['OAUTH_TOKEN_SECRET'] = auth['oauth_token_secret']
        return self.create_response(request, {
                    'auth_url': auth['auth_url'],
                    'message': 'waiting for the user to authorize',
                    })
        
    def twitter_login_callback(self, request=None, **kwargs):
        '''
        when we have the oauth verifier then send it through this api
        '''
        
        #get the params twitter need
        post = simplejson.loads(request.body)
        twitter_key = settings.TWITTER_KEY
        twitter_secret = settings.TWITTER_SECRET
        oauth_token = request.session.get('OAUTH_TOKEN', '')
        oauth_token_secret = request.session.get('OAUTH_TOKEN_SECRET', '')
        oauth_verifier = post.get('oauth_verifier', '')
        
        #get the params from the login
        twitter = Twython(twitter_key, twitter_secret,oauth_token, oauth_token_secret)
        final_step = twitter.get_authorized_tokens(oauth_verifier)
        user_oauth_token = final_step['oauth_token']
        user_oauth_token_secret = final_step['oauth_token_secret']
        
        #find existing user or create a new one
        try:
            userprofile = UserProfile.objects.get(twitter_oauth_token=user_oauth_token, twitter_oauth_token_secret=user_oauth_token_secret)
            user = userprofile.user
        except:
            #create a user and user profile
            api_key = ApiKey()
            username = api_key.generate_key()[0:30]
            password = api_key.generate_key()[0:30]
            user = User()
            user.username = username
            user.is_active = True
            user.password = password
            user.save()
            userprofile = user.profile
            userprofile.twitter_oauth_token = user_oauth_token
            userprofile.twitter_oauth_token_secret = user_oauth_token_secret
            userprofile.save()
            
        #delete all the old api keys
        api_keys = ApiKey.objects.filter(user=user)
        api_keys.delete()
        
        #create a new api key
        api_key, created = ApiKey.objects.get_or_create(user=user)
        api_key.save()
        
        #store the keys in the session
        request.session['api_key'] = api_key.key
        request.session['username'] = user.username
        
        ur = UserProfileResource()
        ur_bundle = ur.build_bundle(obj=user.profile, request=request)
        return self.create_response(request, {
                    'is_logged_in': True,
                    'message': 'The user is logged in',
                    'username': user.username,
                    'api_key': api_key.key,
                    'user_profile': json.loads(ur.serialize(None, ur.full_dehydrate(ur_bundle), 'application/json'))
                    })
        
    def change_password(self, request=None, **kwargs):
        '''
        change the password of the user
        @param old_password: will get this as post param
        @param new_password: will get this as post param
        @return: 401 if unauth or 200 if success  
        '''
        
        #check auth
        if not NerdeezAuthentication().is_authenticated(request):
            return self.create_response(request, {
                    'success': False,
                    'message': 'You are not authorized to do this',
                    }, HttpUnauthorized)
            
        #get the params
        post = simplejson.loads(request.body)
        old_password = post.get('old_password')
        new_password = post.get('new_password')
        
        #check that the old password match
        user = auth.authenticate(username=request.session.get('username'), password=old_password)
        if user is None:
            return self.create_response(request, {
                    'success': False,
                    'message': "Old password doesn't match",
                    }, HttpUnauthorized)
        
        #set the new password and return success    
        user.set_password(new_password)
        user.save()
        return self.create_response(request, {
                    'success': True,
                    'message': "Successfully changed the password.",
                    })
        
    def forget_password(self, request=None, **kwargs):
        '''
        api for the user when he forgets his password
        @param email
        @return: 404 if account not found, 200 if all is goot
        '''
        
        #get the params
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
            
        # Delete all old forgot password entries
        ForgotPass.objects.filter(user=user_profile).delete()
        
        #create a new hash key and save the hash
        forgot_pass = ForgotPass(user=user_profile)
        forgot_pass.save()
        hash = forgot_pass.hash
        
        #send mail to the user
        if is_send_grid():
            t = get_template('emails/forgot_password_email.html')
            html = t.render(Context({'hash': hash , 'url': os.environ['CLIENT_SITE_URL'] + '#/reset-password/', 'email': email}))
            text_content = strip_tags(html)
            msg = EmailMultiAlternatives('Nerdeez - Reset password', text_content, settings.FROM_EMAIL_ADDRESS, [email])
            msg.attach_alternative(html, "text/html")
            try:
                msg.send()
            except SMTPSenderRefused, e:
                return self.create_response(request, {
                        'success': False,
                        'message': 'Failed to send mail',
                        }, HttpApplicationError )
            return self.create_response(request, {
                        'success': True,
                        'message': 'Sent mail to reset your password',
                        })
        else:
            return self.create_response(request, {
                        'success': False,
                        'message': "Unable to send emails",
                        }, HttpApplicationError )
            
    def reset_password(self, request=None, **kwargs):
        '''
        after the user tell that he forgot a password he will be prompt
        with a new place to set a new password, and it will call this api
        @param email
        @param password
        @param hash
        @return 200 - success 401 on bad hash 404 on user not found
        '''
        
        #get the params
        post = simplejson.loads(request.body)
        email = post.get('email')
        password = post.get('password')
        hash = post.get('hash')
        
        #check if the hash exists
        try:
            hash_object = ForgotPass.objects.get(hash=hash)
        except ObjectDoesNotExist:
            return self.create_response(request, {
                    'success': False,
                    'message': "Didn't find the change password request",
                    }, HttpNotFound )
            
        #check if the hash is still valid
        creation_date = hash_object.creation_date.replace(tzinfo=None)
        now = datetime.datetime.now().replace(microsecond=0)
        minus_day = (now - timedelta(days=1))
        if minus_day > creation_date:
            return self.create_response(request, {
                    'success': False,
                    'message': "Change password request is older than 24 hours",
                    }, HttpBadRequest )
            
        # Delete old password link
        hash_object.delete()
        
        #grab the user and change the password and pass success
        user = User.objects.get(id=hash_object.user.user_id)
        if user.email == email:
            user.set_password(password)
            user.save()
            return self.create_response(request, {
                    'success': True,
                    'message': "Successfully changed the password",
                    } )
        else:
            return self.create_response(request, {
                    'success': False,
                    'message': "Email address don't match",
                    }, HttpNotFound ) 
            
            
        
#===============================================================================
# end teh actual rest api
#===============================================================================