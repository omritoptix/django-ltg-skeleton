# '''
# will hold our celery settings module
# Created on May 12, 2014
# 
# @author: Omri Dagan
# @version: 1.0
# @copyright: LTG
# '''
# 
# ## Broker settings.
# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# 
# # List of modules to import when celery starts.
# CELERY_IMPORTS = ('ltg_backend_app.tasks', )
# 
# ## Using the database to store task state and results.
# CELERY_RESULT_BACKEND = 'redis://localhost/0'
# 
# # celery task serializer
# CELERY_TASK_SERIALIZER = 'json'
# 
# # celery result serializer. default is pickle
# CELERY_RESULT_SERIALIZER = 'json'
# 
# # celery accept content format
# CELERY_ACCEPT_CONTENT=['json']
# 
# # celery enable utc for backward compatability. if set to false, system timezone will be used.
# CELERY_ENABLE_UTC = True