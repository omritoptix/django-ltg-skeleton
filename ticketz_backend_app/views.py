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
from datetime import date
import pdfcrowd
from django.http import HttpResponse
from tastypie.test import TestApiClient
from django.utils import simplejson
from ticketz_backend_app.custom_views import ReportView
 

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
    # activate the business
    business = BusinessProfile.objects.get(id=id)
    user = business.user_profile.user
    user.is_active = True
    api_key = ApiKey()
    pass_length = random.randint(8, 15)
    password = api_key.generate_key()[0:pass_length]
    user.set_password(password)
    user.save()
    
    # semd mail to the business about the account activation
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

class TransactionReport(ReportView):
    '''
    will render the transaction report
    '''
    
    def get(self, request, *args, **kwargs):
        
        # init business profile and pdf client
        self.init_report(request)     
        
        # will hold the sum of amount paid for transactions
        sumOfAmountPaidTransactions = 0
        
        # will hold number of t.testotal transactions
        sumOfTransactions = 0        
        
        # will hold all the relevant deals ids for this business
        business_profile_deals = ""
        
        # get all the relevant deals ids
        for deal in Deal.objects.filter(business_profile__id=self.business_profile.id, status__in=[1, 2, 3, 4]):
            business_profile_deals += str(deal.id) + ","
            
        # remove last comma
        business_profile_deals = business_profile_deals[:-1]
        
        # copy the current request and add to it the business profile and transaction status params (the original
        # request.GET is immutable)
        updated_request = request.GET.copy()
        request_additional_dict = {'deal__in' : business_profile_deals , 'status': 3 }
        updated_request.update(request_additional_dict)
        
        # get relevant transactions from the rest server
        api_client = TestApiClient()
        resp = api_client.get(uri='/api/v1/transaction/', format='json', data=updated_request)
        transactions_unicode = simplejson.loads(resp.content)['objects']
        
        # will hold the transactions list
        transactions = []
        
        # get transaction objects from the transactions_unicode and
        # sum the total transactions and amount paid
        for transaction_unicode in transactions_unicode:
            
            # sum total num of transactions
            sumOfTransactions += 1
            
            # sum total amount paid
            try:
                
                sumOfAmountPaidTransactions += (transaction_unicode['amount'] * float(transaction_unicode['deal']['discounted_price'].encode()))
                
            except:
                
                pass
            
            # add element to the transaction
            transactions.append(Transaction.objects.get(id=transaction_unicode['id']))
            
        # sort transactions list by creation date
        if (len(transactions) > 0):
            transactions = sorted(transactions, key=lambda transaction:transaction.creation_date)
        
        # convert a web page and store the generated PDF to a variable
        t = get_template('report_transaction.html')
        html = t.render(Context(
                                {
                                'transactions': transactions,
                                'sumOfAmountPaidTransactions' : sumOfAmountPaidTransactions,
                                'sumOfTransactions' : sumOfTransactions 
                                 })).encode('utf-8')       
                                     
        return self.render_report(html)

class DealReport(ReportView):
    '''
    will render the deal report
    '''
    
    def get(self, request, *args, **kwargs):
        
        # init business profile and pdf client
        self.init_report(request)     
        
        # will hold the sum of amount paid for transactions
        sumOfAmountPaidTransactions = 0
        
        # will hold number of total transactions
        sumOfTransactions = 0        
        
        # copy the current request and add to it the business profile id (the original
        # request.GET is immutable)
        updated_request = request.GET.copy()
        request_additional_dict = {'business_profile__id' : self.business_profile.id }
        updated_request.update(request_additional_dict)
            
        # get the deals from the rest server
        api_client = TestApiClient()
        resp = api_client.get(uri='/api/v1/deal/', format='json', data=updated_request)
        deals = simplejson.loads(resp.content)['objects']
         
        # get transactions for each deal
        for deal in deals:  
                    
            # filter only deals with status 3 - claimed
            transactionForCurrDeal = Transaction.objects.filter(deal__id=deal['id'], status=3)
            deal['transaction'] = transactionForCurrDeal
            deal['valid_to'] = datetime.datetime.strptime(deal['valid_to'].encode(), "%Y-%m-%dT%H:%M:%S")
            deal['valid_from'] = datetime.datetime.strptime(deal['valid_from'].encode(), "%Y-%m-%dT%H:%M:%S")
            
            # loop over the relevant transaction to sum the total amount paid
            for transaction in transactionForCurrDeal:
                sumOfTransactions += 1
                try:
                    sumOfAmountPaidTransactions += (transaction.amount * float(deal['discounted_price'].encode()))
                    
                except ValueError:
                    print "Could not calculate sumOfTransactions"
                    # TODO - log the error
        
                finally:
                    pass
            
        # convert a web page and store the generated PDF to a variable
        t = get_template('report_deal.html')
        html = t.render(Context(
                                {
                                 'deals': deals,
                                 'sumOfAmountPaidTransactions' : sumOfAmountPaidTransactions,
                                 'sumOfTransactions' : sumOfTransactions 
                                 })).encode('utf-8')
                                     
        return self.render_report(html)




#===============================================================================
# end server views
#===============================================================================
