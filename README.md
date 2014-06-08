django-ltg-skeleton
==============

Django skeleton for ltg projects

## Enviroment Variables

The enviroment variables are specified in the settings.py file and consist of the following:
* IS_DEBUG: TRUE/FALSE determine if we are in debug mode (Default: TRUE)
* ADMIN_MAIL: <String> the admin mail address (Default: admin@ltgexam.com)
* AWS_ACCESS_KEY_ID: <String> used to connect to s3 (Default: '')
* AWS_SECRET_ACCESS_KEY: <String> used to connect to s3 (Default: '')
* AWS_STORAGE_BUCKET_NAME: <String> used to connect to s3 (Default: '')
* FROM_EMAIL_ADDRESS: <String> when sending mail the return address (Default: noreply@ltgexam.com)
* DATABASE_URL: <String> the database url
* DJANGO_SETTINGS_MODULE: <String> path to project settings module
* SENDGRID_USERNAME: <String> the sendgrid username
* SENDGRID_PASSWORD: <String> the sendgrid password



