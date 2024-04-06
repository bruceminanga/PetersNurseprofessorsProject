import os
from .base import *


DEBUG = False

ADMINS = [
    ('Bruce Minanga', 'bruceminanga@gmail.com'),
]

ALLOWED_HOSTS = ['nurseprofessors.com', 'www.nurseprofessors.com']

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': os.environ.get('POSTGRES_DB'),
       'USER': os.environ.get('POSTGRES_USER'),
       'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
       'HOST': 'db',
       'PORT': 5432,
   }
}
