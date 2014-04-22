'''
will hold our authentication for the api
Created on April 22, 2014
 
@author: Omri Dagan & Yariv Katz
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from tastypie.authentication import ApiKeyAuthentication
import json

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin authentication
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
    
#===============================================================================
# end authentication
#===============================================================================