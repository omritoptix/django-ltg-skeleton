'''
contains the db models
Created on November 7th, 2013

@author: Yariv Katz
@version: 1.0
@copyright: nerdeez.com
'''

#===============================================================================
# begin imports
#===============================================================================

from django.db import models
import datetime
import sys
from django.contrib.auth.models import User
from ticketz_backend_app.encryption import EncryptedCharField
from picklefield.fields import PickledObjectField
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField
from ticketz_backend_app.gcm import gcm_send_bulk_message, gcm_send_message
from ticketz_backend_app.apns import apns_send_bulk_message, apns_send_message
from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin constants
#===============================================================================

DEAL_STATUS = (
    (0, 'Inactive'),
    (1, 'Pending'),
    (2,  'Approved'),
    (3,  'Close'),
    (4,  'Active'),
)

TRANSACTION_STATUS = (
    (0, 'Inactive'),
    (1, 'Reserved'),
    (2,  'Confirmed'),
    (3,  'Claimed'),
)

UNPAID_TRANSACTION_STATUS = (
    (0, 'Inactive'),
    (1, 'Created'),
    (2,  'Claimed'),
)

#===============================================================================
# end constants
#===============================================================================

#===============================================================================
# begin models abstract classes
#===============================================================================

class NerdeezModel(models.Model):
    '''
    this class will be an abstract class for all my models
    and it will contain common information
    '''
    creation_date = models.DateTimeField(default=lambda: datetime.datetime.now().replace(microsecond=0))
    modified_data = models.DateTimeField(default=lambda: datetime.datetime.now().replace(microsecond=0), auto_now=True)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        '''
        object description string
        @returns String: object description
        '''
        return self.title
    
    def updateSearchIndex(self,transactionsList):
        '''
        will update search_index field in each
        transaction with appropriate search indexes
        '''
        
        for transaction in transactionsList:
            
            #get the deal for the transaction
            tranDeal = Deal.objects.get(id = transaction.deal_id)           
            
            #get the userProfile for the transaction
            tranPhoneProfile = PhoneProfile.objects.get(id = transaction.phone_profile_id)
            tranUserProfile = UserProfile.objects.get(id = tranPhoneProfile.user_profile_id)
            tranUser = User.objects.get(id = tranUserProfile.user_id)
            
            #update our data object
            data = tranUser.email + " " + tranUser.first_name + " " + tranUser.last_name + " " + tranUserProfile.phone + " " + tranDeal.title + " " + tranDeal.description
            
            #update our search_index field
            try:
                catalog = 'pg_catalog.english'
                cursor = connection.cursor()
                sql = "update ticketz_backend_app_transaction set search_index = to_tsvector(%s, %s) where id = %s"
                cursor.execute(sql, (catalog, data, transaction.id))
            finally:
                cursor.close()
                
#===============================================================================
# end models abstract classes
#===============================================================================

#===============================================================================
# begin tables - models
#===============================================================================

