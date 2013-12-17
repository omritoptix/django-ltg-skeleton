'''
will hold custom decorators 

Created on Dec 16, 2013
@author: omri
@version : 1.0
@company : Nerdeez.com
'''
#===============================================================================
# begin imports
#===============================================================================

from tastypie.authentication import ApiKeyAuthentication
from django.http import HttpResponse
from django.utils.unittest.compatibility import wraps

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin custom decorators
#===============================================================================

    
def business_auth_required(func):
    '''
    will make sure the user trying
    to access if of type business profile 
    '''
    @wraps(func) 
    def check_authorized(request, *args, **kwargs):
         
#       check if the user is authorized to view this page
        auth = ApiKeyAuthentication()
        if auth.is_authenticated(request) != True:
            return HttpResponse('Unauthorized', status=401)
        user = request.user
        user_profile = user.get_profile()
        
        #check that it has a business profile, and that it's not a phone profile 
        #if not - return unauthorized
        if not user_profile.business_profile.all().exists():
            return HttpResponse('Unauthorized', status=401)
        
        return func(request, *args, **kwargs)
    
    return check_authorized

#===============================================================================
# end custom decorators
#===============================================================================