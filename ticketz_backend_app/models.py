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
from django.contrib.auth.models import User
from ticketz_backend_app.encryption import EncryptedCharField
from picklefield.fields import PickledObjectField

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin constants
#===============================================================================

DEAL_STATUS = (
    (0, 'Inactive'),
    (1, 'Pending'),
    (2,  'Active'),
    (3,  'Close'),
)

TRANSACTION_STATUS = (
    (0, 'Inactive'),
    (1, 'Reserved'),
    (2,  'Confirmed'),
    (3,  'Claimed'),
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
    phone = models.CharField(max_length=20, default=None, blank=True, null=True)
    uuid = models.CharField(max_length=50, default=None, blank=True, null=True, unique=True)
    business = models.ForeignKey('Business', related_name='user_profile', default=None, blank=True, null=True)
    paymill_client_id = models.CharField(max_length=50, default=None, blank=True, null=True)
    paymill_payment_id = models.CharField(max_length=50, default=None, blank=True, null=True)
    
    def __unicode__(self):
        return self.user.email
    
    def owner(self):
        return self.user.username
    
        
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
    user_profile = models.ForeignKey(UserProfile, related_name='prefrences', blank=False, null=False, unique=True)
    city = models.ForeignKey(City, blank=True, null=True, default=None)
    region = models.ForeignKey(Region, blank=True, null=True, default=None)
    
    def __unicode__(self):
        return self.user_profile.user.email
    
    def owner(self):
        return self.user_profile.user.username
    
class Category(NerdeezModel):
    '''
    will hold the ticketz categories: Movie, Theater, etc.
    the image field will hold a url for an image
    those images has to be loaded in the splash screen
    '''
    title = models.CharField(max_length=100, blank=False, null=False, unique=True)
    image = models.ImageField(upload_to='img/category', default=None, blank=True, null=True)
    
class Business(NerdeezModel):
    '''
    will hold the data for each business that is working with us.
    I didnt want to include fields that are specific for toptix needs cause we might want in the 
    future to work with other API's, so to make stuff as generic as I could I created a dictionary
    field that will hold specific api data that toptix or titan or other service requires.
    Question: Should that data be encrypted?
    '''
    title = models.CharField(max_length=100, blank=False, null=False)
    business_number = models.CharField(max_length=20, blank=True, null=True, unique=True, default=None)
    phone = models.CharField(max_length=20, blank=False, null=False)
    city = models.ForeignKey(City, blank=True, null=True, default=None)
    address = models.CharField(max_length=200, blank=True, null=True, default=None)
    web_service_url = models.CharField(max_length=300, blank=True, null=True, default=None)
    adapter_class = models.CharField(max_length=50, blank=True, null=True, default=None)
    adapter_object = PickledObjectField()
    
class Deal(NerdeezModel):
    '''
    will hold the table for the deals a business is making
    '''
    business = models.ForeignKey(Business)
    title = models.CharField(max_length=150, blank=False, null=False)
    description = models.CharField(max_length=300, blank=True, null=True)
    valid_from = models.DateTimeField(default=lambda: datetime.datetime.now().replace(microsecond=0))
    valid_to = models.DateTimeField(default=lambda: datetime.datetime.now().replace(microsecond=0))
    num_total_places = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='img/deal', default=None, blank=True, null=True)
    original_price = models.DecimalField(max_digits = 6, decimal_places = 3)
    discounted_price = models.DecimalField(max_digits = 6, decimal_places = 3)
    status = models.PositiveIntegerField(choices=DEAL_STATUS, default=0)
    category = models.ForeignKey(Category, blank=True, null=True, default=None)
    
    def owner(self):
        return self.business.user_profile.all()[0].user.username
    
class Transaction(NerdeezModel):
    '''
    will hold the table for a transaction
    '''
    user_profile = models.ForeignKey(UserProfile, blank=False, null=False)
    deal = models.ForeignKey(Deal, blank=False, null=False)
    status = models.PositiveSmallIntegerField(choices=TRANSACTION_STATUS, default=0)
    amount = models.PositiveIntegerField(default=1)
    hash = models.CharField(max_length=20, default=None, blank=True, null=True)
    
    
    
    
    
    
    
    
#===============================================================================
# end tables - models
#===============================================================================

#===============================================================================
# begin signals
#===============================================================================

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

#===============================================================================
# end signals
#===============================================================================



