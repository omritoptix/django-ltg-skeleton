'''
Client to interact with hubspot api
Created on April 9, 2014

@author:Omri Dagan
@version: 1.0
@copyright: LTG
'''

#===============================================================================
# begin imports
#===============================================================================

import requests
import logging
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpApplicationError
import json
from django.contrib.auth import get_user_model

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin constants
#===============================================================================

BASE_API_URL = 'https://api.hubapi.com'
GET_CONTACT_API = '/contacts/v1/contact/vid/%s/profile?'
GET_CONTACT_LIST_API = '/contacts/v1/lists/%s/contacts/all?'
CREATE_CONTACT_API = '/contacts/v1/contact/?'
UPDATE_CONTACT_API = '/contacts/v1/contact/vid/%d/profile?'
ADD_CONTACT_TO_LIST = '/contacts/v1/lists/%s/add?'
API_KEY_QUERY_STRING = 'hapikey=%s'

#===============================================================================
# end constants
#===============================================================================

#===============================================================================
# begin globals
#===============================================================================

# set global logger to be root logger
logger = logging.getLogger()

#===============================================================================
# end globals
#===============================================================================

#===============================================================================
# begin client
#===============================================================================

class HubSpotClientError(Exception):
    pass

class HubSpotClient(object):
    '''
    will be used as a portal for the hubspot api
    '''
       
    def __init__(self, api_key):
        '''
        init the client with a hubspot api_key
        '''
        self._api_key = api_key
        
    def _handle_exception(self,message):
        '''
        will handle our client exceptions by prefixing it with
        message info and logging it
        @param message str: an exception message
        @return str: a prefixed message
        '''
        exception_message = "HubSpot api client Exception: " + message
        logger.exception(exception_message)
        return exception_message
    
    def _request_handler(self,url,method='get',data=None,headers=None):
        '''
        will handle our client api calls
        @param method str: the method for the request (right now supports 'post','get')
        @param url str: the url to which will make the api request
        @param data str: the data for the request
        @param headers str: the headers for the request
        @return resp requests.models.Response : response object  
        '''
        if (method=='get'):
            resp = requests.get(url,data=data,headers=headers)
        if (method=='post'):
            resp = requests.post(url,data=data,headers=headers)
            
        if resp.ok:
            return resp
        else:
            resp.raise_for_status()
        
    def _parse_contact(self,**kwargs):
        '''
        will build a data dictionary containing a contact information.
        @param kwargs: json contact object from hubspot api
        @return: a dictionary with contact details
        '''
        data ={}
        data['id'] = kwargs['vid']
        properties = kwargs['properties']
        data['first_name'] = properties.get('firstname',{}).get('value')
        data['last_name'] = properties.get('lastname',{}).get('value')
        data['file_upload'] = properties.get('file_upload',{}).get('value')
        data['email'] = properties.get('email',{}).get('value')
        data['skype_id'] = properties.get('skype_id',{}).get('value')
        data['tutor_description'] = properties.get('tutor_description',{}).get('value')
        data['tutor_rate'] = properties.get('tutor_rate',{}).get('value')
        data['tutor_video'] = properties.get('tutor_video',{}).get('value')
        data['tutor_speciality'] = properties.get('tutor_speciality',{}).get('value')
        data['tutor_groups'] = properties.get('tutor_groups',{}).get('value')
        data['country'] = properties.get('country',{}).get('value')
        return data
        
    def get_contact(self,contact_id):
        '''
        will return a parsed contact dict by using hubspot contact api as it's data source.
        @param str contact_id:the contact we want to build dict for
        @return: a dictionary with contact details
        '''
        try:
            # call the hubspot contact api
            resp = self._request_handler((BASE_API_URL + GET_CONTACT_API + API_KEY_QUERY_STRING) % (contact_id, self._api_key))
            # return a parsed contact json
            contact_json = resp.json()
            return self._parse_contact(**contact_json)
        
        except Exception as e:
            raise ImmediateHttpResponse(HttpApplicationError(self._handle_exception(e.message)))
        
        
    def get_contact_list(self,list_id):
        '''
        will return a list containing parsed contacts dicts by using hubspot api as it's data source
        @param list_id str: the list id we want to return contact for
        @return: list containing parsed contacts dicts
        '''
        try:
            # call the hubspot contact list api
            resp = self._request_handler((BASE_API_URL + GET_CONTACT_LIST_API + API_KEY_QUERY_STRING) % (list_id, self._api_key))
            #popluate our results list with parsed contacts dicts
            results =[]
            contacts_json = resp.json()['contacts']
            for contact in contacts_json:
                results.append(self._parse_contact(**contact))
            return results
               
        except Exception as e:
            raise ImmediateHttpResponse(HttpApplicationError(self._handle_exception(e.message)))
        
    def add_contact(self,user,list_id,*properties,**extra_properties):
        """
        will create a contact in hubspot and add it to a given list
        @param user: the auth user model of our app
        @param list_id: the list id which will add the user after creation
        @param properties: properties to add to the hubspot contact on creation.
        @param extra_properties: extra properties to add to the hubspot contact on creation.
        @return: void
        
        # note : properties names must exist in hubspot or else a 400 will be raised. 
        """
        # add the user to hubspot
        try:
            properties = self._build_user_properties_list(user.id,*properties,**extra_properties)
            # create the data object for the post request
            data = json.dumps({'properties':properties})
            # set request headers
            headers = {'content-type': 'application/json'}
            # set the url
            url = (BASE_API_URL + CREATE_CONTACT_API + API_KEY_QUERY_STRING) % self._api_key 
            # call the hubspot request handler
            resp = self._request_handler(url=url,method="post", data=data, headers=headers)
            contact_json = resp.json()
            # save hubspot contact id to the user
            user.hubspot_contact_id = contact_json['vid']
            user.save()
        
        except Exception as e:
            raise ImmediateHttpResponse(HttpApplicationError(self._handle_exception(e.message)))
        
        # add the recently created contact to a list
        self._add_contact_to_list(contact_id = contact_json['vid'], list_id=list_id)
        
    def update_contact(self,user,*properties,**extra_properties):
        """
        will update a contact in hubspot.
        @param user: the auth user model of our app
        @param properties: properties to update on hubspot
        @return: void
        """
        try:
            properties = self._build_user_properties_list(user.id,*properties,**extra_properties)
            # create the data object for the post request
            data = json.dumps({'properties':properties})
            # set request headers
            headers = {'content-type': 'application/json'}
            # check user has a hubspot contact id
            if user.hubspot_contact_id is None:
                raise ImmediateHttpResponse(HttpApplicationError(self._handle_exception("can't update hubpost contact since user's hubspot_contact_id field is null")))
            
            # set the url
            url = (BASE_API_URL + UPDATE_CONTACT_API + API_KEY_QUERY_STRING) % (user.hubspot_contact_id, self._api_key) 
            # call the hubspot request handler
            self._request_handler(url=url,method="post", data=data, headers=headers)
        
        except Exception as e:
            raise ImmediateHttpResponse(HttpApplicationError(self._handle_exception(e.message)))

        
    def _add_contact_to_list(self,contact_id,list_id):
        """
        will add a contact to a list
        @param contact_id: the contact id
        @param list_id: the list id we want to add the contact to
        @return:void
        """
        try:
            # set the request payload
            data = json.dumps({'vids':[contact_id]})
            # set request headers
            headers = {'content-type': 'application/json'}
            # set the url
            url = (BASE_API_URL + ADD_CONTACT_TO_LIST + API_KEY_QUERY_STRING) % (list_id,self._api_key)
            # call the hubspot request handler
            self._request_handler(url=url,method="post", data=data, headers=headers)
    
        except Exception as e:
            raise ImmediateHttpResponse(HttpApplicationError(self._handle_exception(e.message)))
        
    def _build_user_properties_list(self,user_id,*properties,**extra_properties):
        """
        will build properties list according to hubspot convention for a specific user
        @param user_id: the id of the user
        @param properties: properties list
        @param extra_properties: extra properties list
        """
        # build properties as kwargs
        properties_kwargs = get_user_model().objects.filter(id=user_id).values(*properties)[0]
        # if there is any extra kwargs, add it
        properties_kwargs.update(**extra_properties)
        # build properties according to hubspot convention
        return self._build_properties_list(**properties_kwargs)
        
    
    def _build_properties_list(self,**properties):
        """
        will be used to build properties list for the hubspot api
        @return: list of properties matching hubspot convention
        """
        properties_list = []
        
        for key, value in properties.iteritems():
            contact_property = {}
            contact_property['property'] = key
            contact_property['value'] = value
            properties_list.append(contact_property)
        
        return properties_list
        
#===============================================================================
# end client
#===============================================================================

