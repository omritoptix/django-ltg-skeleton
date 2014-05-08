'''
will hold Base model for all of our model resources and globals defenitions
Created on April 22, 2014
 
@author: Yariv Katz & Omri Dagan
@version: 1.0
@copyright: LTG
'''


#===============================================================================
# begin imports
#===============================================================================


from tastypie import fields
from django.core.urlresolvers import get_script_prefix, resolve
import os
import logging
from tastypie.resources import ModelResource
from ltg_backend_app.third_party_subclasses.tastypie_subclasses import MyDateSerializer

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin abstract base resource
#===============================================================================

class LtgResource(ModelResource):
    '''
    abstract class with commone attribute common to all my rest models
    '''
    creation_date = fields.DateTimeField(attribute='creation_date',readonly=True)
    modified_data = fields.DateTimeField(attribute='modified_data',readonly=True)
    
    #set read only fields
    class Meta:
        allowed_methods = ['get']
        always_return_data = True
        ordering = ['creation_date','modified_date']
        serializer = MyDateSerializer()
        
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
    
    def obj_create(self, bundle, **kwargs):
        # if the calling class an attr of 'user_profile', create the resource with the request.user as the user for the resource
        if hasattr(self, 'user_profile'):
            return super(LtgResource, self).obj_create(bundle, user_profile=bundle.request.user.profile)
        else:
            return super(LtgResource, self).obj_create(bundle)
        return bundle
            
#===============================================================================
# end abstract base resources
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
# begin globals
#===============================================================================

# set global logger to be root logger
logger = logging.getLogger()

#===============================================================================
# end globals
#===============================================================================