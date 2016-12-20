# -*- coding: utf-8 -*-

from django.conf import settings

if not settings.DEBUG:
	import os

	BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

	# SECURITY WARNING: don't run with debug turned on in production!
	DEBUG = False

	################################################################################
	# Database
	################################################################################
	# from pswd import PRODUCTION_DB_NAME, PRODUCTION_DB_USER, PRODUCTION_DB_PASS
	# DATABASES = {
	# 	'default': {
	# 		'ENGINE': 'django.db.backends.mysql',
	# 		'NAME': LOCAL_DB_NAME,
	# 		'USER': LOCAL_DB_USER,
	# 		'PASSWORD': LOCAL_DB_PASS,
	# 		'HOST': '127.0.0.1',
	# 		'PORT': '3306'
	# 	}
	# }

	################################################################################
