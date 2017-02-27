'''
Assemble our service.
'''
import config
from flask import Flask
import logging

_logger = logging.getLogger(__name__)

def _initialize_blueprints(application):
    '''
    Register Flask blueprints
    '''
    from app.views.splunk import splunk
    application.register_blueprint(splunk, url_prefix='/api/v1/splunk')

def _initialize_errorhandlers(application):
    '''
    Initialize error handlers
    '''
    from app.errors import errors
    application.register_blueprint(errors)

def create_app():
    '''
    Create an app by initializing components.
    '''
    _logger.info('Initializing application')
    application = Flask(__name__)

    _initialize_errorhandlers(application)
    _initialize_blueprints(application)

    # Do it!
    return application

