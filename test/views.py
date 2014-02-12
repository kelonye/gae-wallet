
import os
import time
from cgi import escape

from google.appengine.dist import use_library
use_library('django', '1.2')
os.environ['DJANGO_SETTINGS_MODULE'] = '__init__'

import webapp2 as webapp
from webapp2_extras import sessions
from google.appengine.ext.webapp import template

from models import *


sessions.default_config['secret_key'] = '-- secret key --'


class View(webapp.RequestHandler):

    def dispatch(self):

        self.session_store = sessions.get_store(
            request=self.request
        )
        try:
            webapp.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp.cached_property
    def session(self):
        return self.session_store.get_session()


class PayView(View):

    def get(self):

        curr_time = int(time.time())
        exp_time = curr_time + 3600

        request_info = {
            'currencyCode': 'USD',
            'sellerData': 'Custom Data'
        }

        jwt_info = {
            'iss': SELLER_ID,
            'aud': 'Google',
            'typ': 'google/payments/inapp/item/v1',
            'iat': curr_time,
            'exp': exp_time,
            'request': request_info
        }

        # create JWT for first item
        request_info.update({
            'name': 'Golden Gate Bridge Aniversary',
            'price': '20.00'
        })
        token_1 = jwt.encode(jwt_info, SELLER_SECRET)

        # create JWT for second item
        request_info.update({
            'name': 'Drive Inn Aniversary', 
            'price': '25.00'
        })
        token_2 = jwt.encode(jwt_info, SELLER_SECRET)

        # update store web page
        template_values = {
            'jwt_1': token_1,
            'jwt_2': token_2
        }

        path = os.path.join(
            os.path.dirname(__file__), 'template.html'
        )
        self.response.out.write(template.render(path, template_values))



class MainHandler(webapp.RequestHandler):
  """Handles /"""

  def get(self):
    """Handles get requests."""

    curr_time = int(time.time())
    exp_time = curr_time + 3600

    request_info = {'currencyCode': 'USD',
                    'sellerData': 'Custom Data'}
    jwt_info = {'iss': SELLER_ID,
                'aud': 'Google',
                'typ': 'google/payments/inapp/item/v1',
                'iat': curr_time,
                'exp': exp_time,
                'request': request_info}

    # create JWT for first item
    request_info.update({'name': 'Golden Gate Bridge Aniversary', 'price': '20.00'})
    token_1 = jwt.encode(jwt_info, SELLER_SECRET)

    # create JWT for second item
    request_info.update({'name': 'Drive Inn Aniversary', 'price': '25.00'})
    token_2 = jwt.encode(jwt_info, SELLER_SECRET)

    # update store web page
    template_vals = {'jwt_1': token_1,
                     'jwt_2': token_2}

    path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    self.response.out.write(template.render(path, template_vals))


class PostbackHandler(webapp.RequestHandler):

    def post(self):

        encoded_jwt = self.request.get('jwt', None)
        if encoded_jwt is not None:

          decoded_jwt = jwt.decode(str(encoded_jwt), SELLER_SECRET)

          if decoded_jwt['iss'] == 'Google' and decoded_jwt['aud'] == SELLER_ID:
            if ('response' in decoded_jwt and
                'orderId' in decoded_jwt['response'] and
                'request' in decoded_jwt):
              order_id = decoded_jwt['response']['orderId']
              request_info = decoded_jwt['request']
              if ('currencyCode' in request_info and 'sellerData' in request_info
                  and 'name' in request_info and 'price' in request_info):
                # optional - update local database
                
                # respond back to complete payment
                self.response.out.write(order_id)


urls = [
    ('/', PayView),
    ('/postback', PostbackHandler),
]

app = webapp.WSGIApplication(urls, debug=True)
