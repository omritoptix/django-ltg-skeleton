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
from ltg_backend_app.models import LtgUser, UserScore
from tastypie import fields
from ltg_backend_app.api.authorization import UserAuthorization
from tastypie.models import ApiKey
from ltg_backend_app.tasks import create_hubspot_contact, update_hubspot_contact
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
    num_of_sessions = fields.IntegerField(readonly=True,attribute='num_of_sessions')
    hubspot_contact_id = fields.IntegerField(readonly=True,attribute='hubspot_contact_id',null=True)
    
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
        excludes = ['password','is_superuser','is_staff','is_active','date_joined','last_login','uuid']
        
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/start-session%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('start_session'), name="api_start_session"),
        ]
    

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
        # create the user in hubspot
        properties = {'email','first_name','last_name','language'}
        create_hubspot_contact.delay(bundle.obj,settings.HUBSPOT_USERS_LIST_ID, *properties)
        
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
    
    def start_session(self, request, **kwargs):
        """
        Indication that a user has started a new session.
        will increment the current user session number, update last login details,
        and update hubspot contact.
        """
        # authenticate the user
        self.method_check(request, allowed=['post'])
        ApiKeyAuthentication().is_authenticated(request)
        if not request.user.is_authenticated():
            raise ImmediateHttpResponse(HttpUnauthorized("Operation not allowed for anonymous user."))
        
        # update last logged in
        user = request.user
        user.last_login = datetime.datetime.now().replace(microsecond=0,tzinfo=utc)
        # increment user session
        user.increment_session()
        user.save()
        # update hubspot contact 
        if user.hubspot_contact_id is not None:
            properties = {'num_of_sessions'}
            # convert last login to unix timestamp at midnight , to match hubspot conventions
            extra_properties = {'last_login':int(time.mktime(user.last_login.replace(second=0,minute=0,hour=0).timetuple())*1000)}
            # check if user has test date and if so add it to properties
            if user.test_date is not None:
                test_date = {'test_date':int(time.mktime(user.test_date.replace(second=0,minute=0,hour=0).timetuple())*1000)}
                extra_properties.update(test_date)
            # check if user has score and if so add it to properties            
            try:
                user_score = {'user_score':user.userscore_set.latest('creation_date').score}
                extra_properties.update(user_score) 
            except UserScore.DoesNotExist:
                pass
            
            update_hubspot_contact.delay(user, *properties,**extra_properties)
        
        return self.create_response(request, {'message': 'session started successfully',},)
        
    
#===============================================================================
# end user resource
#===============================================================================