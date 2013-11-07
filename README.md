nerdeez-backend
==============

Backend project for the 90 minute ticket sell application

## Enviroment Variables

The enviroment variables are specified in the settings.py file and consist of the following:
* IS_DEBUG: TRUE/FALSE determine if we are in debug mode (Default: TRUE)
* ADMIN_MAIL: <String> the admin mail address (Default: yariv@nerdeez.com)
* TWITTER_SECRET: <string> the twitter secret key used for interaction with twitter (Default: '')
* TWITTER_KEY: <string> twitter public key (Default: '')
* FACEBOOK_APP_ID: <string> facebook application key (Default: '')
* FACEBOOK_APP_SECRET: <string> (Default: '')
* SENDGRID_USERNAME: <string> supplied by heroku to send mail
* SENDGRID_PASSWORD: <string> supplied by heroku to send mails
* TICKETZ_ENV_AWS_ACCESS_KEY_ID: <String> used to connect to s3 (Default: '')
* TICKETZ_ENV_AWS_SECRET_ACCESS_KEY: <String> used to connect to s3 (Default: '')
* TICKETZ_ENV_AWS_STORAGE_BUCKET_NAME: <String> used to connect to s3 (Default: '')
* FROM_EMAIL_ADDRESS: <String> when sending mail the return address (Default: noreply@nerdeez.com)

## API

We run a rest server with the following api:

###### UserProfile

- only get or put are allowed here
- get and put are allowed only with api key cradentials

###### Region

- we allow only get here
- basic authentication

###### City

- we allow only get here
- basic authentication

###### UserPrefrence

- only get or put are allowed here
- get and put are allowed only with api key cradentials

###### Category

- we allow only get here
- basic authentication

###### Business

- we allow only get here
- api key authentication if you want to read

###### Utilities

- we allow only post
- right now only contact is supported which send a mail to the admin

## Admin interface

located in the url /admin/
password to access was send to your mail account



