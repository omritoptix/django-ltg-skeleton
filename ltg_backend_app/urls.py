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
import ltg_backend_app.views
from ltg_backend_app.api.utilities import UtilitiesResource
from ltg_backend_app.api.user import UserResource

#===============================================================================
# end imports
#===============================================================================

# enable admin
admin.autodiscover()

#register rest urls
v1_api = Api(api_name='v1')
v1_api.register(UtilitiesResource())
v1_api.register(UserResource())

#register urls
urlpatterns = patterns('',
    # enable admin
    url(r'^admin/', include(admin.site.urls)),
    
    #urls for tastypie
    (r'^api/', include(v1_api.urls)),
    
    #grappelli
    (r'^grappelli/', include('grappelli.urls')),
    
    ('^$', ltg_backend_app.views.homepage),
    
    # url for the api docs generated by tastypie-swagger package
    url(r'api/doc/', include('tastypie_swagger.urls', namespace='tastypie_swagger'),kwargs={'tastypie_api_module':'ltg_backend_app.urls.v1_api', 'namespace':'tastypie_swagger'}),
    
)
