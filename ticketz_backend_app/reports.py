'''
will hold the reports views for our app

Created on Dec 17, 2013
@author: omri
@version:1.0
@copyright:Nerdeez
'''

#===============================================================================
# begin imports
#===============================================================================

from ticketz_backend_app.models import *
from django.template.loader import get_template
from django.template import Context
from tastypie.test import TestApiClient
from django.utils import simplejson
from ticketz_backend_app.custom_views import ReportView
 
#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin reports
#===============================================================================


class TransactionReport(ReportView):
    '''
    will render the transaction report
    '''
    
    def get(self, request, *args, **kwargs):
        
        # init business profile and pdf client
        self.init_report(request)     
        
        # will hold the sum of amount paid for transactions
        sum_of_amount_paid_transactions = 0
        
        # will hold number of t.testotal transactions
        sum_of_transactions = 0        
        
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
            sum_of_transactions += 1
            
            # sum total amount paid
            try:
                
                sum_of_amount_paid_transactions += (transaction_unicode['amount'] * float(transaction_unicode['deal']['discounted_price'].encode()))
                
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
                                'sum_of_amount_paid_transactions' : sum_of_amount_paid_transactions,
                                'sum_of_transactions' : sum_of_transactions 
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
        sum_of_amount_paid_transactions = 0
        
        # will hold number of total transactions
        sum_of_transactions = 0        
        
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
                sum_of_transactions += 1
                try:
                    sum_of_amount_paid_transactions += (transaction.amount * float(deal['discounted_price'].encode()))
                    
                except ValueError:
                    print "Could not calculate sum_of_transactions"
                    # TODO - log the error
        
                finally:
                    pass
            
        # convert a web page and store the generated PDF to a variable
        t = get_template('report_deal.html')
        html = t.render(Context(
                                {
                                 'deals': deals,
                                 'sum_of_amount_paid_transactions' : sum_of_amount_paid_transactions,
                                 'sum_of_transactions' : sum_of_transactions 
                                 })).encode('utf-8')
                                     
        return self.render_report(html)
    
#===============================================================================
# end reports
#===============================================================================
