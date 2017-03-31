'''Splunk model'''

from app.errors import AppBaseError
import config
import json
import logging
import requests
import six
import sys

_logger = logging.getLogger(__name__)

SPLUNK_HEC_TOKEN = config.SPLUNK_HEC_TOKEN
SPLUNK_SOURCE_TYPE = config.SPLUNK_SOURCE_TYPE
SPLUNK_BASE_URL = config.SPLUNK_BASE_URL
SPLUNK_SSL_VERIFY = config.SPLUNK_SSL_VERIFY

class SplunkBaseError(AppBaseError):
    '''Base Splunk Exception class'''

class SplunkRequestError(SplunkBaseError):
    '''Splunk request error'''

class SplunkAPIError(SplunkBaseError):
    '''Splunk request error'''

class SplunkModel(object):
    def __init__(self,
                splunk_base_url=SPLUNK_BASE_URL,
                splunk_token=SPLUNK_HEC_TOKEN,
                splunk_source_type=SPLUNK_SOURCE_TYPE,
                splunk_ssl_verify=SPLUNK_SSL_VERIFY):

        self.splunk_base_url = splunk_base_url
        self.splunk_source_type = splunk_source_type
        self.splunk_token = splunk_token
        self.splunk_ssl_verify = splunk_ssl_verify

    def _make_splunk_request(self, request_type, path, json_data=None):
        '''Make requests to splunk'''
        url = ''.join([self.splunk_base_url, path])
        headers = {'Authorization':'Splunk {}'.format(self.splunk_token)}
        try:
            resp = requests.request(
                request_type,
                url,
                headers=headers,
                verify=self.splunk_ssl_verify,
                json=json_data,
            )

        except requests.exceptions.RequestException as e:
            exc_info = sys.exc_info()
            if sys.version_info >= (3,0,0):
                raise SplunkRequestError(e).with_traceback(exc_info[2])
            else:
                six.reraise(
                    SplunkRequestError,
                    SplunkRequestError(e),
                    exc_info[2]
                )

        if not resp.ok:
            if 'application/json' in resp.headers.get('Content-Type'):
                raise SplunkAPIError(
                    resp.reason,
                    resp.status_code,
                    resp.json()
                )
            else:
                raise SplunkRequestError(resp.reason, resp.status_code)

        return resp.json()


    def is_available(self):
        '''Check if Splunk is available'''
        # This is enough to check connection and token validity
        path = '/services'

        return self._make_splunk_request('GET', path)


    def put_alert_event(self,
                        alert,
                        hostname,
                        source,
                        source_type=SPLUNK_SOURCE_TYPE):
        '''Send an alert to Splunk'''
        path = '/services/collector'

        splunk_data = {
            'time': alert.get('created_at')/1000,
            'host': hostname,
            'index': 'main',
            'source': source,
            'sourcetype': source_type,
            'event': json.dumps(alert)
        }

        return self._make_splunk_request('POST', path, splunk_data)

