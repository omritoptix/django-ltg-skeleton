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
import ticketz_backend_app.reports

#===============================================================================
# end imports
#===============================================================================

# enable admin
admin.autodiscover()

#register rest urls
v1_api = Api(api_name='v1')
v1_api.register(FlatpageResource())
v1_api.register(UserProfileResource())
v1_api.register(BusinessProfileResource())
v1_api.register(PhoneProfileResource())
v1_api.register(RegionResource())
v1_api.register(CityResource())
v1_api.register(UserPrefrenceResource())
v1_api.register(CategoryResource())
# v1_api.register(BusinessResource())
v1_api.register(DealResource())
v1_api.register(UtilitiesResource())
v1_api.register(TransactionResource())
v1_api.register(UnpaidTransactionResource())
v1_api.register(LoggerResource())
v1_api.register(RefundResource())

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
    
    #views activated from admin
    (r'^confirm-business/(\d+)', ticketz_backend_app.views.confirm_activate_business),
    (r'^activate-business/(\d+)', ticketz_backend_app.views.activate_business),
    
    #report views
    (r'^report/transaction/',ticketz_backend_app.reports.TransactionReport.as_view()),
    (r'^report/deal/',ticketz_backend_app.reports.DealReport.as_view())
    
    
)
