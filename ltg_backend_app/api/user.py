'''
will hold our user resource
Created on April 22, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from tastypie.validation import FormValidation
from tastypie.authentication import Authentication, ApiKeyAuthentication
from ltg_backend_app.forms import UserForm
from tastypie.resources import ModelResource
from ltg_backend_app.models import LtgUser
from tastypie import fields
from ltg_backend_app.api.authorization import UserAuthorization
from tastypie.models import ApiKey
from ltg_backend_app import settings
from tastypie.utils.urls import trailing_slash
from django.conf.urls import url
from tastypie.http import HttpUnauthorized
from tastypie.exceptions import ImmediateHttpResponse
import datetime
from django.utils.timezone import utc
import time

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin user resource
#===============================================================================

class UserResource(ModelResource):
    '''
    resource for our user model
    '''   
    username = fields.CharField(readonly=True,attribute='username')
    
    class Meta:
        resource_name = 'user'
        allowed_methods = ['get','post','put','patch']
        detail_allowed_methods = ['get', 'post', 'put', 'patch']
        include_resource_uri = True
        always_return_data = True
        validation = FormValidation(form_class=UserForm)
        authentication = Authentication()
        authorization = UserAuthorization()
        queryset = LtgUser.objects.all()
        excludes = ['password','is_superuser','is_staff','is_active','date_joined','last_login']
    

    def obj_create(self, bundle , **kwargs):
        # create the object 
        bundle = super(UserResource, self).obj_create(bundle)
        # set the new password
        bundle.obj.set_password(bundle.data['password'])
        bundle.obj.save()
        # create api key for the user
        api_key = ApiKey.objects.get_or_create(user=bundle.obj)[0]
        api_key.key = api_key.generate_key()
        api_key.save()
        
        return bundle
    
    def obj_update(self, bundle, **kwargs):
        # email is not allowed to be updated
        if ('email' in bundle.data):
            del bundle.data['email'] 
        bundle = super(UserResource, self).obj_update(bundle)
        
        return bundle
    
    def dehydrate(self,bundle):
        # add the api key and username
        bundle = super(UserResource,self).dehydrate(bundle)
        bundle.data['api_key'] = bundle.obj.api_key.key
        
        return bundle
    
#===============================================================================
# end user resource
#===============================================================================