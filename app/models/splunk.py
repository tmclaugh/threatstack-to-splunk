'''Splunk model'''

from app.errors import AppBaseError
import config
import json
import logging
from splunk_handler import SplunkHandler

_logger = logging.getLogger(__name__)

SPLUNK_HEC_TOKEN = config.SPLUNK_HEC_TOKEN
SPLUNK_SOURCE_TYPE = config.SPLUNK_SOURCE_TYPE
SPLUNK_HOST = config.SPLUNK_HOST
SPLUNK_PORT = config.SPLUNK_PORT

class SplunkBaseError(AppBaseError):
    '''Base Splunk Exception class'''

class SplunkRequestErrorError(Exception):
    '''Splunk request error'''

class SplunkAPIError(Exception):
    '''Splunk API error'''

class SplunkModel(object):
    def __init__(self,
                splunk_host=SPLUNK_HOST,
                splunk_port=SPLUNK_PORT,
                splunk_token=SPLUNK_HEC_TOKEN,
                splunk_source_type=SPLUNK_SOURCE_TYPE,
                splunk_verify=False):

        self.splunk_host = splunk_host
        self.splunk_port = splunk_port
        self.splunk_source_type = splunk_source_type
        self.splunk_token = splunk_token
        self.splunk_verify = splunk_verify

    def is_avaialble(self):
        return True

    def put_alert_event(self, alert, hostname, source):
        splunk_handler = SplunkHandler(
            host=self.splunk_host,
            port=self.splunk_port,
            token=self.splunk_token,
            hostname=hostname,
            index='main',
            source=source,
            sourcetype=self.splunk_source_type,
            verify=self.splunk_verify,
            record_time="__import__('json').loads(record.msg).get('created_at')/1000",
            flush_interval = 0
        )
        splunk_logger = logging.getLogger('splunk_hec')
        splunk_logger.addHandler(splunk_handler)
        splunk_logger.warning(json.dumps(alert))

        return

