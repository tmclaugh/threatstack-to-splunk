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

@splunk.route('/event', methods=['POST'])
@check_aws_sns
def put_alert():
    '''
    Send Threat Stack alerts to Splunk.
    '''
    splunk_response_list = []
    webhook_data = request.get_json(force=True)
    for alert in webhook_data.get('alerts'):
        ts = threatstack_model.ThreatStackModel()
        alert_full = ts.get_alert_by_id(alert.get('id'))
        if alert_full.get('agent_id'):
            agent = ts.get_agent_by_id(alert_full.get('agent_id'))
            hostname = agent.get('hostname')
        else:
            hostname = None

        spl = splunk_model.SplunkModel()
        splunk_response = spl.put_alert_event(alert_full, hostname)
        splunk_response_list.append(splunk_response)

    status_code = 200
    success = True
    response = {'success': success, 'splunk': splunk_response_list}

    return jsonify(response), status_code

