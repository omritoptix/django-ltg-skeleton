'''
will hold our celery init module
Created on May 12, 2014

@author: Omri Dagan
@version: 1.0
@copyright: LTG
'''
#===============================================================================
# begin imports
#===============================================================================

from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
#===============================================================================
# end imports
#===============================================================================

#===============================================================================
# begin celery init
#===============================================================================

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ltg_backend_app.settings')

# init the celery app
app = Celery('ltg_backend_app')


# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

#===============================================================================
# end celery init
#===============================================================================


