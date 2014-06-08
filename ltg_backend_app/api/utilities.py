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


from tastypie.authentication import Authentication, ApiKeyAuthentication
from django.conf.urls import url
from tastypie.utils.urls import trailing_slash
from django.utils import simplejson
from django.contrib.auth import login, get_user_model, authenticate
from tastypie.http import HttpForbidden, HttpUnauthorized,\
    HttpApplicationError, HttpAccepted, HttpNotFound, HttpBadRequest
from django.template.loader import get_template
from django.template.context import Context
from django.utils.html import strip_tags
from django.core.mail.message import EmailMultiAlternatives
from smtplib import SMTPSenderRefused
from tastypie.models import ApiKey
from ltg_backend_app.api.base import LtgResource, is_send_grid
from ltg_backend_app import settings
from django.contrib.auth.models import User
import uuid
from ltg_backend_app.forms import ResetPasswordForm
from ltg_backend_app.api.user import UserResource

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
            url(r"^(?P<resource_name>%s)/forgot-password%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('forgot_password'), name="api_forgot_password"),
            url(r"^(?P<resource_name>%s)/reset-password%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('reset_password'), name="api_reset_password"),
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
         
        # try to login the user by mail and password
        user = authenticate(email=email, password=password)
        if (user):
            if user.is_active:
                login(request, user)
                # get the user api key
                api_key, created = ApiKey.objects.get_or_create(user=user)
                if (created):
                    api_key.save()
                # build user uri
                user_uri = UserResource().get_resource_uri(user)                    
                return self.create_response(request, {
                    'success': True,
                    'message':'Successfully logged in!',
                    'user': user_uri,
                    'username':user.username,
                    'api_key':user.api_key.key
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
                User = get_user_model()
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
        ApiKeyAuthentication().is_authenticated(request)

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
            
            
    def send_email(self, request=None, **kwargs):
        '''
        TODO
        '''
        pass
            
#===============================================================================
# end utilities resource
#===============================================================================
            