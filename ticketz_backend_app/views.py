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

from django.shortcuts import render_to_response
from django.template import RequestContext

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin server views
#===============================================================================

def porthole(request):
    '''
    used for cross domain requests
    '''
    return render_to_response('nerdeez-ember/porthole.html', locals(), context_instance=RequestContext(request))

def proxy(request):
    '''
    used for cross domain requests
    '''
    return render_to_response('nerdeez-ember/proxy.html', locals(), context_instance=RequestContext(request))

#===============================================================================
# end server views
#===============================================================================