class UserProfile(NerdeezModel):
    '''
    will hold the models for a user profile
    note that email, first_name. last_name are contained in the user object
    '''
    user = models.ForeignKey(User, unique=True)
    phone = models.CharField(max_length=20, default=None, blank=True, null=True, unique=True)
    
    def __unicode__(self):
        return self.user.email
    
    def owner(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        '''
        will update the search_index field for all the 
        transactions related to this user profile
        '''
        # Call the "real" save() method.
        super(UserProfile, self).save(*args, **kwargs)
        
        #get the phone profile for that user profile
        #use 'filter' instead of 'get' to avoid 'doesNotExist' exception
        phoneProfile = PhoneProfile.objects.filter(user_profile__id = self.id)
        
        #make sure phone profile exists, if not, its a business profile
        #which we don't want to update the transactions for
        if (phoneProfile.exists()):
            
            #get the phone profile object
            phoneProfile = phoneProfile[0]
            
            #get all transactions related to this deal
            transactionsToUpdate = Transaction.objects.filter(phone_profile__id = phoneProfile.id)
            
            #update the search_index field 
            if (transactionsToUpdate.exists()):
                try:
                    self.updateSearchIndex(transactionsToUpdate)
                    
                except:
                    #TODO - log to server
                    print "1. Unexpected error:", sys.exc_info()[0]
                    
                finally:
                    pass
    
class BaseProfile(NerdeezModel):
    
    class Meta(NerdeezModel.Meta):
        abstract = True
    
    def __unicode__(self):
        return self.user_profile.user.email
    
    def owner(self):
        return self.user_profile.user.username
       

class PhoneProfile(BaseProfile):
    user_profile = models.ForeignKey(UserProfile, related_name='phone_profile')
    uuid = models.CharField(max_length=50, default=None, blank=True, null=True, unique=True)
    paymill_client_id = models.CharField(max_length=50, default=None, blank=True, null=True)
    paymill_payment_id = models.CharField(max_length=50, default=None, blank=True, null=True)
    
    
class BusinessProfile(BaseProfile):
    user_profile = models.ForeignKey(UserProfile, related_name='business_profile')
    title = models.CharField(max_length=100, blank=False, null=False)
    business_number = models.CharField(max_length=20, blank=True, null=True, unique=True, default=None)
    city = models.ForeignKey('City', blank=True, null=True, default=None)
    address = models.CharField(max_length=200, blank=True, null=True, default=None)
    web_service_url = models.CharField(max_length=300, blank=True, null=True, default=None)
    adapter_class = models.CharField(max_length=50, blank=True, null=True, default=None)
    adapter_object = PickledObjectField()
    
    def __unicode__(self):
        return 'Business: %s mail: %s' % (self.title, self.user_profile.user.email)


class PushNotificationManager(models.Manager):
    '''
    alows to override the regular querysets
    '''
    def get_query_set(self):
        return PushNotificationQuerySet(self.model)


class PushNotificationQuerySet(models.query.QuerySet):
    '''
    will allow to send push notifications via queryset (bulk messages)
    '''
    def send_message(self, message):
        if self:
            
            #send to all android devices
            registration_ids = []
            for push_notification in self:
                if push_notification.gcm_token != None:
                    registration_ids.append(push_notification.gcm_token)
            if len(registration_ids) > 0:
                gcm_send_bulk_message(
                    registration_ids=registration_ids,
                    data={"message": message},
                    collapse_key="message"
                )
            
            #send to all iphone devices
            apn_tokens = []
            for push_notification in self:
                if push_notification.apn_token != None:
                    apn_tokens.append(push_notification.apn_token)
            if len(apn_tokens) > 0:
                apns_send_bulk_message(registration_ids=apn_tokens, data=message)
    
    
class PushNotification(NerdeezModel):
    '''
    push notification data will be saved here 
    we will send push notification to unregistered users as well
    '''
    
    phone_profile = models.ForeignKey(PhoneProfile, related_name='push_notification', blank=True, null=True)
    apn_token = models.CharField(max_length=100, default=None, blank=True, null=True, unique=True)
    gcm_token = models.CharField(max_length=100, default=None, blank=True, null=True, unique=True)
    objects = PushNotificationManager()
    
    def __unicode__(self):
        if self.phone_profile != None:
            return self.phone_profile.user_profile.user.email
        if self.apn_token != None:
            return self.apn_token
        if self.gcm_token != None:
            return self.gcm_token
        
    def send_message(self, message):
        if self.gcm_token != None:
            return gcm_send_message(registration_id=self.gcm_token, data={"message": message}, collapse_key="message")
        if self.apn_token != None:
            return apns_send_message(registration_id=self.apn_token, data=message)
        
class FlatPage(NerdeezModel):
    '''
    the flatpage table
    will contain textual data about pages like about us and Q&A
    '''
    title = models.CharField(max_length=250, blank=False, null=False, unique=True)
    html = models.TextField(blank=True, null=True)
    
class Region(NerdeezModel):
    '''
    will hold geographic regions
    '''
    title = models.CharField(max_length=100, blank=False, null=False, unique=True)
    
class City(NerdeezModel):
    '''
    will hold a city - all city has a region that they are part of
    '''
    title = models.CharField(max_length=100, blank=False, null=False, unique=True)
    region = models.ForeignKey(Region, related_name='cities',null=False, blank=False)
    
class UserPrefrence(NerdeezModel):
    '''
    will hold user specific configurations
    '''
    phone_profile = models.ForeignKey(PhoneProfile, related_name='prefrences', blank=False, null=False, unique=True)
    city = models.ForeignKey(City, blank=True, null=True, default=None)
    region = models.ForeignKey(Region, blank=True, null=True, default=None)
    
    def __unicode__(self):
        return self.phone_profile.user_profile.user.email
    
    def owner(self):
        return self.phone_profile.user_profile.user.username
    
class Category(NerdeezModel):
    '''
    will hold the ticketz categories: Movie, Theater, etc.
    the image field will hold a url for an image
    those images has to be loaded in the splash screen
    '''
    title = models.CharField(max_length=100, blank=False, null=False, unique=True)
    image = models.ImageField(upload_to='img/category', default=None, blank=True, null=True, max_length=1000)
    
    
class Deal(NerdeezModel):
    '''
    will hold the table for the deals a business is making
    '''
    business_profile = models.ForeignKey(BusinessProfile)
    title = models.CharField(max_length=150, blank=False, null=False)
    description = models.CharField(max_length=300, blank=True, null=True)
    valid_from = models.DateTimeField(default=lambda: datetime.datetime.now().replace(microsecond=0))
    valid_to = models.DateTimeField(default=lambda: datetime.datetime.now().replace(microsecond=0))
    num_total_places = models.PositiveIntegerField(default=0)
    num_places_left = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='img/deal', default=None, blank=True, null=True, max_length=1000)
    original_price = models.DecimalField(max_digits = 6, decimal_places = 3)
    discounted_price = models.DecimalField(max_digits = 6, decimal_places = 3)
    status = models.PositiveIntegerField(choices=DEAL_STATUS, default=0)
    category = models.ForeignKey(Category, blank=True, null=True, default=None)
    is_notified = models.BooleanField(default=False)
    
    search_index = VectorField()

    objects = SearchManager(
        fields = ('title', 'description'),
        config = 'pg_catalog.english', # this is default
        search_field = 'search_index', # this is default
        auto_update_search_field = True
    )
    
    def owner(self):
        return self.business_profile.user_profile.user.username
    
    @classmethod
    def search(cls, query):
        '''
        used for searching using contains
        @param query: string of the query to search
        @return: {QuerySet} all the objects matching the search
        '''
        
        return cls.objects.search(query).distinct()
    
    def save(self, *args, **kwargs):
        '''
        will update the search_index field for all the 
        transactions related to this deal
        '''
        # Call the "real" save() method.
        super(Deal, self).save(*args, **kwargs)
        
        #get all transactions related to this deal
        transactionsToUpdate = Transaction.objects.filter(deal__id = self.id)
        
        #update the search_index field 
        if (transactionsToUpdate.exists()):
            try:
                self.updateSearchIndex(transactionsToUpdate)
                
            except:
                #TODO - log to server
                print "2. Unexpected error:", sys.exc_info()[0]
                
            finally:
                pass
        
    
