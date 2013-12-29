'''
Tastypie will play with this file to create a rest server
Created on Jun 20, 2013

@author: Yariv Katz
@version: 1.0
@copyright: nerdeez.com
'''

#===============================================================================
# begin imports
#===============================================================================

from tastypie.resources import ModelResource, ALL
from tastypie import fields
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.authentication import ApiKeyAuthentication, Authentication
from ticketz_backend_app.models import *
import os
from django.template.loader import get_template
from django.template import Context
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from ticketz_backend_app import settings
from smtplib import SMTPSenderRefused

from tastypie.http import HttpAccepted, HttpApplicationError
from django.conf.urls import url
from tastypie.utils import trailing_slash
from django.utils import simplejson
from tastypie.exceptions import Unauthorized
from tastypie.http import HttpUnauthorized, HttpConflict, HttpCreated, HttpBadRequest, HttpNotFound, HttpBadRequest
from django.contrib import auth
from tastypie.models import ApiKey
from django.utils import simplejson as json
from ticketz_backend_app.forms import UserCreateForm
from django.contrib.auth import authenticate, login
import random
from tastypie.resources import ALL_WITH_RELATIONS
import pymill
from twilio.rest import TwilioRestClient
from django.core.urlresolvers import resolve, get_script_prefix
from django.db.models import Q
from tastypie import http
from tastypie.exceptions import ImmediateHttpResponse
from kombu.transport.django.managers import select_for_update
from django.db import transaction
from ticketz_backend_app import facebook
from tastypie.test import TestApiClient



#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin constants
#===============================================================================

API_URL = '/api/v1/'

#===============================================================================
# end constants
#===============================================================================


#===============================================================================
# begin abstract resources
#===============================================================================

class NerdeezResource(ModelResource):
    '''
    abstract class with commone attribute common to all my rest models
    '''
    
    #set read only fields
    class Meta:
        allowed_methods = ['get']
        always_return_data = True
        ordering = ['title']
        read_only_fields = ['creation_date', 'modified_data']
        invisible_fields = []
        
    @staticmethod
    def send_sms(to, body):
        '''
        will send an sms to the phone number with a message
        @param str to: the phone number to send the message to
        @param str body: the body of the message 
        '''
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        client = TwilioRestClient(account_sid, auth_token)
        message = client.messages.create(from_=settings.TWILIO_PHONE, to=to, body=body)
        return message
    
    @staticmethod
    def get_pk_from_uri(uri):
        '''
        gets a uri and return the pk from the url
        @param uri: the url
        @return: string the pk 
        '''
        
        prefix = get_script_prefix()
        chomped_uri = uri
    
        if prefix and chomped_uri.startswith(prefix):
            chomped_uri = chomped_uri[len(prefix)-1:]
    
        try:
            view, args, kwargs = resolve(chomped_uri)
        except:
            return 0
    
        return kwargs['pk']
    
    def hydrate(self, bundle):
        read_only_fields = self.Meta.read_only_fields
        for field in read_only_fields:
            if field in bundle.data:
                del bundle.data[field]
        return super(NerdeezResource, self).hydrate(bundle)
    
    def dehydrate(self, bundle):
        invisible_fields = self.Meta.invisible_fields
        for field in invisible_fields:
            if field in bundle.data:
                print field
                del bundle.data[field]
        return super(NerdeezResource, self).dehydrate(bundle)
        
#===============================================================================
# end abstract resources
#===============================================================================

#===============================================================================
# begin global function
#===============================================================================

def is_send_grid():
    '''
    determine if i can send mails in this server
    @return: True if i can
    '''
    return 'SENDGRID_USERNAME' in os.environ


#===============================================================================
# end global function
#===============================================================================

#===============================================================================
# begin authorization/authentication
#===============================================================================

class NerdeezApiKeyAuthentication(ApiKeyAuthentication):
    def extract_credentials(self, request):
        username, api_key = super(NerdeezApiKeyAuthentication, self).extract_credentials(request)
        if username == None and api_key == None and (request.method == 'POST' or request.method == 'PUT'):
            post = simplejson.loads(request.body)
            username = post.get('username')
            api_key = post.get('api_key')
        return username, api_key
            

class NerdeezReadForFreeAuthentication(NerdeezApiKeyAuthentication):
    
    def is_authenticated(self, request, **kwargs):
        '''
        get is allowed without cradentials and all other actions require api key and username
        @return: boolean if authenticated
        '''
        if request.method == 'GET':
            return True
        return super( NerdeezReadForFreeAuthentication, self ).is_authenticated( request, **kwargs )
        
