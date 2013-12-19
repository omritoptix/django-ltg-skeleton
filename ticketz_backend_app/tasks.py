# -*- coding: utf-8 -*-
'''
will hold the async tasks

Created on Nov 26, 2013
@copyright: Nerdeez
@author: ywarezk
@version: 1.0
'''

###############################
# begin imports
###############################

import datetime
from datetime import timedelta
from ticketz_backend_app.models import *
from celery.decorators import periodic_task
from dateutil.relativedelta import relativedelta
from tastypie.models import ApiKey
import django.db.transaction 


###############################
# end imports
###############################



##############################
# Begin async tasks
#############################

@periodic_task(run_every=timedelta(seconds=60), name='tasks.close_deals')
def close_deals():
    '''
    deal that passed the valid to should be closed
    '''
    
    print 'Closing deals that passed the valid_to'
    Deal.objects.filter(valid_to__lte=datetime.datetime.now()).update(status=3)
    
@periodic_task(run_every=timedelta(seconds=60), name='tasks.active_deals')
def active_deals():
    '''
    deal that passed the valid from should be Active
    '''
    
    print 'Change to active deals that passed the valid_from'
    Deal.objects.filter(valid_from__lte=datetime.datetime.now(), valid_to__gt=datetime.datetime.now(), status=2).update(status=4)

@periodic_task(run_every=timedelta(minutes=5), name='tasks.activate_pending_deals')
def activate_pending_deals():
    '''
    deals that are pending more than 10 minutes should turn to active
    '''
    
    print 'activating pending deals'
    now = datetime.datetime.now()
    ten_before = now + relativedelta(minutes=-10)
    Deal.objects.filter(creation_date__lte=ten_before, status=1).update(status=2)
    
@periodic_task(run_every=timedelta(hours=24), name='tasks.delete_old_api_keys')
def delete_old_api_keys():
    '''
    api keys that are older than 24 hours should be deleted
    '''
    
    print 'Deleting old api keys'
    now = datetime.datetime.now()
    day_before = now + relativedelta(hours=-24)
    ApiKey.objects.filter(created__lt=day_before).delete()
    
@periodic_task(run_every=timedelta(minutes=5), name='tasks.send_push_notification')
def send_push_notification():
    '''
    will send push notifications for all active deals that are not modified
    '''
    
    print 'Sending push notifications'
    deals = Deal.objects.filter(status=4, is_notified=False)
    deal = deals[0]
    deals.update(is_notified=True)
#     phone_profiles_ids = [deal.phone_profile.id for deal in deals]
#     phone_profiles = PhoneProfile.objects.filter(id__in=phone_profiles_ids)
    push_message = u'מבצע חדש %s ב %s %s עד השעה %d:%d' % (deal.title, deal.business_profile.title, deal.business_profile.city.title, deal.valid_to.hour, deal.valid_to.minute)
    print push_message
    PushNotification.objects.all().send_message(push_message);
    
    
@periodic_task(run_every=timedelta(minutes=1), name='tasks.close_unactive_reservation')
def close_unactive_reservation():
    '''
    transaction with reserved status should be closed after 10 minutes
    '''
    
    print 'Closing reserved transactions'
    
    #find the transactions that needs to be closed
    now = datetime.datetime.now()
    ten_before = now + relativedelta(minutes=-10)
    transactions = Transaction.objects.filter(status=1, creation_date__lte=ten_before)
    ids = [transaction.id for transaction in transactions]
    transactions.update(status=0)
    transactions = Transaction.objects.filter(id__in=ids)
    
    #for each transaction increment the seat number
    for current_transaction in transactions:
        deal = Deal.objects.select_for_update().get(id=current_transaction.deal.id)    
        seats_left = deal.num_places_left
        new_seats_left = seats_left + current_transaction.amount
        deal.num_places_left = new_seats_left
        deal.save()
        django.db.transaction.commit()
    

    

##############################
# end async tasks
#############################
