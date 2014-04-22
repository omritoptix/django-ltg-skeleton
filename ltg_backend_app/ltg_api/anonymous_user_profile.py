'''
will hold our anonymous user profile resource
Created on April 22, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from ltg_backend_app.ltg_api.user_profile import UserProfileResource
from tastypie.validation import FormValidation
from ltg_backend_app.forms import AnonymousUserProfileForm

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin anonymous user profile resource
#===============================================================================

class AnonymousUserProfileResource(UserProfileResource):
    '''
    resource for anonymous user profile creation
    '''  
    class Meta(UserProfileResource.Meta):
        validation = FormValidation(form_class=AnonymousUserProfileForm)
        
    def hydrate(self,bundle):
        bundle.obj.is_anonymous = True
        return super(AnonymousUserProfileResource,self).hydrate(bundle)
    
#===============================================================================
# end anonymous user profile resource
#===============================================================================