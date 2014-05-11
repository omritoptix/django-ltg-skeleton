'''
will hold our utilities resource
Created on April 22, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================


from tastypie.authentication import Authentication
from django.conf.urls import url
from tastypie.utils.urls import trailing_slash
from django.utils import simplejson
from django.contrib.auth import authenticate, login
from tastypie.http import HttpForbidden, HttpUnauthorized, HttpCreated,\
    HttpApplicationError, HttpAccepted, HttpNotFound, HttpBadRequest
from ltg_backend_app.models import UserProfile
from ltg_backend_app.api.user import UserResource
from ltg_backend_app.api.authentication import LtgApiKeyAuthentication
from django.template.loader import get_template
from django.template.context import Context
from django.utils.html import strip_tags
from django.core.mail.message import EmailMultiAlternatives
from smtplib import SMTPSenderRefused
from tastypie.models import ApiKey
from ltg_backend_app.api.user_profile import UserProfileResource
from ltg_backend_app.api.anonymous_user import AnonymousUserResource
from ltg_backend_app.api.anonymous_user_profile import AnonymousUserProfileResource
from ltg_backend_app.api.base import LtgResource, is_send_grid
from ltg_backend_app import settings
from django.contrib.auth.models import User
import uuid
from ltg_backend_app.forms import ResetPasswordForm

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin utilities resource
#===============================================================================

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
            url(r"^(?P<resource_name>%s)/reset-password%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('reset_password'), name="api_reset_password"),
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
        
        # try to login the user using it's mail using our custom backend 'authenticate'
        user = authenticate(username=email, password=password)
        if (user):
            if user.is_active and not user.profile.is_anonymous:
                login(request, user)
                # get the user api key
                api_key, created = ApiKey.objects.get_or_create(user=user)
                if (created):
                    api_key.save()
                # build user profile uri
                user_profile_uri = UserProfileResource().get_resource_uri(user.profile)                    
                return self.create_response(request, {
                    'success': True,
                    'message':'Successfully logged in!',
                    'user_profile': user_profile_uri,
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
        @return success: will return a 201 code with the following object.
        {
            success: <Boolean>,
            message: <String>,
            user_profile:<String>,
            username:<String>,
            api_key:<String>
        } 
        '''       
        # get params
        post = simplejson.loads(request.body)
        try:
            # check if user is already registered
            user_profile = UserProfile.objects.get(uuid = post.get('uuid'),is_anonymous=True)
            # build user profile uri
            user_profile_uri = UserProfileResource().get_resource_uri(user_profile)  
            return self.create_response(request, {
                 'success': True,
                 'message': "User created successfully",
                 'user_profile':user_profile_uri,
                 'username':user_profile.user.username,
                 'api_key':user_profile.user.api_key.key,
                 },)  
            
        except UserProfile.DoesNotExist:
            # register the user
            return self.register(request,user_resource = AnonymousUserResource(), user_profile_resource = AnonymousUserProfileResource()) 
                 

    def register(self, request=None, user_resource = UserResource(), user_profile_resource = UserProfileResource(), **kwargs):
        '''
        will try and register the user.
        if the user was previously registered as anonymous user, will update it's user and user profile details.
        @param user_resource : the resource which we will use to create the user (either UserResource or AnonymnousUserResource)
        @param user_profile_resource : the resource which we will use to create the user profile (either UserProfileResource or AnonymnousProfileUserResource) 
        @return success: will return a 201 code with the following object.
        {
            success: <Boolean>,
            message: <String>,
            user_profile:<String>,
            username:<String>,
            api_key:<String>
        } 
        '''
        new_user = True
        # get params
        post = simplejson.loads(request.body)      
        # if uuid exist - update the new user flag
        try:
            existing_user = UserProfile.objects.get(uuid=post.get('uuid',None)).user
            new_user = False
        except UserProfile.DoesNotExist:
            pass
        # create/update user from user resource
        if (new_user):
            user = user_resource.obj_create(user_resource.build_bundle(data=post))
        else:
            user = user_resource.obj_update(user_resource.build_bundle(obj=existing_user,data=post))
        try:           
            # update the post dict with the user we've just created/updated
            post['user'] = user_resource.get_resource_uri(user)
            # create/update user profile from user resource
            if (new_user):
                user_profile = user_profile_resource.obj_create(user_profile_resource.build_bundle(data=post))
            else:
                user_profile = user_profile_resource.obj_update(user_profile_resource.build_bundle(obj=existing_user.profile,data=post))
            
        except Exception as e:
            user.obj.delete()
            raise e
                    
        # build user profile uri
        user_profile_uri = UserProfileResource().get_resource_uri(user_profile)
        return self.create_response(request, {
                     'success': True,
                     'message': "User created successfully",
                     'user_profile' : user_profile_uri,
                     'username':user.obj.username,
                     'api_key':user.obj.api_key.key,
                     }, HttpCreated)            
        
    def forgot_password(self, request=None, **kwargs):
        '''
        api for the user to create a new password.
        the user will be sent with new temp passsword to his email address.
        @param email: the email address of the user 
        @return:
            200 on success
            401 on unuthorized (account not activated)
            404 on account not found
            500 if failed to send mail
        '''
        #get the post params
        post = simplejson.loads(request.body)
        email = post.get('email')
        
        if (email):
            # make sure the email is an email of user in our system
            user = None
            try:
                user = User.objects.get(email=email, is_active = True)
            except User.DoesNotExist:
                return self.create_response(request, {
                    'success': False,
                    'message': 'Account not found or not active',
                    }, HttpNotFound )
                
            #send the mail with the new password
            if is_send_grid():
                # generate new password and set it to the user
                new_password = uuid.uuid4().hex[0:8]
                user.set_password(new_password)
                user.save()
                first_name = user.first_name.capitalize()
                # send the mail
                t = get_template('emails/forgot_password.html')
                html = t.render(Context({'new_password':new_password, 'first_name':first_name}))
                text_content = strip_tags(html)
                msg = EmailMultiAlternatives('Prep4GMAT - Forgot Password', text_content, settings.ADMIN_MAIL, [email])
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
                    'message': 'Mail was successfully sent',
                    }, HttpAccepted )
            
            else:
                return self.create_response(request, {
                    'success': False,
                    'message': 'Mail server not defined',
                    }, HttpApplicationError )
            
        else:
            return self.create_response(request, {
                    'success': False,
                    'message': 'You must pass an email address',
                    }, HttpBadRequest )

    def reset_password(self,request=None, **kwargs):
        '''
        api for the user to reset his current password.
        user credentails (username,api_key) need to be passed in request.
        @param password: the new passowrd to update
        @return:
            200 on success
            401 on user unauthorized
        '''  
        #get the post params
        post = simplejson.loads(request.body)
        password = post.get('password')
        
        #authenticate the user
        LtgApiKeyAuthentication().is_authenticated(request)

        # if user is anonymous reply with unauthorized        
        if (request.user.is_anonymous()):
            return self.create_response(request, {
                    'success': False,
                    'message': 'You are not authorized for this action',
                    }, HttpUnauthorized )
            
        # set the new password for the user
        if (password):
            # check password is valid
            reset_password_form = ResetPasswordForm(post)
            if (reset_password_form.is_valid()): 
                # set the password
                request.user.set_password(password)
                request.user.save()         
                return self.create_response(request, {
                        'success': True,
                        'message': 'New password successfully set!',
                        }, )
            else:
                return self.create_response(request, {
                        'success': False,
                        'message': reset_password_form.errors,
                        }, HttpBadRequest )
        else:
            return self.create_response(request, {
                    'success': False,
                    'message': 'You must specify a new password',
                    }, HttpBadRequest )
            
        
        
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
# end utilities resource
#===============================================================================
            