class NerdeezReadForFreeAuthorization( DjangoAuthorization ):
    '''
    Authorizes every authenticated user to perform GET, 
    it will allow post to everyone
    and put/delete if there is owner only he can do it.
    '''
    
    def owner_auth(self, bundle):
        '''
        gets a bundle and return true if the current user is the owner
        @param Object bundle: tastypie bundle object
        @return: true if owner raise Unauthorized if not
        '''
        obj = bundle.obj
        if hasattr(obj, 'owner') and (obj.owner() == bundle.request.user.username or bundle.request.user.username in obj.owner()):
            return True
        else:
            raise Unauthorized('you are not auth to modify this record');
        
    def read_detail(self, object_list, bundle):
        return True
    
    def create_detail(self, object_list, bundle):
        return True
    
    def create_list(self, object_list, bundle):
        return object_list
    
    def update_detail(self, object_list, bundle):
        return self.owner_auth(bundle)
    
    def delete_detail(self, object_list, bundle):
        return self.owner_auth(bundle)
    
class NerdeezOnlyOwnerCanReadAuthorization( NerdeezReadForFreeAuthorization ):
    '''
    Authorizes every authenticated owner to perform GET, for all others
    performs NerdeezReadForFreeAuthorization.
    '''
    
    def read_detail(self, object_list, bundle):
        return self.owner_auth(bundle)

        

#===============================================================================
# end authorization/authentication
#===============================================================================

#===============================================================================
# begin the actual rest api
#===============================================================================

class FlatpageResource(NerdeezResource):
    '''
    the rest api for the flatpage
    '''
    class Meta(NerdeezResource.Meta):
        queryset = FlatPage.objects.all()
        filtering = {
                     'title': ALL,
                     }
        

     
class UserProfileResource(NerdeezResource):
    class Meta(NerdeezResource.Meta):
        queryset = UserProfile.objects.all()
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezOnlyOwnerCanReadAuthorization()
        read_only_fields = ['user', 'phone']
    
    def dehydrate(self, bundle):
        bundle.data['first_name'] = bundle.obj.user.first_name
        bundle.data['last_name'] = bundle.obj.user.last_name
        bundle.data['email'] = bundle.obj.user.email
        return super(UserProfileResource, self).dehydrate(bundle)
        
class PhoneProfileResource(NerdeezResource):
    '''
    api for the phone users
    '''
    user_profile = fields.ToOneField('ticketz_backend_app.ticketz_api.api.UserProfileResource', 'user_profile', full=True, null=True)
    class Meta(NerdeezResource.Meta):
        queryset = PhoneProfile.objects.all()
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezOnlyOwnerCanReadAuthorization()
        allowed_methods = ['get', 'put']
        read_only_fields = ['paymill_client_id', 'paymill_payment_id', 'user_profile', 'facebook_user_id', 'facebook_access_token']
        invisible_fields = ['paymill_client_id', 'paymill_payment_id', 'apn_token', 'gcm_token', 'facebook_user_id', 'facebook_access_token']
        
    def dehydrate(self, bundle):
        '''
        will return also is_payed
        '''
        bundle.data['is_payed'] = False
        try:
            if bundle.obj.paymill_payment_id != None:
                bundle.data['is_payed'] = True
        except:
            bundle.data['is_payed'] = False
        return super(PhoneProfileResource, self).dehydrate(bundle)
        
class BusinessProfileResource(NerdeezResource):
    '''
    api for the business profile
    '''
    user_profile = fields.ToOneField('ticketz_backend_app.ticketz_api.api.UserProfileResource', 'user_profile', full=True, null=True)
    class Meta(NerdeezResource.Meta):
        queryset = BusinessProfile.objects.all()
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezOnlyOwnerCanReadAuthorization()
        allowed_methods = ['get', 'put']
        read_only_fields = ['web_service_url', 'adapter_class', 'adapter_object']
        invisible_fields = ['web_service_url', 'adapter_class', 'adapter_object']
        filtering = {
                     'id': ALL_WITH_RELATIONS
                     }
        

class PushNotificationResource(NerdeezResource):
    '''
    api to save the user push notification cradentials
    '''
    class Meta(NerdeezResource.Meta):
        queryset = PushNotification.objects.all()
        authentication = Authentication()
        authorization = Authorization()
        allowed_methods = ['post']
        
class RegionResource(NerdeezResource):
    class Meta(NerdeezResource.Meta):
        queryset = Region.objects.all()
        
class CityResource(NerdeezResource):
    region = fields.ToOneField(RegionResource, 'region', null=True, full=True)
    class Meta(NerdeezResource.Meta):
        queryset = City.objects.all()
        
class UserPrefrenceResource(NerdeezResource):
    phone_profile = fields.ToOneField(PhoneProfileResource, 'phone_profile', null=True, full=True)
    city = fields.ToOneField(CityResource, 'city', null=True, full=True)
    region = fields.ToOneField(RegionResource, 'region', null=True, full=True)
    class Meta(NerdeezResource.Meta):
        queryset = UserPrefrence.objects.all()
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezOnlyOwnerCanReadAuthorization()
        allowed_methods = ['get', 'put']
        read_only_fields = ['phone_profile']
        
