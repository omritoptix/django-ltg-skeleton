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
