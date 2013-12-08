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
from django.contrib.auth.decorators import user_passes_test
from ticketz_backend_app.models import *
from ticketz_backend_app.ticketz_api.api import is_send_grid
from ticketz_backend_app import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.utils.html import strip_tags
from smtplib import SMTPSenderRefused
from tastypie.models import ApiKey
import random
from tastypie.authentication import ApiKeyAuthentication
from datetime import date
import pdfcrowd
from django.http import HttpResponse
from ticketz_backend_app.ticketz_api.api import DealResource
from tastypie.test import TestApiClient
from django.utils import simplejson
 

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

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')
def confirm_activate_business(request, id):
    '''
    if we want to activate a business with an id
    '''
    business = BusinessProfile.objects.get(id=id)
    return render_to_response('activate_business.html', {'business': business}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')
def activate_business(request, id):
    '''
    if we want to activate a business with an id
    '''
    #activate the business
    business = BusinessProfile.objects.get(id=id)
    user = business.user_profile.user
    user.is_active = True
    api_key = ApiKey()
    pass_length = random.randint(8, 15)
    password = api_key.generate_key()[0:pass_length]
    user.set_password(password)
    user.save()
    
    #semd mail to the business about the account activation
    if is_send_grid():
        t = get_template('emails/confirm_approve_business.html')
        html = t.render(Context({'admin_mail': settings.ADMIN_MAIL, 'admin_phone': settings.ADMIN_PHONE, 'provider_url': settings.PROVIDER_URL, 'password': password}))
        text_content = strip_tags(html)
        msg = EmailMultiAlternatives('2Nite Registration', text_content, settings.FROM_EMAIL_ADDRESS, [user.email])
        msg.attach_alternative(html, "text/html")
        try:
            msg.send()
        except SMTPSenderRefused, e:
            pass
    
    return render_to_response('confirm_activate_business.html', {}, context_instance=RequestContext(request))

def report(request):
    '''
    download user profile pdf
    @param id: the id of the profile being asked 
    '''
    
    #check if the user is authorized to view this pdf
    auth = ApiKeyAuthentication()
    if auth.is_authenticated(request) != True:
        response = HttpResponse(mimetype="text/plain")
        response.write('Unautorized')
        return response
    user = request.user
    user_profile = user.get_profile()
    business = user_profile.business_profile.all()[0]
    
    try:
        
        # create an API client instance
        client = pdfcrowd.Client(settings.PDFCROWD_USERNAME, settings.PDFCROWD_APIKEY)
        
        t = get_template('report_footer.html')
        html = t.render(Context({})).encode('utf-8')
        client.setDefaultTextEncoding('utf-8')
        client.setFooterHtml(html)
        client.setHorizontalMargin("0.0in")

        #date
        today = date.today()
        pdf_date = today.strftime("%d/%m/%y")
        
        #get the deals from the rest server
        api_client = TestApiClient()
        resp = api_client.get(uri='/api/v1/deal/', format='json', data=request.GET)
        deals = simplejson.loads(resp.content)['objects']
         
        #get transactions for each deal
        for deal in deals:
            deal['transaction'] = Transaction.objects.filter(deal__id=deal['id'])
        
                
        # convert a web page and store the generated PDF to a variable
        t = get_template('report.html')
        html = t.render(Context(
                                {
                                 'date': pdf_date, 
                                 'deals': deals, 
                                 })).encode('utf-8')
        pdf = client.convertHtml(html)

        # set HTTP response headers
        response = HttpResponse(mimetype="application/pdf")
        response["Cache-Control"] = "no-cache"
        response["Accept-Ranges"] = "none"
        #response["Content-Disposition"] = "attachment; filename=google_com.pdf"

        # send the generated PDF
        response.write(pdf)
    except pdfcrowd.Error, why:
        response = HttpResponse(mimetype="text/plain")
        response.write(why)
    return response


#===============================================================================
# end server views
#===============================================================================