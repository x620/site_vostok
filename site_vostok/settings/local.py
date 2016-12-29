# -*- coding: utf-8 -*-

import os
from site_vostok.settings import BASE_DIR

DEBUG = True
ALLOWED_HOSTS = ['*']

################################################################################
# Database
################################################################################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
################################################################################
