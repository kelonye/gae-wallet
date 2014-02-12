import os
import sys
from datetime import datetime, date, tzinfo, timedelta
from google.appengine.ext import ndb
from google.appengine.ext import deferred
from google.appengine.api import urlfetch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "lib")))

import jwt

SELLER_ID = 'AIzaSyBxBp3-63JbaLMfxlsi_QELYpW_A6OMwxg'

SELLER_SECRET = ''

