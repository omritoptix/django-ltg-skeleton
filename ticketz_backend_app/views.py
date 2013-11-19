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
from ticketz_backend_app.models import Business
from ticketz_backend_app.ticketz_api.api import is_send_grid
from ticketz_backend_app import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.utils.html import strip_tags
from smtplib import SMTPSenderRefused
from tastypie.models import ApiKey
import random
 

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
    business = Business.objects.get(id=id)
    return render_to_response('activate_business.html', {'business': business}, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/')
def activate_business(request, id):
    '''
    if we want to activate a business with an id
    '''
    #activate the business
    business = Business.objects.get(id=id)
    user = business.user_profile.all()[0].user
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


#===============================================================================
# end server views
#===============================================================================