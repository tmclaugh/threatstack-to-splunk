'''
Send alert events to Splunk.
'''

from flask import Blueprint, jsonify, request
import logging
import app.models.splunk as splunk_model
import app.models.threatstack as threatstack_model
from app.sns import check_aws_sns

_logger = logging.getLogger(__name__)

splunk = Blueprint('splunk', __name__)

#decerator refers to the blueprint object.
@splunk.route('/status', methods=['GET'])
def is_available():
    '''
    Test that Threat Stack and Splunk are reachable.
    '''
    spl = splunk_model.SplunkModel()
    splunk_status = spl.is_available()
    splunk_info = {'success': splunk_status}

    ts = threatstack_model.ThreatStackModel()
    ts_status = ts.is_available()
    ts_info = {'success': ts_status}

    status_code = 200
    if splunk_status and ts_status:
        success = True
    else:
        success = False

    return jsonify(success=success, splunk=splunk_info, threatstack=ts_info), status_code

@splunk.route('/alert', methods=['POST'])
@check_aws_sns
def put_alert():
    '''
    Send Threat Stack alerts to Splunk.
    '''
    webhook_data = request.get_json(force=True)
    for alert in webhook_data.get('alerts'):
        ts = threatstack_model.ThreatStackModel()
        alert_full = ts.get_alert_by_id(alert.get('id'))
        hostname = alert.get('server_or_region')
        source = alert.get('source')

        spl = splunk_model.SplunkModel()
        spl.put_alert_event(alert_full, hostname, source)

    status_code = 200
    success = True
    response = {'success': success}

    return jsonify(response), status_code

