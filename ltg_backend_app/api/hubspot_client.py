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
        
    def add_contact(self,user,list_id,**kwargs):
        """
        will create a contact in hubspot and add it to a given list
        @param user: the auth user model of our app
        @param list_id: the list id which will add the user after creation
        @return: void
        """
        # add the user to hubspot
        try:
            # build the properties list of the user
            properties = []
            # build properties for the user
            email = self._build_property('email', user.email)
            first_name = self._build_property('firstname', user.first_name)
            last_name = self._build_property('lastname', user.last_name)
            # add properties to the list
            properties.extend([first_name,last_name,email])
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
            
    def _build_property(self,key,value):
        """
        will build property which matches the hubspot api convention
        @param key: the property key, i.e 'email'
        @param value: the property value , i.e 'omri@ltgexam.com'
        @return: dict containing the key value matching the hubspot api property convention  
        """
        contact_property = {}
        contact_property['property'] = key
        contact_property['value'] = value
        return contact_property
    
#===============================================================================
# end client
#===============================================================================

