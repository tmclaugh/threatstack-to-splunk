import os
THREATSTACK_API_KEY = os.environ.get('THREATSTACK_API_KEY')
THREATSTACK_BASE_URL = os.environ.get('THREATSTACK_BASE_URL', 'https://app.threatstack.com/api/v1')

SPLUNK_API_TOKEN = os.environ.get('SPLUNK_API_TOKEN')
SPLUNK_APP_NAME = os.environ.get('SPLUNK_APP_NAME', 'threatstack-to-splunk')
SPLUNK_BASE_URL = os.environ.get('SPLUNK_BASE_URL')

