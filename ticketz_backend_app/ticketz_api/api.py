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
        if hasattr(obj, 'owner') and (obj.owner() == bundle.request.user.username):
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
    business = fields.ToOneField('ticketz_backend_app.ticketz_api.api.BusinessResource', 'business', full=True, null=True)
    class Meta(NerdeezResource.Meta):
        queryset = UserProfile.objects.all()
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezOnlyOwnerCanReadAuthorization()
        allowed_methods = ['get', 'put']
        read_only_fields = ['paymill_client_id', 'paymill_client_id', 'user', 'phone', 'uuid', 'business']
        
class RegionResource(NerdeezResource):
    class Meta(NerdeezResource.Meta):
        queryset = Region.objects.all()
        
class CityResource(NerdeezResource):
    region = fields.ToOneField(RegionResource, 'region', null=True, full=True)
    class Meta(NerdeezResource.Meta):
        queryset = City.objects.all()
        
class UserPrefrenceResource(NerdeezResource):
    user_profile = fields.ToOneField(UserProfileResource, 'user_profile', null=True, full=True)
    city = fields.ToOneField(CityResource, 'city', null=True, full=True)
    region = fields.ToOneField(RegionResource, 'region', null=True, full=True)
    class Meta(NerdeezResource.Meta):
        queryset = UserPrefrence.objects.all()
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezOnlyOwnerCanReadAuthorization()
        allowed_methods = ['get', 'put']
        read_only_fields = ['user_profile']
        
class CategoryResource(NerdeezResource):
    class Meta(NerdeezResource.Meta):
        queryset = Category.objects.all()
        
class BusinessResource(NerdeezResource):
    city = fields.ToOneField(CityResource, 'city', null=True, full=True)
    class Meta(NerdeezResource.Meta):
        queryset = Business.objects.all()
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezOnlyOwnerCanReadAuthorization()
        filtering = {
                     'id': ALL_WITH_RELATIONS
                     }
        
class DealResource(NerdeezResource):
    business = fields.ToOneField(BusinessResource, 'business', null=True, full=False)
    category = fields.ToOneField(CategoryResource, 'category', null=True, full=True)
    class Meta(NerdeezResource.Meta):
        queryset = Deal.objects.all()
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezReadForFreeAuthorization()
        allowed_methods = ['get', 'put', 'post']
        filtering = {
                     'status': ALL_WITH_RELATIONS,
                     'business': ALL_WITH_RELATIONS
                     }
        ordering = ['valid_to']
        
    def hydrate(self, bundle):
        status = bundle.data.get('status', 1)
        if status > 1:
            bundle.data['status'] = 1
        bundle.data['business'] = API_URL + 'business/' + str(bundle.request.user.profile.business.id) + '/'
        return super(DealResource, self).hydrate(bundle)
                     
    def dehydrate(self, bundle):
        
        #calculate the number of purchases
        transactions = Transaction.objects.filter(deal=bundle.obj, status__gte=2)
        total_baught = sum([transaction.amount for transaction in transactions])
        bundle.data['num_available_places'] = bundle.obj.num_total_places - total_baught          
        return super(DealResource, self).dehydrate(bundle)
    
    def get_object_list(self, request):
        '''
        search group logic
        '''
        if request.GET.get('search') != None:
            return self.Meta.object_class.search(request.GET.get('search'))
        else:
            return super(DealResource, self).get_object_list(request)
        
    def obj_create(self, bundle, **kwargs):
        #if the user is not a business than he is unauth to post
        if bundle.request.user.get_profile().business == None:
            raise ImmediateHttpResponse(response=http.HttpUnauthorized())
        return super(DealResource, self).obj_create(bundle, **kwargs)
    
    
