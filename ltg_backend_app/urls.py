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
from ltg_backend_app.ltg_api.api import *
import ltg_backend_app.views

#===============================================================================
# end imports
#===============================================================================

# enable admin
admin.autodiscover()

#register rest urls
v1_api = Api(api_name='v1')
v1_api.register(UtilitiesResource())

#register urls
urlpatterns = patterns('',
    # enable admin
    url(r'^admin/', include(admin.site.urls)),
    
    #urls for tastypie
    (r'^api/', include(v1_api.urls)),
    
    #grappelli
    (r'^grappelli/', include('grappelli.urls')),
    
    ('^$', ltg_backend_app.views.homepage),
    
    
)