class Transaction(NerdeezModel):
    '''
    will hold the table for a transaction
    '''
    phone_profile = models.ForeignKey(PhoneProfile, blank=False, null=False)
    deal = models.ForeignKey(Deal, blank=False, null=False, related_name='transactions')
    status = models.PositiveSmallIntegerField(choices=TRANSACTION_STATUS, default=0)
    amount = models.PositiveIntegerField(default=1)
    hash = models.CharField(max_length=20, default=None, blank=True, null=True)
    paymill_transaction_id = models.CharField(max_length=50, default=None, blank=True, null=True)
    
    search_index = VectorField()

    objects = SearchManager(
        fields = None,
        config = 'pg_catalog.english', # this is default
        search_field = 'search_index', # this is default
        auto_update_search_field = False
    )
    
    def owner(self):
        return [self.deal.business_profile.user_profile.user.username, self.phone_profile.user_profile.user.username]
    
    class Meta(NerdeezModel.Meta):
        unique_together = (("phone_profile", "hash"),)
    
    def __unicode__(self):
        return 'Transaction for user: %s with phone: %s' % (self.phone_profile.user_profile.user.email, self.phone_profile.user_profile.phone)
    
    def save(self, *args, **kwargs):
        '''
        will update the search_index field for the current transaction
        '''
        # Call the "real" save() method.
        super(Transaction, self).save(*args, **kwargs)        
        
        #update the search_index field 
        try:
            self.updateSearchIndex([self])
            
        except:
            #TODO - log to server
            print "3. Unexpected error:", sys.exc_info()[0]
            
        finally:
            pass
    
