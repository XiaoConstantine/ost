import os
os.environ['DJANGO_SETTING_MODULE'] = 'settings'

from google.appengine.dis import use_library
use_library('django','1.4')
