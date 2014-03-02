'''
Handles registration and login using the facebook service
'''
import random
import urllib
import urlparse
import json
import logging
from gettext import gettext as _

import web

from mypinnings import settings
from mypinnings import template
from mypinnings import session
from mypinnings import database
from mypinnings import auth


urls = ('/register', 'Register',
        '/return', 'Return',
        )

logger = logging.getLogger('facebook')

class Register:
    '''
    Start the facebook login
    '''
    def GET(self):
        '''
        Redirects to facebook login page
        '''
        base_url = 'https://www.facebook.com/dialog/oauth?'
        parameters = {'state': str(random.randrange(99999999)),
                      'client_id': settings.FACEBOOK['application_id'],
                      'redirect_uri': settings.FACEBOOK['login_redirect_uri'],
                      }
        url_redirect = base_url + urllib.urlencode(parameters)
        raise web.seeother(url=url_redirect, absolute=True)

class Return:
    '''
    Manages the return from the facebook login
    '''
    def GET(self):
        '''
        Manages the return from the facebook login
        '''
        error = web.input(error=None)['error']
        if error:
            errors = web.input()
            template.ltpl('facebook/no-login', **errors)
        else:
            self.code = web.input(code=None)['code']
            if self.code:
                if not self._exchange_code_for_access_token():
                    return template.lmsg(_('Invalid facebook login'))
                if not self._obtain_user_profile():
                    return template.lmsg(_('Invalid facebook login'))
                user_id = self._get_user_from_db()
                if not user_id:
                    user_id = self._insert_user_to_db()
                auth.login_user(session.get_session(), user_id)
                raise web.seeother(url='/', absolute=True)
            else:
                return template.lmsg(_('Failure in the OAuth protocol with facebook. Try again'))

    def _exchange_code_for_access_token(self):
        try:
            base_url = 'https://graph.facebook.com/oauth/access_token?'
            parameters = {'client_id': settings.FACEBOOK['application_id'],
                          'client_secret': settings.FACEBOOK['application_secret'],
                          'redirect_uri': settings.FACEBOOK['login_redirect_uri'],
                          'code': self.code,
                          }
            url_exchange = base_url + urllib.urlencode(parameters)
            exchange_data = urllib.urlopen(url=url_exchange).read()
            token_data = urlparse.parse_qs(qs=exchange_data)
            self.access_token = token_data['access_token'][-1]
            self.access_token_expires = token_data['expires'][-1]
            return True
        except:
            logger.error('Cannot exchange code for access token. Code: {}', self.code, exc_info=True)
            return False

    def _obtain_user_profile(self):
        try:
            base_url = 'https://graph.facebook.com/me?'
            parameters = {'access_token': self.access_token}
            url_profile = base_url + urllib.urlencode(parameters)
            self.profile = json.load(urllib.urlopen(url=url_profile))
            return True
        except:
            logger.error('Cannot cannot obtain user profile. Access token: {}', self.access_token, exc_info=True)
            return False

    def _get_user_from_db(self):
        db = database.get_db()
        query_result = db.select(tables='users', where="username=$username",
                                   vars={'username': self.profile['username']})
        for row in query_result:
            self.user_id = row['id']
            return self.user_id
        return False

    def _insert_user_to_db(self):
        values = {'email': self.profile.get('email', ''),
                  'name': self.profile['name'],
                  'username': self.profile['username'],
                  'facebook': self.profile['username'],
                  'hometown': self.profile.get('hometown', {'name': ''}).get('name', ''),
                  }
        db = database.get_db()
        user_id = db.insert(tablename='users', **values)
        return user_id

app = web.application(urls, locals())