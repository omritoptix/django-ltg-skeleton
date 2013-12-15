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

def report(request,type):
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
    
    #check that it has a business profile, and that it's not a phone profile 
    #if not - return unauthorized
    if not user_profile.business_profile.all().exists():
        
        #return unauthorized
        response = HttpResponse(mimetype="text/plain")
        response.write('Unautorized')
        return response
    
    try:
        
        #get the business profile for this report
        business_profile = BusinessProfile.objects.get(user_profile__id = user_profile.id)
        
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
        
        #DEAL REPORT LOGIC
        
        #if the report is of type 'deal'
        if (type=='deal'):
        
            #will hold the sum of amount paid for transactions
            sumOfAmountPaidTransactions = 0
            
            #will hold number of total transactions
            sumOfTransactions = 0        
            
            #copy the current request and add to it the business profile id (the original
            #request.GET is immutable)
            updated_request = request.GET.copy()
            request_additional_dict = {'business_profile__id' : business_profile.id }
            updated_request.update(request_additional_dict)
                
            #get the deals from the rest server
            api_client = TestApiClient()
            resp = api_client.get(uri='/api/v1/deal/', format='json', data=updated_request)
            deals = simplejson.loads(resp.content)['objects']
             
            #get transactions for each deal
            for deal in deals:  
                        
                #filter only deals with status 3 - claimed
                transactionForCurrDeal = Transaction.objects.filter(deal__id=deal['id'],status=3)
                deal['transaction'] = transactionForCurrDeal
                deal['valid_to'] = datetime.datetime.strptime(deal['valid_to'].encode(),"%Y-%m-%dT%H:%M:%S")
                deal['valid_from'] = datetime.datetime.strptime(deal['valid_from'].encode(),"%Y-%m-%dT%H:%M:%S")
                
                #loop over the relevant transaction to sum the total amount paid
                for transaction in transactionForCurrDeal:
                    sumOfTransactions+=1
                    try:
                        sumOfAmountPaidTransactions += (transaction.amount * float(deal['discounted_price'].encode()))
                        
                    except ValueError:
                        print "Could not calculate sumOfTransactions"
                        #TODO - log the error
                        
                    finally:
                        pass
                
            # convert a web page and store the generated PDF to a variable
            t = get_template('report_deal.html')
            html = t.render(Context(
                                    {
                                     'date': pdf_date, 
                                     'deals': deals,
                                     'sumOfAmountPaidTransactions' : sumOfAmountPaidTransactions,
                                     'sumOfTransactions' : sumOfTransactions 
                                     })).encode('utf-8')
                                     
        #TRANSACTION REPORT LOGIC
        
        elif (type=='transaction'):
            
            #will hold the sum of amount paid for transactions
            sumOfAmountPaidTransactions = 0
            
            #will hold number of total transactions
            sumOfTransactions = 0        
            
            #will hold all the relevant deals ids for this business
            business_profile_deals = ""
            
            #get all the relevant deals ids
            for deal in Deal.objects.filter(business_profile__id = business_profile.id, status__in = [1,2,3,4]):
                business_profile_deals += str(deal.id) + ","
                
            #remove last comma
            business_profile_deals = business_profile_deals[:-1]
            
            #copy the current request and add to it the business profile and transaction status params (the original
            #request.GET is immutable)
            updated_request = request.GET.copy()
            request_additional_dict = {'deal__in' : business_profile_deals , 'status': 3 }
            updated_request.update(request_additional_dict)
            
            #get relevant transactions from the rest server
            api_client = TestApiClient()
            resp = api_client.get(uri='/api/v1/transaction/', format='json', data=updated_request)
            transactions_unicode = simplejson.loads(resp.content)['objects']
            
            #will hold the transactions list
            transactions=[]
            
            #get transaction objects from the transactions_unicode and
            #sum the total transactions and amount paid
            for transaction_unicode in transactions_unicode:
                
                #sum total num of transactions
                sumOfTransactions+=1
                
                #sum total amount paid
                try:
                    
                    sumOfAmountPaidTransactions += (transaction_unicode['amount'] * float(transaction_unicode['deal']['discounted_price'].encode()))
                    
                except:
                    
                    pass
                
                #add element to the transaction
                transactions.append(Transaction.objects.get(id = transaction_unicode['id']))
                
            #sort transactions list by creation date
            if (len(transactions) > 0):
                transactions = sorted(transactions, key=lambda transaction:transaction.creation_date)
        
            # convert a web page and store the generated PDF to a variable
            t = get_template('report_transaction.html')
            html = t.render(Context(
                                    {
                                     'date': pdf_date, 
                                     'transactions': transactions,
                                    'sumOfAmountPaidTransactions' : sumOfAmountPaidTransactions,
                                    'sumOfTransactions' : sumOfTransactions 
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