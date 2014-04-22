'''
will hold our anonymous user resource
Created on April 22, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''
#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.ltg_api.user import UserResource
from tastypie.validation import FormValidation
from ltg_backend_app.forms import AnonymousUserCreateForm
import uuid

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin anonymous user resource
#===============================================================================

class AnonymousUserResource(UserResource):
    '''
    resource for anonymous user creation
    '''
    class Meta(UserResource.Meta):
        validation = FormValidation(form_class=AnonymousUserCreateForm)
        
    def obj_create(self, bundle, **kwargs):
        # assign password to anonymous user
        bundle.data['password'] = bundle.data.get('password',uuid.uuid4().hex[:16])
        return super(AnonymousUserResource,self).obj_create(bundle,**kwargs)
    
#===============================================================================
# end anonymous user resource
#===============================================================================