class CategoryResource(NerdeezResource):
    class Meta(NerdeezResource.Meta):
        queryset = Category.objects.all()
        filtering = {
                     'id': ALL_WITH_RELATIONS
                     }
        
# class BusinessResource(NerdeezResource):
#     '''
#     @deprecated: use BusinessProfileResource
#     '''
#     city = fields.ToOneField(CityResource, 'city', null=True, full=True)
#     class Meta(NerdeezResource.Meta):
#         queryset = Business.objects.all()
#         authentication = NerdeezApiKeyAuthentication()
#         authorization = NerdeezOnlyOwnerCanReadAuthorization()
#         filtering = {
#                      'id': ALL_WITH_RELATIONS
#                      }
        
class DealResource(NerdeezResource):
    business_profile = fields.ToOneField(BusinessProfileResource, 'business_profile', null=True, full=True)
    category = fields.ToOneField(CategoryResource, 'category', null=True, full=True)
    class Meta(NerdeezResource.Meta):
        queryset = Deal.objects.all()
        authentication = Authentication()
        authorization = NerdeezReadForFreeAuthorization()
        allowed_methods = ['get', 'put', 'post']
        filtering = {
                     'status': ALL_WITH_RELATIONS,
                     'business_profile': ALL_WITH_RELATIONS,
                     'category': ALL_WITH_RELATIONS,
                     'valid_to': ALL_WITH_RELATIONS,
                     'valid_from': ALL_WITH_RELATIONS,
                     'id':ALL_WITH_RELATIONS,
                     }
        ordering = ['valid_to']
        
    def hydrate(self, bundle):
        status = bundle.data.get('status', 1)
        if status > 1:
            bundle.data['status'] = 1
        bundle.data['business_profile'] = API_URL + 'businessprofile/' + str(bundle.request.user.profile.business_profile.all()[0].id) + '/'
        return super(DealResource, self).hydrate(bundle)
                     
    def get_object_list(self, request):
        '''
        search group logic
        '''
        #if user is not authenticated return just the active deals
        if NerdeezApiKeyAuthentication().is_authenticated(request) != True:
            return Deal.objects.filter(status=4)
        
        if request.GET.get('search') != None:
            return self.Meta.object_class.search(request.GET.get('search'))
        else:
            return super(DealResource, self).get_object_list(request)
        
    def obj_create(self, bundle, **kwargs):
        #if the user is not a business than he is unauth to post
        NerdeezApiKeyAuthentication().is_authenticated(bundle.request)
        try:
            if bundle.request.user.get_profile().business_profile.all()[0] == None:
                raise ImmediateHttpResponse(response=http.HttpUnauthorized("Couldn't find the business profile"))
        except:
            raise ImmediateHttpResponse(response=http.HttpUnauthorized("Couldn't find the business profile"))
        if 'num_total_places' in bundle.data:
            bundle.data['num_places_left'] = bundle.data['num_total_places']
        return super(DealResource, self).obj_create(bundle, **kwargs)
    
    
