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
                    
#===============================================================================
# end teh actual rest api
#===============================================================================