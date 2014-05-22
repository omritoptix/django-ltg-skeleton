'''
will handle social authentication 
Created on May 21st, 2014

@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

from tastypie.resources import BaseModelResource
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from social.apps.django_app.utils import load_strategy
from social.backends.oauth import BaseOAuth1, BaseOAuth2
from tastypie.http import HttpBadRequest
from tastypie.exceptions import BadRequest, ImmediateHttpResponse
from django.core.urlresolvers import reverse
from social.exceptions import MissingBackend
from django.http.response import Http404, HttpResponse
from tastypie.validation import FormValidation
from ltg_backend_app.models import LtgUser
from ltg_backend_app.api.user import UserResource
from ltg_backend_app.forms import SocialAuthenticationForm
import json

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin social authentication resource 
#===============================================================================

class SocialAuthenticationResource(BaseModelResource):

    class Meta:
        queryset = LtgUser.objects.all()
        allowed_methods = ['post']
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

    def obj_create(self, bundle, request=None, **kwargs):
        """
        Will handle our social authentication.
        require an email permission, or an exception will be raised.
        @param str backend: the backend to use, i.e "twitter"
        @param str uuid: the uuid of the device
        """
        # validate params
        social_auth_form = SocialAuthenticationForm(bundle.data)
        if not (social_auth_form.is_valid()):
            raise ImmediateHttpResponse(HttpBadRequest(json.dumps(social_auth_form.errors)))
        
        # get params
        backend = bundle.data['backend']
        uuid = bundle.data.get('uuid')
        
        # setup redirect uri in order to load strategy
        uri = redirect_uri = "social:complete"
        if uri and not uri.startswith('/'):
            uri = reverse(redirect_uri, args=(backend,))
            
        # load the strategy
        try:
            strategy = load_strategy(
                request=request, backend=backend,
                redirect_uri=uri, **kwargs
            )
        except MissingBackend:
            raise Http404('Backend not found')
        
        # get the backend for the strategy
        backend = strategy.backend
        
        # check backend type and set token accordingly
        if isinstance(backend, BaseOAuth1):
            token = {
                'oauth_token': bundle.data.get('access_token'),
                'oauth_token_secret': bundle.data.get('access_token_secret'),
            }
        elif isinstance(backend, BaseOAuth2):
            token = bundle.data.get('access_token')
        else:
            raise ImmediateHttpResponse(HttpBadRequest('Wrong backend type'))
        
        # authenticate the user
        user = strategy.backend.do_auth(token)
        # check if user is active and set the bundle object to the new user fetch/created
        if user and user.is_active:
            user.uuid = uuid
            bundle.obj = user
            return bundle
        
        else:
            # if email adress was not supplied this error will also occur
            raise BadRequest("Error authenticating user with this provider.")
        
        
    def dehydrate(self, bundle):
        # exclude access_token fields 
        if (bundle.data['access_token']):
            del bundle.data['access_token']
        if (bundle.data['access_token_secret']):
            del bundle.data['access_token_secret']
        # exclude resource uri
        del bundle.data['resource_uri']
        # include user profile resource uri
        bundle.data['user'] = UserResource().get_resource_uri(bundle.obj)              
        # Include the username and api_key in the response
        bundle.data['username'] = bundle.obj.email
        bundle.data['api_key'] = bundle.obj.api_key.key
        
        return bundle
    
#===============================================================================
# end social authentication resource 
#===============================================================================