class TransactionResource(NerdeezResource):
    phone_profile = fields.ToOneField(PhoneProfileResource, 'phone_profile', null=True, full=True)
    deal = fields.ToOneField(DealResource, 'deal', null=True, full=True)
    
    class Meta(NerdeezResource.Meta):
        queryset = Transaction.objects.all()
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezOnlyOwnerCanReadAuthorization()
        allowed_methods = ['get', 'post', 'put']
        read_only_fields = ['paymill_transaction_id']
        filtering = {
                     'deal': ALL_WITH_RELATIONS,
                     'status': ALL_WITH_RELATIONS,
                     'creation_date': ALL_WITH_RELATIONS,
                     }
        ordering = ['creation_date']
        
    def hydrate(self, bundle):
        try:
            bundle.data['phone_profile'] = API_URL + 'phoneprofile/' + str(bundle.request.user.profile.phone_profile.all()[0].id) + '/'
        except:
            if 'phone_profile' in bundle.data:
                del bundle.data['phone_profile']
            
        return super(TransactionResource, self).hydrate(bundle)
    
    def obj_create(self, bundle, **kwargs):
        '''
        will create a transaction object and by doing so will reserve the seats
        @param string deal: will get a deal resource uri
        @return on success a 201 response with the object
        on error will return a 
        '''
        
        bundle.data['status'] = 1
        amount = int(bundle.data.get('amount', 0))
        
        #check amount is legal
        if not amount > 0:
            raise ImmediateHttpResponse(response=http.HttpBadRequest())
        
        #get the deal and lower the seats while maintaining cuncurancy
        deal_id = NerdeezResource.get_pk_from_uri(bundle.data['deal'])
        deal = Deal.objects.select_for_update().get(id=int(deal_id))
        seats_left = deal.num_places_left
        new_seats_left = seats_left - amount
        if new_seats_left < 0:
            transaction.commit()
            raise ImmediateHttpResponse(response=http.HttpConflict())
        deal.num_places_left = new_seats_left
        deal.save()
        transaction.commit()
        
        return super(TransactionResource, self).obj_create(bundle, **kwargs)
    
    def obj_update(self, bundle, skip_errors=False, **kwargs):
        
        #get params
        print '1'
        token = bundle.data.get('token','')
        phone = bundle.data.get('phone', '')
        bundle.data['status'] = 2
        if 'amount' in bundle.data:
            del bundle.data['amount']
        if 'deal' in bundle.data:
            del bundle.data['deal']
        
        #get the user profile
        print '2'
        user = bundle.request.user
        user_profile = user.get_profile()
        phone_profile = user_profile.phone_profile.all()[0]
            
        #update the user object with the data entered
        print '3'
        try:
            if phone != '':
                user_profile.phone = phone
                user_profile.save()
        except Exception, e:
            print e.message
            
        #create a paymill instance
        print '4'
        private_key = settings.PAYMILL_PRIVATE_KEY
        p = pymill.Pymill(private_key)
            
        #get or create the client
        print phone_profile.paymill_client_id
        client_id = phone_profile.paymill_client_id
        if client_id == None:
            if user.email == None:
                raise ImmediateHttpResponse(response=http.HttpBadRequest("user doesn't have a client defined - you must pass an email"))
            try:
                client = p.new_client(
                      email=user.email,
                      description='{id: %d, Name: "%s %s", Email: "%s", Phone: "%s"}' % (phone_profile.id, user.first_name, user.last_name, user.email, user_profile.phone)
                )
            except Exception,e:
                raise ImmediateHttpResponse(response=http.HttpBadRequest(e.message['error']))
                
            client_id = client.id
            phone_profile.paymill_client_id = client_id
            phone_profile.save()
            
        #get or create the payment
        print '5'
        payment_id = phone_profile.paymill_payment_id
        if payment_id == None:
            print token
            if token == '':
                raise ImmediateHttpResponse(response=http.HttpBadRequest("user doesn't have a payment defined - you must pass a token"))
            try:
                payment = p.new_card(
                    token=token,
#                     client=client_id
                    client=p.get_client(client_id)
                )
            except Exception,e:
                raise ImmediateHttpResponse(response=http.HttpBadRequest(e.message['error']))
            payment_id = payment.id
            phone_profile.paymill_payment_id = payment_id
            phone_profile.save()
            
        #get the deal
        #deal_id = NerdeezResource.get_pk_from_uri(bundle.data['deal'])
        print '6'
        transaction = Transaction.objects.get(id=kwargs['pk'])
        deal = transaction.deal
        print bundle.obj.amount
        
        #do the payment
        print '7'
        total_price = deal.discounted_price * bundle.obj.amount
        try:
            transaction = p.transact(
                        amount=int(total_price) * 100,
                        currency='ILS',
                        description='{user_phone_id: %d, amount_purchased: %d, deal_id: %d, first_name: "%s", last_name: "%s", email: "%s", phone: "%s"}' % (phone_profile.id, bundle.obj.amount, deal.id, user.first_name, user.last_name, user.email, user_profile.phone),
                        payment=payment_id
                    )
            transaction_id = transaction.id
        except Exception,e:
            raise ImmediateHttpResponse(response=http.HttpBadRequest(e.message['error']))
                
        bundle.data['paymill_transaction_id'] = transaction_id
        
        #send the user a cnfirmation email
        print '8'
        if is_send_grid():
            t = get_template('emails/confirm_purchase.html')
            html = t.render(Context({'admin_mail': settings.ADMIN_MAIL, 'admin_phone': settings.ADMIN_PHONE, 'deal': deal, 'amount': bundle.obj.amount}))
            text_content = strip_tags(html)
            msg = EmailMultiAlternatives('2Nite Confirm Purchase', text_content, settings.FROM_EMAIL_ADDRESS, [user.email])
            msg.attach_alternative(html, "text/html")
            try:
                msg.send()
            except SMTPSenderRefused, e:
                raise ImmediateHttpResponse(response=http.HttpBadRequest("Failed to send the mail"))
                
        #sms the hash
        print '9'
        hash = ''
        for i in range(0,5):
            hash = hash + str(random.randrange(start=0, stop=10))
        bundle.data['hash'] = hash
        try:
            message = 'Your order confirmation code is: %s' % (bundle.data['hash'])
            print user_profile.phone
            NerdeezResource.send_sms(user_profile.phone, message)
        except Exception,e:
            raise ImmediateHttpResponse(response=http.HttpBadRequest(e.message))
        
        return super(TransactionResource, self).obj_update(bundle, skip_errors=skip_errors, **kwargs)
    
