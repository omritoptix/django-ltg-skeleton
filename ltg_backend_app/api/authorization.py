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
from tastypie.authentication import ApiKeyAuthentication

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin authorization
#===============================================================================
    
class UserObjectsOnlyAuthorization(Authorization):
    '''
    assumes the resource using this auth has a 'user' as fk.
    allow POST/GET/PUT. 
    deny DELETE.
    '''
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.filter(user=bundle.request.user)
        
    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")
    
class UserAuthorization(Authorization):
    '''
    custom authorization for user resource
    allow POST/GET/PUT for detail only.
    deny DELETE.
    '''
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        raise Unauthorized("You are not allowed to view a list of objects for this resource.")
        
    def read_detail(self, object_list, bundle):
        # authenticate the user
        ApiKeyAuthentication().is_authenticated(bundle.request)
        # Is the requested object owned by the user?
        return bundle.obj == bundle.request.user

    def update_list(self, object_list, bundle):
        raise Unauthorized("You are not allowed to update a list of objects for this resource.")

    def update_detail(self, object_list, bundle):
        # authenticate the user
        ApiKeyAuthentication().is_authenticated(bundle.request)
        return bundle.obj == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")
    
#===============================================================================
# end authorization
#===============================================================================