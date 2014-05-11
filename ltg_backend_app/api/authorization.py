'''
will hold our authorization for the api
Created on April 22, 2014
 
@author: Omri Dagan & Yariv Katz
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin authorization
#===============================================================================
    
class UserObjectsOnlyAuthorization(Authorization):
    '''
    assumes the resource using this auth has a 'user_profile'/'user' as fk.
    allow POST/GET/PUT per user profile.
    deny DELETE.
    '''
    def _get_user(self, obj):
        '''
        will get the user of the object
        @param obj: django model
        @return: a user model
        '''
        if hasattr(obj,'user_profile_id'):
            return obj.user_profile.user
        if hasattr(obj,'user_id'):
            return obj.user
        else:
            raise Unauthorized("The resource can't use this authorization class since it does not have user/user_profile attributes.")
    
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        if hasattr(bundle.obj,'user_profile_id'):
            return object_list.filter(user_profile__user=bundle.request.user)
        else:
            return object_list.filter(user=bundle.request.user)
        
    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        user = self._get_user(bundle.obj)
        return user == bundle.request.user.profile

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            user = self._get_user(bundle.obj)
            if user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        user = self._get_user(bundle.obj)
        return user == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")
    
#===============================================================================
# end authorization
#===============================================================================