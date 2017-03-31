import os
THREATSTACK_API_KEY = os.environ.get('THREATSTACK_API_KEY')
THREATSTACK_BASE_URL = os.environ.get('THREATSTACK_BASE_URL', 'https://app.threatstack.com/api/v1')

# SPLUNK_BASE_URL="https://<HOSTNAME>:8088"
SPLUNK_BASE_URL = os.environ.get('SPLUNK_BASE_URL')
SPLUNK_SSL_VERIFY = bool(int(os.environ.get('SPLUNK_SSL_VERIFY', 1)))
SPLUNK_HEC_TOKEN = os.environ.get('SPLUNK_HEC_TOKEN')
SPLUNK_SOURCE_TYPE = os.environ.get('SPLUNK_SOURCE_TYPE', 'threatstack')

