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

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin authentication
#===============================================================================

class LtgReadForFreeAuthentication(ApiKeyAuthentication):
    
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