class RefundResource(NerdeezResource):
    '''
    the api to refund a customer
    '''
    transaction = fields.ToOneField(TransactionResource, 'transaction', null=False, full=True)
    class Meta(NerdeezResource.Meta):
        queryset = Refund.objects.all()
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezOnlyOwnerCanReadAuthorization()
        allowed_methods = ['get', 'post']
        
    def obj_create(self, bundle, **kwargs):
        '''
        will create a refund for a user and will return the money through paymill api
        '''
        
        #get the transaction object and the total paid
        transaction_id = NerdeezResource.get_pk_from_uri(bundle.data['transaction'])
        transaction = Transaction.objects.get(id=transaction_id)
        total_refund = transaction.amount * 100 * int(transaction.deal.discounted_price)
        
        #submit a refund to paymill
        private_key = settings.PAYMILL_PRIVATE_KEY
        p = pymill.Pymill(private_key)
        refund = p.refund(transaction.paymill_transaction_id, int(total_refund), bundle.data.get('description', ''))
        bundle.data['paymill_refund_id'] = refund.id
        
        return super(RefundResource, self).obj_create(bundle, **kwargs)
        
                
        

class UnpaidTransactionResource(NerdeezResource):
    phone_profile = fields.ToOneField(PhoneProfileResource, 'phone_profile', null=True, full=False)
    deal = fields.ToOneField(DealResource, 'deal', null=True, full=False)
    
    class Meta(NerdeezResource.Meta):
        queryset = UnpaidTransaction.objects.all()
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezOnlyOwnerCanReadAuthorization()
        allowed_methods = ['get', 'post']
        
    def hydrate(self, bundle):
        bundle.data['status'] = 1
        try:
            bundle.data['phone_profile'] = API_URL + 'phoneprofile/' + str(bundle.request.user.profile.phone_profile.all()[0].id) + '/'
        except:
            if 'phone_profile' in bundle.data:
                del bundle.data['phone_profile']
        return super(UnpaidTransactionResource, self).hydrate(bundle)
    
    def obj_create(self, bundle, **kwargs):
        
        #update the phone if needed
        phone = bundle.data.get('phone', '')
        user_profile = bundle.request.user.get_profile()
        if phone != '':
            user_profile.phone = phone
            user_profile.save()
            
        #create the hash and put it in bundle
        hash = ''
        for i in range(0,5):
            hash = hash + str(random.randrange(start=0, stop=10))
        bundle.data['hash'] = hash
        
        result =  super(UnpaidTransactionResource, self).obj_create(bundle, **kwargs)
        
        #send the sms to the user
        try:
            message = 'Your order confirmation code is: %s' % (hash)
            NerdeezResource.send_sms(user_profile.phone, message)
        except Exception,e:
            return self.create_response(bundle.request, {
                    'success': False,
                    'message': "Failed to send the sms",
                    'exception': e.message
                    }, HttpApplicationError)
            
        return result
    
class LoggerResource(NerdeezResource):
    class Meta(NerdeezResource.Meta):
        allowed_methods = ['post']
        queryset = Logger.objects.all()
        authentication = Authentication()
        authorization = Authorization()
        
    
        
