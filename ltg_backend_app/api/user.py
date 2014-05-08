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
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from django.contrib.auth.models import User
import uuid
from ltg_backend_app.forms import UserForm
from tastypie.resources import ModelResource

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
    class Meta:
        resource_name = 'user'
        excludes = ['password']
        allowed_methods = []
        include_resource_uri = False
        always_return_data = True
        validation = FormValidation(form_class=UserForm)
        authentication = Authentication()
        authorization = Authorization()
        queryset = User.objects.all()

    def obj_create(self, bundle , **kwargs):
        # set username
        bundle.data['username'] = uuid.uuid4().hex[:30]
        # create the object 
        bundle = super(UserResource, self).obj_create(bundle)
        # set the new password
        bundle.obj.set_password(bundle.data['password'])
        bundle.obj.save()
        return bundle
    
    def obj_update(self, bundle, **kwargs):
        # get the username
        bundle.data['username'] = bundle.obj.username
        # update the object 
        bundle = super(UserResource, self).obj_update(bundle)
        # set the new password
        bundle.obj.set_password(bundle.data['password'])
        bundle.obj.save()
        return bundle
    
#===============================================================================
# end user resource
#===============================================================================