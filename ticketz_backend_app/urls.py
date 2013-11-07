'''
our server urls are defined in this page
Created on November 7, 2013

@author: Yariv Katz
@version: 1.0
@copyright: nerdeez.com
'''

#===============================================================================
# begin imports
#===============================================================================

from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from ticketz_backend_app.ticketz_api.api import *
import ticketz_backend_app.views

#===============================================================================
# end imports
#===============================================================================

# enable admin
admin.autodiscover()

#register rest urls
v1_api = Api(api_name='v1')

#register urls
urlpatterns = patterns('',
    # enable admin
    url(r'^admin/', include(admin.site.urls)),
    
    #urls for the cross domain comunications
    ('^$', ticketz_backend_app.views.porthole),
    ('^proxy/', ticketz_backend_app.views.proxy),
    
    #urls for tastypie
    (r'^api/', include(v1_api.urls)),
    
    #grappelli
    (r'^grappelli/', include('grappelli.urls')),
    
    
)