class UtilitiesResource(NerdeezResource):
    '''
    the api for things that are not attached to models: 
    - contact us: url: /api/v1/utilities/contact/
    '''
    
    class Meta(NerdeezResource.Meta):
        allowed_methods = ['post']
        
    def _register_user(self, email, password=None, is_active=False, username=None, request=None):
        '''
        create a user object
        @param string password: 
        @param string email: 
        @param boolean is_active: set if the user is active 
        @param string username: if none than will create a random username
        @return: boolean if created the user 
        '''
        
        #create the username if needed
        api_key = ApiKey()
        if username == None:            
            username = api_key.generate_key()[0:30]
            
        #create password if needed
        if password == None:
            password = api_key.generate_key()[0:30]
        
        #set the request post to contain email password and username
        post_values = {}
        post_values['username'] = username
        post_values['password1'] = password
        post_values['password2'] = password
        post_values['email'] = email
        
        #validation success
        user_form = UserCreateForm(post_values)
        user = None
        if user_form.is_valid():
            
            #create the user
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username,
                                password=password)
            login(request, user)
            user.is_active = is_active
            user.save()
            
        return (user_form.is_valid(), user)
        
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/contact%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('contact'), name="api_contact"),
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r"^(?P<resource_name>%s)/register%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('register'), name="api_register"),
            url(r"^(?P<resource_name>%s)/forgot-password%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('forgot_password'), name="api_forgot_password"),
            url(r"^(?P<resource_name>%s)/register-user%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('register_user'), name="api_register_user"),
            url(r"^(?P<resource_name>%s)/payment%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('payment'), name="api_payment"),
            url(r"^(?P<resource_name>%s)/confirm-transaction%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('confirm_transaction'), name="api_confirm_transaction"),
            url(r"^(?P<resource_name>%s)/login-user%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login_user'), name="api_login_user"),
            url(r"^(?P<resource_name>%s)/register-facebook%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('register_facebook'), name="api_register_facebook"),
        ]
        
    def contact(self, request=None, **kwargs):
        '''
        will send the message to our mail
        '''
        #get params
        post = simplejson.loads(request.body)
        message = post.get('message')
        mail = post.get('mail')
        admin_mail = settings.ADMIN_MAIL
        
        t = get_template('emails/contact_us_email.html')
        html = t.render(Context({'mail': mail, 'message': message}))
        text_content = strip_tags(html)
        msg = EmailMultiAlternatives(u'Nerdeez contact us', text_content, settings.FROM_EMAIL_ADDRESS, [admin_mail])
        msg.attach_alternative(html, "text/html")
        try:
            msg.send()
        except SMTPSenderRefused, e:
            return self.create_response(request, {
                    'success': False,
                    'message': 'Failed to send the email',
                    }, HttpApplicationError )
        
        return self.create_response(request, {
                    'success': True,
                    'message': 'Successfully sent your message',
                    }, HttpAccepted )
        
    def _login(self, request):
        '''
        comon login for users and business
        '''
        #get the params
        post = simplejson.loads(request.body)
        password = post.get('password')
        email = post.get('email')
        
        #get the user with that email address
        try:
            user = User.objects.get(email=email)
        except:
            return {
                    'success': False,
                    'message': 'Invalid email or password',
                    }
        
        user = auth.authenticate(username=user.username, password=password)
        if user is None:
            return {
                    'success': False,
                    'message': 'Invalid email or password',
                    }
        if not user.is_active:
            return {
                'success': False,
                'message': 'Account not activated',
            }
                    
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        
        #successfull login delete all the old api key of the user and create a new one
        #api_keys = ApiKey.objects.filter(user=user)
        #api_keys.delete()
        api_key, created = ApiKey.objects.get_or_create(user=user)
        api_key.save()
        
        return {
                'success': True,
                'message': 'Successfully logged in',
                'api_key': api_key.key,
                'username': user.username
                }
        
        
        
        
    def login(self, request=None, **kwargs):
        '''
        login request is sent here
        @param password: the user password 
        @param email: the user email 
        @return: 401 if login failed with a disctionary with a message, if success will return the following object
        {
            'success': True,
            'message': 'Successfully logged in',
            "user_profile": <The user profile object>,
            'api_key': <the api key of the user valid for a day>,
            'username': <the username of the password>
        }
        '''
        
        #get the login status
        login_status = self._login(request)
        
        #if the login was unsuccessfull than return
        if not login_status['success']:
            return self.create_response(request, login_status, HttpUnauthorized )
            
        ur = BusinessProfileResource()
        ur_bundle = ur.build_bundle(obj=request.user.profile.business_profile.all()[0], request=request)
        login_status["business_profile"] = json.loads(ur.serialize(None, ur.full_dehydrate(ur_bundle), 'application/json')) 
        return self.create_response(request, login_status, HttpAccepted )
    
    def login_user(self, request=None, **kwargs):
        '''
        login the user from the phone
        '''
        
        #get the login status
        login_status = self._login(request)
        
        #if the login was unsuccessfull than return
        if not login_status['success']:
            return self.create_response(request, login_status, HttpUnauthorized )
        
        ur = PhoneProfileResource()
        ur_bundle = ur.build_bundle(obj=request.user.profile.phone_profile.all()[0], request=request)
        login_status["phone_profile"] = json.loads(ur.serialize(None, ur.full_dehydrate(ur_bundle), 'application/json')) 
        return self.create_response(request, login_status, HttpAccepted )
        
    def register(self, request=None, **kwargs):
        '''
        will try and register the user
        we expect here an email and a password sent as post params
        @return:    201 if user is created
                    500 failed to send emails
                    409 conflict with existing account
        '''
        
        #get params
        post = simplejson.loads(request.body)
        email = post.get('email')
        business_number = post.get('business_number')
        phone = post.get('phone')
        address = post.get('address')
        city = post.get('city')
        title = post.get('title')
        
        #is the email already exists?
        try:
            user = User.objects.get(email=email)
            return self.create_response(request, {
                    'success': False,
                    'message': 'User with this mail address already exists',
                    }, HttpConflict )
        except:
            pass
        
        #create the user and the business profile
        is_created, user = self._register_user(email=email, password=None, is_active=False, username=None, request=request)
        if is_created:
            user_profile = user.profile
            user_profile.phone = phone
            user_profile.save() 
            business = BusinessProfile()
            business.title = title
            business.business_number = business_number
            if city != None:
                business.city = City.objects.get(id=city)
            business.user_profile = user_profile
            business.address = address
            business.save()
            
            #send the verification mail
            if is_send_grid():
                t = get_template('emails/register_approval_mail.html')
                html = t.render(Context({'admin_mail': settings.ADMIN_MAIL, 'admin_phone': settings.ADMIN_PHONE}))
                text_content = strip_tags(html)
                msg = EmailMultiAlternatives('2Nite Registration', text_content, settings.FROM_EMAIL_ADDRESS, [email])
                msg.attach_alternative(html, "text/html")
                try:
                    msg.send()
                except SMTPSenderRefused, e:
                    return self.create_response(request, {
                        'success': False,
                        'message': 'Failed to send mail',
                        }, HttpApplicationError )
                    
                #send the admin mail that he should activate the business
                t = get_template('emails/admin_new_business_mail.html')
                html = t.render(Context({}))
                text_content = strip_tags(html)
                msg = EmailMultiAlternatives('Business approval', text_content, settings.FROM_EMAIL_ADDRESS, [settings.ADMIN_MAIL])
                msg.attach_alternative(html, "text/html")
                try:
                    msg.send()
                except SMTPSenderRefused, e:
                    pass
            
            #return the status code
            return self.create_response(request, {
                    'success': True,
                    'message': 'Successfully created the account, Account pending approval',
                    }, HttpCreated )
            
        #validation failed    
        else:
            return self.create_response(request, {
                    'success': False,
                    'message': 'Failed to register the user',
                    }, HttpBadRequest )
            
    def forgot_password(self, request=None, **kwargs):
        '''
        api for the user to create a new password
        return 200 on success
        return 401 on unuthorized (account not activated)
        return 404 on account not found
        return 500 if failed to send mail
        '''
        post = simplejson.loads(request.body)
        email = post.get('email')
        
        #get the profile for that mail
        try:
            user = User.objects.get(email=email)
            user_profile = user.profile
        except:
            return self.create_response(request, {
                    'success': False,
                    'message': "Account with that mail doesn't exist",
                    }, HttpNotFound)
        
        #if the user is not activated by admin yet
        if not user.is_active:
            return self.create_response(request, {
                    'success': False,
                    'message': "Account not activated",
                    }, HttpUnauthorized)
            
        #set the new password
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
                return self.create_response(request, {
                    'success': False,
                    'message': "Failed to send the mail",
                    }, HttpApplicationError)
        
        #success
        return self.create_response(request, {
                    'success': True,
                    'message': "Your new password was sent to your mail",
                    }, HttpAccepted)
        
    def register_user(self, request=None, **kwargs):
        '''
        api for user registration will get the following post params
        @param uuid:
        @param first_name: the users first name 
        @param last_name: the users last name 
        @param email: the users email 
        @param password: the users password 
        @param apn_token: the token for push notification ios
        @param gcm_token: the token for push notification android
        @return  
                 success - 201 if created containing the following details
                 {
                     success: true
                     message: 'registered a new device'
                     api_key: 'api key for the user'
                     username: 'username of the user',
                     'id': '<id of user>'  
                 }
                 success - 202 if user exists containing the following details
                 {
                     success: true
                     message: 'user is already registered'
                     api_key: 'api key for the user'
                     username: 'username of the user'
                     'id': '<id of user>'    
                 }
        '''
        #get the params
        post = simplejson.loads(request.body)
        first_name = post.get('first_name', '')
        last_name = post.get('last_name', '')
        email = post.get('email')
        password = post.get('password')
        
        #check for duplicates for uuid and email
        if User.objects.filter(email=email).count() > 0:
            return self.create_response(request, {
                    'success': False,
                    'message': "Duplicated uuid or email",
                    }, HttpConflict)
        
        #create the user and the phone profile    
        is_created, user = self._register_user(email=email, password=password, is_active=True, username=None, request=request)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        if is_created:
            user_profile = user.profile
            phone_profile = PhoneProfile()
            phone_profile.user_profile = user_profile
            phone_profile.save()
        else:
            return self.create_response(request, {
                    'success': False,
                    'message': "Failed to create the user",
                    }, HttpApplicationError)
            
        #create a new api key for the user
        api_keys = ApiKey.objects.filter(user=user)
        api_keys.delete()
        api_key, created = ApiKey.objects.get_or_create(user=user)
        api_key.save()
        
        ur = PhoneProfileResource()
        ur_bundle = ur.build_bundle(obj=phone_profile, request=request)
        return self.create_response(request, {
                    'success': True,
                    'message': "registered a new user",
                    'api_key': api_key.key,
                    'username': user.username,
                    'phone_profile': json.loads(ur.serialize(None, ur.full_dehydrate(ur_bundle), 'application/json')),
                    }, HttpCreated)
        
    def register_facebook(self, request=None, **kwargs):
        '''
        api for user facebook registration will get the following post params
        @param facebook_user_id: the users id on facebook 
        @param facebook_access_token: the users token on facebook 
        @param uuid: device uuid
        @return  
                 success - 201 if created containing the following details
                 {
                     success: true
                     message: 'registered a new device'
                     api_key: 'api key for the user'
                     username: 'username of the user',
                     'phone_profile': '<profile object>'  
                 }
                 success - 202 if user exists containing the following details
                 {
                     success: true
                     message: 'user is already registered'
                     api_key: 'api key for the user'
                     username: 'username of the user'
                     'phone_profile': '<profile object>'    
                 }
        '''
        
        #get the params
        post = simplejson.loads(request.body)
        facebook_access_token = post.get('facebook_access_token', '')
        
        #get the other data from facebook
        graph = facebook.GraphAPI(facebook_access_token)
        profile = graph.get_object("me")
        
        #get the email
        email = profile['email']
        
        #first lets check if the user exists
        user = None
        try:
            user = User.objects.get(email=email)
            phone_profile = user.get_profile().phone_profile.all()[0]
            api_key, created = ApiKey.objects.get_or_create(user=user)
            ur = PhoneProfileResource()
            ur_bundle = ur.build_bundle(obj=phone_profile, request=request)
            return self.create_response(request, {
                        'success': True,
                        'message': "sending data of existing user",
                        'api_key': api_key.key,
                        'username': user.username,
                        'phone_profile': json.loads(ur.serialize(None, ur.full_dehydrate(ur_bundle), 'application/json')),
                        }, HttpAccepted)
        except:
            pass
        
        #if we didnt find the user than we need to register him
        first_name =  profile['first_name']       
        last_name =  profile['last_name'] 
        data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': facebook_access_token[:10],
                }
        api_client = TestApiClient()
        resp = api_client.post(uri='/api/v1/utilities/register-user/', format='json', data=data)  
        
        #rape the user wall
        graph.put_object("me", "feed", message="This is me raping your wall", link="http://google.com", picture="http://sereedmedia.com/srmwp/wp-content/uploads/kitten.jpg")
        
        #return response
        return self.create_response(request, resp.content, HttpCreated)
            
            
    def confirm_transaction(self, request=None, **kwargs):
        '''
        gets a phone number and a date and check if there is a transaction for those cradentials
        @param string phone: phone number of the user
        @param string hash: the transaction code
        @return: on error - 401 unauth, 404 - transaction not founr
                 on success {
                     success: true
                     is_unpaid: true/false
                     message: <descriptive message>
                     deal: {<deal object>}
                 }  
        '''
        
        #get the params
        post = simplejson.loads(request.body)
        phone = post.get('phone')
        hash = post.get('hash')
        
        #check auth
        apikey_auth = NerdeezApiKeyAuthentication()
        if apikey_auth.is_authenticated(request) != True:
            return self.create_response(request, {
                    'success': False,
                    'message': 'You are not authorized for this action'
                    }, HttpUnauthorized)
            
        #get the user profile
        user = request.user
        user_profile = user.get_profile()
        
        #get the business check if this is a legit business
        business = user_profile.business_profile.all()[0]
        if business == None:
            return self.create_response(request, {
                    'success': False,
                    'message': 'You are not authorized for this action'
                    }, HttpUnauthorized)
            
        #find a userprofile with this phone
        try:
            customer = UserProfile.objects.get(phone=phone).phone_profile.all()[0]
        except:
            return self.create_response(request, {
                    'success': False,
                    'message': "I didn't find this user"
                    }, HttpNotFound)
            
        #paid transaction
        transaction = None
        try:
            transaction = Transaction.objects.get(phone_profile=customer, hash=hash)
            transaction.status = 3
            is_unpaid = False
        except:
            pass
        
        #unpaid transaction
        try:
            transaction = UnpaidTransaction.objects.get(phone_profile=customer, hash=hash)
            transaction.status = 2
            is_unpaid = True
        except:
            pass
        
        #did i find a transaction
        if transaction == None:
            return self.create_response(request, {
                    'success': False,
                    'message': "I didn't find this transaction"
                    }, HttpNotFound)
            
        #is the transaction belong to the business?
        if transaction.deal.business_profile.id != business.id:
            return self.create_response(request, {
                    'success': False,
                    'message': "You are not authorized for confirm this deal"
                    }, HttpUnauthorized)
            
        #success
        transaction.save()
        ur = DealResource()
        ur_bundle = ur.build_bundle(obj=transaction.deal, request=request)
        return self.create_response(request, {
                    'success': True,
                    'message': "Found a paid transaction",
                    'is_unpaid': is_unpaid,
                    'deal': json.loads(ur.serialize(None, ur.full_dehydrate(ur_bundle), 'application/json')),
                    })
            
        
            
        
#===============================================================================
# end teh actual rest api
#===============================================================================