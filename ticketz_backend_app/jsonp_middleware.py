'''
Created on Feb 20, 2013
will check for the jsonp flag and wrap everything for jsonp
@author: yariv
'''

#===============================================================================
# begin imports
#===============================================================================

import traceback
import sys
from django.conf import settings

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin modifying the response
#===============================================================================

class JsonpMiddleware(object):
    
    def process_response(self, request, response):

        # if request was successful => response code is in range 2XX
        if response.status_code < 200 or response.status_code >= 300:
            return response

        #return if you dont have format=jsonp
        if not 'format' in request.GET or request.GET['format'] != 'jsonp':
            return response

        # Get the callback function name. 
        callback = request.POST.get('callback') or request.GET.get('callback')

        # If we found a callback function name and the response is not already encapsulated in it
        if callback and not response.content.startswith(callback):
            response.content = callback + '(' + response.content + ')'
        
        return response

#===============================================================================
# end modifying the response
#===============================================================================