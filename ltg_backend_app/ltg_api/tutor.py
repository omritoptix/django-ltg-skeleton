'''
will hold our tutor resource
Created on April 22, 2014
 
@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''
#===============================================================================
# begin imports
#===============================================================================

from tastypie.resources import Resource
from tastypie import fields
from ltg_backend_app.models import Tutor
from tastypie.authentication import Authentication
from ltg_backend_app.ltg_api.hubspot_client import HubSpotClient
import settings
from tastypie.bundle import Bundle

#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin tutor resource
#===============================================================================

class TutorResource(Resource):
    '''
    will return all tutors by using hubspot api as it's data source.
    '''
    id = fields.CharField(attribute='id',null=True)
    first_name = fields.CharField(attribute='first_name',null=True)
    last_name = fields.CharField(attribute='last_name', null=True)
    file_upload = fields.CharField(attribute='file_upload', null=True)
    email = fields.CharField(attribute='image_url', null=True)
    skype_id = fields.CharField(attribute='skype_id', null=True)
    tutor_description = fields.CharField(attribute='tutor_description', null=True)
    tutor_rate = fields.CharField(attribute='tutor_rate', null=True)
    tutor_video = fields.CharField(attribute='tutor_video', null=True)
    tutor_speciality = fields.CharField(attribute='tutor_speciality', null=True)
    tutor_groups = fields.CharField(attribute='tutor_groups', null=True)
    country = fields.CharField(attribute='country', null=True)

    class Meta:
        resource_name = 'tutor'
        allowed_methods = ['get']
        object_class = Tutor
        authentication = Authentication()
        
    def _client(self):
        #define our api client
        return HubSpotClient(settings.HUBSPOT_API_KEY)
        
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}
    
        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj['id']
    
        return kwargs
    
    def obj_get(self, request=None, **kwargs):
        result = self._client().get_contact(kwargs['pk'])
        return Tutor(**result)
    
    def get_object_list(self, request):
        list_id = request.GET.get('list_id',settings.HUBSPOT_LIST_ID)
        contact_list = self._client().get_contact_list(list_id)
        
        results = []
        for result in contact_list:
            tutor = Tutor(**result)
            results.append(tutor)
     
        return results
    
    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)
    
    def dehydrate(self,bundle):
        updated_data = {}
        # remove null fields
        for key in bundle.data:
            if (bundle.data[key] is not None):
                updated_data[key] = bundle.data[key]
        
        bundle.data = updated_data
        return super(TutorResource, self).dehydrate(bundle)   

#===============================================================================
# end tutor resource
#=============================================================================== 