import re
 
from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers
from ltg_backend_app import settings
 
from django import http
 
try:
    XS_SHARING_ALLOWED_ORIGINS = settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_METHODS = settings.XS_SHARING_ALLOWED_METHODS
    XS_SHARING_ALLOWED_HEADERS = settings.XS_SHARING_ALLOWED_HEADERS
except:
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']
    XS_SHARING_ALLOWED_HEADERS = ['Origin', 'X-Requested-With', 'Content-Type', 'Accept']
 
def get_allowed_origins(requested_origin):
    '''
    '''
    if XS_SHARING_ALLOWED_ORIGINS == '*':
        return requested_origin
    else:
        return XS_SHARING_ALLOWED_ORIGINS

 
class XsSharing(object):
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.
         
 
        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
    """
    def process_request(self, request):
    
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin']  = get_allowed_origins(request.META.get('HTTP_ORIGIN', XS_SHARING_ALLOWED_ORIGINS))
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS ) 
            response['Access-Control-Allow-Headers'] = ",".join( XS_SHARING_ALLOWED_HEADERS )
            
            return response
 
        return None
 
    def process_response(self, request, response):

        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response
 
        response['Access-Control-Allow-Origin']  = get_allowed_origins(request.META.get('HTTP_ORIGIN', XS_SHARING_ALLOWED_ORIGINS))
        response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )
        response['Access-Control-Allow-Headers'] = ",".join( XS_SHARING_ALLOWED_HEADERS )
 
        return response

