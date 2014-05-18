'''
server views are defined here
Created on Jun 20, 2013

@author: Yariv Katz
@version: 1.0
@copyright: nerdeez.com
'''

#===============================================================================
# begin imports
#===============================================================================

from django.template import RequestContext
from django.shortcuts import render_to_response
from social.apps.django_app.utils import strategy
from social.backends.oauth import BaseOAuth1, BaseOAuth2
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.contrib.auth import login
import json
from django.utils import simplejson

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin server views
#===============================================================================

def homepage(request):
    return render_to_response('homepage.html', locals(), context_instance=RequestContext(request))

#===============================================================================
# end server views
#===============================================================================

@strategy('social:complete')
def ajax_auth(request, backend):
    post = simplejson.loads(request.body)
    backend = request.strategy.backend
    if isinstance(backend, BaseOAuth1):
        token = {
            'oauth_token': post.get('access_token'),
            'oauth_token_secret': post.get('access_token_secret'),
        }
    elif isinstance(backend, BaseOAuth2):
        token = post.get('access_token')
    else:
        raise HttpResponseBadRequest('Wrong backend type')
    user = request.strategy.backend.do_auth(token, ajax=True)
    login(request, user)
    data = {'id': user.id, 'username': user.username}
    return HttpResponse(json.dumps(data), mimetype='application/json')