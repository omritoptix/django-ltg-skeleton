import traceback
import sys

from django.conf import settings
from ticketz_backend_app.models import Logger

class ProcessExceptionMiddleware(object):
	def process_response(self, request, response):

		if response.status_code >= 400:
			should_print = True
		else:
			should_print = False

		if should_print:
			log = Logger()
			log.path = request.path
			log.post = str(request.POST)
			log.get = str(request.GET)
			log.content = response.content
# 			log.save()

		return response