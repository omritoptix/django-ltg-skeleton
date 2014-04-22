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
from ltg_backend_app.ltg_api.utilities import UtilitiesResource
from ltg_backend_app.ltg_api.tutor import TutorResource
from ltg_backend_app.ltg_api.user import UserResource
from ltg_backend_app.ltg_api.anonymous_user import AnonymousUserResource
from ltg_backend_app.ltg_api.user_profile import UserProfileResource
from ltg_backend_app.ltg_api.anonymous_user_profile import AnonymousUserProfileResource
from ltg_backend_app.ltg_api.question import QuestionResource
# from ltg_backend_app.ltg_api.api import *

#===============================================================================
# end imports
#===============================================================================

# enable admin
admin.autodiscover()

#register rest urls
v1_api = Api(api_name='v1')
v1_api.register(UtilitiesResource())
v1_api.register(TutorResource())
v1_api.register(UserResource())
v1_api.register(AnonymousUserResource())
v1_api.register(UserProfileResource())
v1_api.register(AnonymousUserProfileResource())
v1_api.register(QuestionResource())

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
