'''
our server urls are defined in this page
Created on Jun 20, 2013

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
from nerdeez_server_app.nerdeez_api.api import *
import nerdeez_server_app.views

#===============================================================================
# end imports
#===============================================================================

# enable admin
admin.autodiscover()

#register rest urls
v1_api = Api(api_name='v1')
v1_api.register(SchoolGroupResource())
v1_api.register(FlatpageResource())
v1_api.register(UtilitiesResource())
v1_api.register(UserProfileResource())
v1_api.register(EnrollResource())
v1_api.register(HwResource())
v1_api.register(FileResource())

#register urls
urlpatterns = patterns('',
    # enable admin
    url(r'^admin/', include(admin.site.urls)),
    
    #urls for the cross domain comunications
    ('^$', nerdeez_server_app.views.porthole),
    ('^proxy/', nerdeez_server_app.views.proxy),
    
    #urls for tastypie
    (r'^api/', include(v1_api.urls)),
    
    #grappelli
    (r'^grappelli/', include('grappelli.urls')),
    
    
)
