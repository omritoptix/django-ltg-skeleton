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

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin constants
#===============================================================================

BASE_API_URL = 'https://api.hubapi.com'
CONTACT_API = '/contacts/v1/contact/vid/%s/profile?'
CONTACT_LIST_API = '/contacts/v1/lists/%s/contacts/all?'
API_KEY_QUERY_STRING = 'hapikey=%s'

#===============================================================================
# end constants
#===============================================================================

#===============================================================================
# begin client
#===============================================================================

class HubSpotClient(object):
    '''
    will be used as a portal for the hubspot api
    '''
       
    def __init__(self, api_key):
        # init the client with the hubspot api_key
        self._api_key = api_key
        
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
            req = requests.get((BASE_API_URL + CONTACT_API + API_KEY_QUERY_STRING) % (contact_id, self._api_key))
            if req.ok:
                # return a parsed contact json
                contact_json = req.json()
                return self._parse_contact(**contact_json)
            else:
                raise Exception                
        except:
            pass
        
    def get_contact_list(self,list_id):
        '''
        will return a list containing parsed contacts dicts by using hubspot api as it's data source
        @param list_id str: the list id we want to return contact for
        @return: list containing parsed contacts dicts
        '''
        try:
            # call the hubspot contact list api
            req = requests.get((BASE_API_URL + CONTACT_LIST_API + API_KEY_QUERY_STRING) % (list_id, self._api_key))
            if req.ok:
                #popluate our results list with parsed contacts dicts
                results =[]
                contacts_json = req.json()['contacts']
                for contact in contacts_json:
                    results.append(self._parse_contact(**contact))
                return results
            else:
                raise Exception                
        except:
            pass
        
#===============================================================================
# end client
#===============================================================================