class Refund(NerdeezModel):
    '''
    the table for refunds for customers
    '''
    transaction = models.ForeignKey(Transaction, blank=False, null=False)
    description = models.CharField(max_length=1000, blank=True, null=True, default=None)
    paymill_refund_id = models.CharField(max_length=100, blank=True, null=True, default=None)
    
    def owner(self):
        return self.transaction.deal.business_profile.user_profile.user.username
    
    def __unicode__(self):
        return 'Refund for user: %s' % (self.transaction.deal.business_profile.user_profile.user.email)
    
    
class UnpaidTransaction(NerdeezModel):
    '''
    a transaction that is not paid
    '''
    phone_profile = models.ForeignKey(PhoneProfile, blank=False, null=False)
    deal = models.ForeignKey(Deal, blank=False, null=False)
    status = models.PositiveSmallIntegerField(choices=UNPAID_TRANSACTION_STATUS, default=0)
    hash = models.CharField(max_length=20, default=None, blank=True, null=True)
    
    class Meta(NerdeezModel.Meta):
        unique_together = (("phone_profile", "deal"),("phone_profile", "hash"),)
        
    def __unicode__(self):
        return "User: %s Purchased deal: %d" % (self.phone_profile.user_profile.user.username, self.deal.id)
    
    def owner(self):
        return self.deal.business_profile.user_profile.user.username
    
    
class Logger(NerdeezModel):
    '''
    will load failed transaction
    '''
    path = models.CharField(max_length=1000, blank=True, null=True, default=None)
    post = models.TextField(blank=True, null=True, default=None)
    get = models.TextField(blank=True, null=True, default=None)
    content = models.TextField(blank=True, null=True, default=None)
    free_text = models.TextField(blank=True, null=True, default=None)
    
    def __unicode__(self):
        return self.path
    
    
    
#===============================================================================
# end tables - models
#===============================================================================

#===============================================================================
# begin signals
#===============================================================================

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

@receiver(post_save, sender=User)
def userPreSaveHandler(sender, **kwargs):
    '''
    will update the search_index field for all transactions related
    to the current user
    '''
    try:
        
            #get the related user profile
            userProfile = UserProfile.objects.filter(user__id = kwargs['instance'].id)
             
            if (userProfile.exists()):
                 
                userProfile = userProfile[0]
             
                #use 'filter' instead of 'get' to avoid 'doesNotExist' exception
                phoneProfile = PhoneProfile.objects.filter(user_profile__id = userProfile.id)
                 
                #make sure phone profile exists, if not, its a business profile
                #which we don't want to update the transactions for
                if (phoneProfile.exists()):
                     
                    #get the phone profile object
                    phoneProfile = phoneProfile[0]
                     
                    #get transaction to related phone profile
                    transactionsList = Transaction.objects.filter(phone_profile_id = phoneProfile.id)
                    
                    #check if there are transactions for the current user
                    if (transactionsList.exists()): 
                 
                        #call nerdeezModel with the userProfile instance (since user does not inherit from nerdeezProfile)
                        NerdeezModel.updateSearchIndex(userProfile,transactionsList)
                 
    except:
        #TODO - log to server
        print "4. Unexpected error:", sys.exc_info()[0]
         
    finally:
        pass
    

#===============================================================================
# end signals
#===============================================================================