class TransactionResource(NerdeezResource):
    user_profile = fields.ToOneField(UserProfileResource, 'user_profile', null=True, full=False)
    deal = fields.ToOneField(DealResource, 'deal', null=True, full=False)
    
    class Meta(NerdeezResource.Meta):
        queryset = Transaction.objects.all()
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezOnlyOwnerCanReadAuthorization()
        allowed_methods = ['get', 'post', 'delete']
        read_only_fields = ['paymill_transaction_id']
        
    def hydrate(self, bundle):
        bundle.data['status'] = 2
        bundle.data['user_profile'] = API_URL + 'userprofile/' + str(bundle.request.user.profile.id) + '/'
        return super(TransactionResource, self).hydrate(bundle)
    
    def obj_create(self, bundle, **kwargs):
        
        #get params
        print '1'
        email = bundle.data.get('email', '')
        token = bundle.data.get('token','')
        first_name = bundle.data.get('first_name', '')
        last_name = bundle.data.get('last_name', '')
        phone = bundle.data.get('phone', '')
        amount = int(bundle.data.get('amount', 0))
        
        #get the user profile
        print '2'
        user = bundle.request.user
        user_profile = user.get_profile()
            
        #update the user object with the data entered
        if first_name != '':
            user.first_name = first_name
        if last_name != '':
            user.last_name = last_name
        if email != '':
            user.email = email
        if phone != '':
            user_profile.phone = phone
            user_profile.save()
        user.save()
        print '3'
            
        #create a paymill instance
        private_key = settings.PAYMILL_PRIVATE_KEY
        p = pymill.Pymill(private_key)
            
        #get or create the client
        client_id = user_profile.paymill_client_id
        if client_id == None:
            if user.email != None:
                return self.create_response(bundle.request, {
                    'success': False,
                    'message': "user doesn't have a client defined - you must pass an email",
                    }, HttpBadRequest )
            try:
                client = p.new_client(
                      email=user.email,
                      description='{id: %d, Name: "%s %s", Email: "%s", Phone: "%s"}' % (user_profile.id, user.first_name, user.last_name, user.email, user_profile.phone)
                )
            except Exception,e:
                return self.create_response(bundle.request, {
                    'success': False,
                    'message': e.message,
                    }, HttpApplicationError )
                
            client_id = client.id
            user_profile.paymill_client_id = client_id
            user_profile.save()
            
        #get or create the payment
        payment_id = user_profile.paymill_payment_id
        if payment_id == None:
            if token == '':
                return self.create_response(bundle.request, {
                    'success': False,
                    'message': "user doesn't have a payment defined - you must pass a token",
                    }, HttpBadRequest )
            try:
                payment = p.new_card(
                    token=token,
                    client=client_id
                )
            except Exception,e:
                return self.create_response(bundle.request, {
                    'success': False,
                    'message': e.message,
                    }, HttpApplicationError )
            payment_id = payment.id
            user_profile.paymill_payment_id = payment_id
            user_profile.save()
            
        #get the deal
        deal_id = NerdeezResource.get_pk_from_uri(bundle.data['deal'])
        deal = Deal.objects.get(id=deal_id)
            
        #do the payment
        total_price = deal.discounted_price * bundle.data['amount']
        try:
            transaction = p.transact(
                        amount=int(total_price) * 100,
                        currency='ILS',
                        description='{user_profile_id: %d, amount_purchased: %d, deal_id: %d, first_name: "%s", last_name: "%s", email: "%s", phone: "%s"}' % (user_profile.id, amount, deal.id, user.first_name, user.last_name, user.email, user_profile.phone),
                        payment=payment_id
                    )
            transaction_id = transaction.id
        except Exception,e:
                return self.create_response(bundle.request, {
                    'success': False,
                    'message': e.message,
                    }, HttpApplicationError )
                
        bundle.data['paymill_transaction_id'] = transaction_id
        
        #send the user a cnfirmation email
        if is_send_grid():
            t = get_template('emails/confirm_purchase.html')
            html = t.render(Context({'admin_mail': settings.ADMIN_MAIL, 'admin_phone': settings.ADMIN_PHONE, 'deal': deal, 'amount': amount}))
            text_content = strip_tags(html)
            msg = EmailMultiAlternatives('2Nite Confirm Purchase', text_content, settings.FROM_EMAIL_ADDRESS, [user.email])
            msg.attach_alternative(html, "text/html")
            try:
                msg.send()
            except SMTPSenderRefused, e:
                return self.create_response(bundle.request, {
                    'success': False,
                    'message': "Failed to send the mail",
                    }, HttpApplicationError)
                
        #sms the hash
        hash = ''
        for i in range(0,5):
            hash = hash + str(random.randrange(start=0, stop=10))
        bundle.data['hash'] = hash
        try:
            message = 'Your order confirmation code is: %s' % (bundle.data['hash'])
            NerdeezResource.send_sms(user_profile.phone, message)
        except Exception,e:
            return self.create_response(bundle.request, {
                    'success': False,
                    'message': "Failed to send the sms",
                    'exception': e.message
                    }, HttpApplicationError)
            
        return super(TransactionResource, self).obj_create(bundle, **kwargs)
    
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
    user_profile = fields.ToOneField(UserProfileResource, 'user_profile', null=True, full=False)
    deal = fields.ToOneField(DealResource, 'deal', null=True, full=False)
    
    class Meta(NerdeezResource.Meta):
        queryset = UnpaidTransaction.objects.all()
        authentication = NerdeezApiKeyAuthentication()
        authorization = NerdeezOnlyOwnerCanReadAuthorization()
        allowed_methods = ['get', 'post']
        
    def hydrate(self, bundle):
        bundle.data['status'] = 1
        bundle.data['user_profile'] = API_URL + 'userprofile/' + str(bundle.request.user.profile.id) + '/'
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
        
        #get the params
        post = simplejson.loads(request.body)
        password = post.get('password')
        email = post.get('email')
        
        #get the user with that email address
        try:
            user = User.objects.get(email=email)
        except:
            return self.create_response(request, {
                    'success': False,
                    'message': 'Invalid email or password',
                    }, HttpUnauthorized )
        
        user = auth.authenticate(username=user.username, password=password)
        if user is None:
            return self.create_response(request, {
                    'success': False,
                    'message': 'Invalid email or password',
                    }, HttpUnauthorized )
        if not user.is_active:
            return self.create_response(request, {
                    'success': False,
                    'message': 'Account not activated',
                    }, HttpUnauthorized )
                    
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        
        #successfull login delete all the old api key of the user and create a new one
        #api_keys = ApiKey.objects.filter(user=user)
        #api_keys.delete()
        api_key, created = ApiKey.objects.get_or_create(user=user)
        api_key.save()

        ur = UserProfileResource()
        ur_bundle = ur.build_bundle(obj=user.profile, request=request)
        return self.create_response(request, {
                    'success': True,
                    'message': 'Successfully logged in',
                    "user_profile": json.loads(ur.serialize(None, ur.full_dehydrate(ur_bundle), 'application/json')),
                    'api_key': api_key.key,
                    'username': user.username
                    }, HttpAccepted )
        
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
        
        #create the username
        api_key = ApiKey()
        username = api_key.generate_key()[0:30]
        password = api_key.generate_key()[0:30]
        
        #set the request post to contain email password and username
        post_values = {}
        post_values['username'] = username
        post_values['password1'] = password
        post_values['password2'] = password
        post_values['email'] = email
        
        #is the email already exists?
        try:
            user = User.objects.get(email=email)
            return self.create_response(request, {
                    'success': False,
                    'message': 'User with this mail address already exists',
                    }, HttpConflict )
        except:
            pass
        
        #validation success
        user_form = UserCreateForm(post_values)
        if user_form.is_valid():
            
            #create the user
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username,
                                password=password)
            login(request, user)
            user.is_active = False
            user.save()
            
            #create the business 
            business = Business()
            business.title = title
            business.business_number = business_number
            business.phone = phone
            if city != None:
                business.city = City.objects.get(id=city)
            business.address = address
            business.save()
            user_profile = user.profile
            user_profile.business = business
            user_profile.save()
            
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
                    'message': [(k, v[0]) for k, v in user_form.errors.items()],
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
                 success - 201 if created containing the following details
                 {
                     success: true
                     message: 'registered a new device'
                     api_key: 'api key for the user'
                     username: 'username of the user'    
                 }
                 success - 202 if user exists containing the following details
                 {
                     success: true
                     message: 'user is already registered'
                     api_key: 'api key for the user'
                     username: 'username of the user'    
                 }
                  
        '''
        #get the params
        post = simplejson.loads(request.body)
        uuid = post.get('uuid')
        
        #find a user profile with this uuid if none exist than create one
        try:
            user_profile = UserProfile.objects.get(uuid=uuid)
            user = user_profile.user
            is_created = False
        except:
            #create the username
            api_key = ApiKey()
            username = api_key.generate_key()[0:30]
            password = api_key.generate_key()[0:30]
            user = User()
            user.username = username
            user.set_password(password)
            user.is_active = True
            user.save()
            user_profile = UserProfile()
            user_profile.uuid = uuid
            user_profile.user = user
            user_profile.save()
            is_created = True
            
        #create a new api key for the user
        api_keys = ApiKey.objects.filter(user=user)
        api_keys.delete()
        api_key, created = ApiKey.objects.get_or_create(user=user)
        api_key.save()
        
        if is_created:
            return self.create_response(request, {
                    'success': True,
                    'message': "registered a new device",
                    'api_key': api_key.key,
                    'username': user.username
                    }, HttpCreated)
        else:
            return self.create_response(request, {
                    'success': True,
                    'message': "user is already registered",
                    'api_key': api_key.key,
                    'username': user.username
                    }, HttpAccepted)
            
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
        business = user_profile.business
        if business == None:
            return self.create_response(request, {
                    'success': False,
                    'message': 'You are not authorized for this action'
                    }, HttpUnauthorized)
            
        #find a userprofile with this phone
        try:
            customer = UserProfile.objects.get(phone=phone)
        except:
            return self.create_response(request, {
                    'success': False,
                    'message': "I didn't find this user"
                    }, HttpNotFound)
            
        #paid transaction
        
        
        try:
            transaction = Transaction.objects.get(user_profile=customer, hash=hash)
            transaction.status = 3
            is_unpaid = False
        except:
            pass
        
        #unpaid transaction
        try:
            transaction = UnpaidTransaction.objects.get(user_profile=customer, hash=hash)
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
        if transaction.deal.business.id != business.id:
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