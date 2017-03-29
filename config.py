import os
THREATSTACK_API_KEY = os.environ.get('THREATSTACK_API_KEY')
THREATSTACK_BASE_URL = os.environ.get('THREATSTACK_BASE_URL', 'https://app.threatstack.com/api/v1')

SPLUNK_HOST = os.environ.get('SPLUNK_HOST')
SPLUNK_PORT = int(os.environ.get('SPLUNK_PORT', 8088))
SPLUNK_HEC_TOKEN = os.environ.get('SPLUNK_HEC_TOKEN')
SPLUNK_SOURCE_TYPE = os.environ.get('SPLUNK_SOURCE_TYPE', 'threatstack')

