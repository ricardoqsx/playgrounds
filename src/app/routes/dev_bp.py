# debug_logging.py
from flask import Blueprint, current_app, request
import logging

debug_bp = Blueprint('debug_bp', __name__)

def log_request_info():
    current_app.logger.debug("Cabeceras de solicitud: %s", request.headers)
    content_type = request.headers.get('Content-Type', '').lower()
    
    if request.content_length and request.content_length > 1024:
        current_app.logger.debug("Cuerpo de solicitud: [demasiado grande]")
    elif 'application/json' in content_type:
        current_app.logger.debug("Cuerpo de solicitud (JSON): %s", request.get_json())
    else:
        current_app.logger.debug("Cuerpo de solicitud: [omitido]")

def log_response_info(response):
    current_app.logger.debug("Cabeceras de respuesta: %s", response.headers)
    content_type = response.headers.get('Content-Type', '').lower()
    
    if 'text/html' in content_type:
        current_app.logger.debug("Cuerpo de respuesta: [HTML omitido]")
    elif not response.is_streamed:
        body = response.get_data(as_text=True)
        current_app.logger.debug("Cuerpo de respuesta: %s", body)
    
    return response

@debug_bp.record_once
def register_debug_handlers(state):
    app = state.app
    logging.basicConfig(level=logging.DEBUG)
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.DEBUG)
    app.before_request(log_request_info)
    app.after_request(log_response_info)


# Para mostrar el debug largo, habilitar este codigo y comentar el de arriba
"""
# debug_logging.py
from flask import Blueprint, current_app, request
import logging

debug_bp = Blueprint('debug_bp', __name__)

def log_request_info():
    current_app.logger.debug("Cabeceras de solicitud: %s", request.headers)
    if request.content_length and request.content_length < 1024:
        current_app.logger.debug("Cuerpo de solicitud: %s", request.get_data(as_text=True))
    else:
        current_app.logger.debug("Cuerpo de solicitud: (stream o grande)")

def log_response_info(response):
    current_app.logger.debug("Cabeceras de respuesta: %s", response.headers)
    if not response.is_streamed:
        body = response.get_data(as_text=True)
        current_app.logger.debug("Cuerpo de respuesta: %s", body)
    return response

@debug_bp.record_once
def register_debug_handlers(state):
    app = state.app
    logging.basicConfig(level=logging.DEBUG)
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.DEBUG)
    app.before_request(log_request_info)
    app.after_request(log_response_info) """