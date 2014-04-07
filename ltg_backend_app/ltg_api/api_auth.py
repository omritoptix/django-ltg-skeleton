'''
Authorization for our tastypie api
Created on Apr 7, 2014

@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from tastypie.authentication import ApiKeyAuthentication
import json
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import Unauthorized

#===============================================================================
# end imports
#===============================================================================


#===============================================================================
# begin authentication/authorization 
#===============================================================================

class LtgApiKeyAuthentication(ApiKeyAuthentication):
    def extract_credentials(self, request):
        username, api_key = super(LtgApiKeyAuthentication, self).extract_credentials(request)
        if username == None and api_key == None and (request.method == 'POST' or request.method == 'PUT'):
            post = json.loads(request.body)
            username = post.get('username')
            api_key = post.get('api_key')
        return username, api_key
            

class LtgReadForFreeAuthentication(LtgApiKeyAuthentication):
    
    def is_authenticated(self, request, **kwargs):
        '''
        get is allowed without cradentials and all other actions require api key and username
        @return: boolean if authenticated
        '''
        if request.method == 'GET':
            return True
        return super( LtgReadForFreeAuthentication, self ).is_authenticated( request, **kwargs )
        
class LtgReadForFreeAuthorization( DjangoAuthorization ):
    '''
    Authorizes every authenticated user to perform GET, 
    it will allow post to everyone
    and put/delete if there is owner only he can do it.
    '''
    
    def base_checks(self, request, model_klass):
        '''
        extend base checks to call api authentication in order
        to recognize the current user
        '''
        LtgApiKeyAuthentication().is_authenticated(request)
        return super(LtgReadForFreeAuthorization,self).base_checks(request,model_klass)
        
    def owner_auth(self, bundle):
        '''
        gets a bundle and return true if the current user is the owner
        @param Object bundle: tastypie bundle object
        @return: true if owner raise Unauthorized if not
        '''
        if hasattr(bundle.obj, 'owner') and (bundle.request.user.username in bundle.obj.owner()):
            return True
        else:
            raise Unauthorized('you are not auth to modify this record');
        
    def read_detail(self, object_list, bundle):
        return True
    
    def update_detail(self, object_list, bundle):
        return self.owner_auth(bundle) and super(LtgReadForFreeAuthorization,self).update_detail(object_list,bundle)
    
    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be updated, iterate over them.
        for obj in object_list:
            if bundle.request.user.username in obj.owner():
                allowed.append(obj)

        #intersect between django authorization and our condition
        django_auth_set = super(LtgReadForFreeAuthorization,self).update_list(object_list,bundle)
        return list(set(allowed).intersection(set(django_auth_set)))
    
    def delete_detail(self, object_list, bundle):
        return self.owner_auth(bundle) and super(LtgReadForFreeAuthorization,self).delete_detail(object_list,bundle)
    
    def delete_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be deleted, iterate over them.
        for obj in object_list:
            if bundle.request.user.username in obj.owner():
                allowed.append(obj)

        #intersect between django authorization and our condition
        django_auth_set = super(LtgReadForFreeAuthorization,self).delete_list(object_list,bundle)
        return list(set(allowed).intersection(set(django_auth_set)))
    
class LtgOnlyOwnerCanReadAuthorization( LtgReadForFreeAuthorization ):
    '''
    Authorizes every authenticated owner to perform GET, for all others
    performs LtgReadForFreeAuthorization.
    '''
    
    def read_detail(self, object_list, bundle):
        return self.owner_auth(bundle)
    
    def read_list(self, object_list, bundle):   
        # if anonymous user return unauthorized
        if (bundle.request.user.is_anonymous()):
            raise Unauthorized('you are not authorized to view this resource')
        
        # will hold a list of all allowed object id's
        allowed = []

        # Since they may not all be read, iterate over them.
        for obj in object_list:
            if bundle.request.user.username in obj.owner():
                allowed.append(obj.id)

        #intersect between django authorization list and our list
        django_auth_query_set = super(LtgReadForFreeAuthorization,self).read_list(object_list,bundle)
        django_auth_id_list = django_auth_query_set.values_list('id',flat=True)
        allowed = list(set(allowed).intersection(set(django_auth_id_list)))
    
        # we need to return QuerySet and not list
        try:
            allowed = bundle.obj._meta.model.objects.filter(id__in = allowed)
        except:
            return []
            
        return allowed
    
#===============================================================================
# end authentication/authorization 
#===============================================================================