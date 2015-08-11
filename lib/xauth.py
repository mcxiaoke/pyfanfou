# coding: utf8
import oauth2
import urllib
import urlparse


class AuthError(Exception):

    def __init__(self, code, message):
        super(AuthError, self).__init__(code, message)


class AuthClient(object):

    '''
    XAuth Client
    '''

    def __init__(self, consumer_key, consumer_secret, token_url):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.token_url = token_url
        self.consumer = oauth2.Consumer(consumer_key, consumer_secret)

    def get(self, url):
        pass

    def get_access_token(self, username, password):
        client = oauth2.Client(self.consumer)
        client.add_credentials(username, password)
        client.set_signature_method = oauth2.SignatureMethod_HMAC_SHA1()
        resp, body = client.request(
            self.token_url, method='POST', body=urllib.urlencode({
                'x_auth_mode': 'client_auth',
                'x_auth_username': username,
                'x_auth_password': password,
            }))
        if resp['status'] != '200':
            raise AuthError(resp['status'], 'invalid username or password')
        self.token = dict(urlparse.parse_qsl(body))
        return self.token


def test_get_access_token():
    consumer_key = "e5dd03165aebdba16611e1f4849ce2c3"
    consumer_secret = "2a14fcbdebfb936a769840b4d5a9263b"
    token_url = "http://fanfou.com/oauth/access_token"
    client = AuthClient(consumer_key, consumer_secret, token_url)
    access_token = client.get_access_token("test", "test")
    print access_token

if __name__ == '__main__':
    test_get_access_token()
