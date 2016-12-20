# -*- coding: utf-8 -*-

from .pswd import LOCAL_DB_NAME, LOCAL_DB_USER, LOCAL_DB_PASS

DEBUG = True
ALLOWED_HOSTS = ['*']

################################################################################
# Database
################################################################################
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': LOCAL_DB_NAME,
		'USER': LOCAL_DB_USER,
		'PASSWORD': LOCAL_DB_PASS,
		'HOST': '127.0.0.1',
		'PORT': '3306'
	}
}

################################################################################
