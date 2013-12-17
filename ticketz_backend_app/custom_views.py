'''
will hold custom views

Created on Dec 16, 2013
@author: omri
@version : 1.0
@company : Nerdeez.com
'''

#===============================================================================
# begin imports
#===============================================================================

from django.views.generic import View
from ticketz_backend_app.decorators import BusinessLoginRequired
from django.utils.decorators import method_decorator
from django.template.loader import get_template
from django.template.context import Context
import pdfcrowd
from django.conf import settings
from django.http import HttpResponse
from ticketz_backend_app.models import BusinessProfile

#===============================================================================
# end imports
#===============================================================================


class ReportView(View):
    '''
    parent view for a report.
    each report must inherit from this view.
    '''
    #will hold the pdfcrowd client
    client = pdfcrowd.Client(settings.PDFCROWD_USERNAME, settings.PDFCROWD_APIKEY)
    #will hold the business profile for the report
    business_profile = None
    
    @method_decorator(BusinessLoginRequired)
    def dispatch(self, *args, **kwargs):
        
        #call parent dispatch
        return super(ReportView, self).dispatch(*args, **kwargs)
    
    def init_report(self,request,*args,**kwars):
        '''
        will init the business profile 
        and the pdf report client
        '''      
        #get the user and user profile
        user = request.user
        user_profile = user.get_profile()
         
        #get the business profile for this report
        self.business_profile = BusinessProfile.objects.get(user_profile__id = user_profile.id)
        
        #set pdf width height and margin
        self.client.setPageWidth("8.5in")
        self.client.setPageHeight("11in")
        self.client.setPageMargins("0.5in", "0.00in", "0.2in", "0.00in")
        
        #set footers and headers
        footer_template = get_template('report_footer.html')
        footer_html = footer_template.render(Context({})).encode('utf-8')
        header_template = get_template('report_header.html')
        header_html = header_template.render(Context({})).encode('utf-8')
        self.client.setDefaultTextEncoding('utf-8')
        self.client.setFooterHtml(footer_html)
        self.client.setHeaderHtml(header_html)

        
    def render_report(self,html):
        '''
        will get an html template to render
        and will return a rendered report
        @param {html} - html - the html page to convert to pdf
        '''
        try:
            
            #get the api client
            pdf = self.client.convertHtml(html)
            
            # set HTTP response headers
            response = HttpResponse(mimetype="application/pdf")
            response["Cache-Control"] = "no-cache"
            response["Accept-Ranges"] = "none"
            #response["Content-Disposition"] = "attachment; filename=google_com.pdf"
    
            # send the generated PDF
            response.write(pdf)
            
        except pdfcrowd.Error, why:
            response = HttpResponse(mimetype="text/plain")
            response.write(why)
            
        finally:
            return response