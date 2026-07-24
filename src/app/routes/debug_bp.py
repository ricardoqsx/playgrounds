# debug_logging.py
from flask import Blueprint, current_app, g, request
from app.models.debug_db import insert_request_log
import logging
import time

debug_bp = Blueprint('debug_bp', __name__)

SENSITIVE_HEADERS = {'authorization', 'cookie', 'set-cookie', 'x-csrftoken', 'x-csrf-token'}
SENSITIVE_FIELDS = {'password', 'passwd', 'csrf_token', 'token', 'secret'}


def sanitize_headers(headers):
    return {
        key: '[redacted]' if key.lower() in SENSITIVE_HEADERS else value
        for key, value in headers.items()
    }


def sanitize_payload(payload):
    if isinstance(payload, dict):
        return {
            key: '[redacted]' if key.lower() in SENSITIVE_FIELDS else sanitize_payload(value)
            for key, value in payload.items()
        }
    if isinstance(payload, list):
        return [sanitize_payload(item) for item in payload]
    return payload


def get_request_body():
    content_type = request.headers.get('Content-Type', '').lower()

    if request.content_length and request.content_length > 1024:
        return '[demasiado grande]'
    if 'application/json' in content_type:
        return sanitize_payload(request.get_json(silent=True))
    return '[omitido]'


def get_response_body(response):
    content_type = response.headers.get('Content-Type', '').lower()

    if 'text/html' in content_type:
        return '[HTML omitido]'
    if response.is_streamed:
        return '[stream omitido]'
    return response.get_data(as_text=True)


def should_store_request():
    return not request.path.startswith('/static/')


def store_request_info(response):
    if not should_store_request():
        return

    user_agent = request.user_agent
    duration_ms = None
    if hasattr(g, 'request_started_at'):
        duration_ms = round((time.perf_counter() - g.request_started_at) * 1000, 2)

    try:
        insert_request_log(
            method=request.method,
            path=request.full_path.rstrip('?'),
            remote_addr=request.remote_addr,
            x_forwarded_for=request.headers.get('X-Forwarded-For'),
            x_real_ip=request.headers.get('X-Real-IP'),
            cf_connecting_ip=request.headers.get('CF-Connecting-IP'),
            user_agent_raw=user_agent.string,
            user_agent_platform=user_agent.platform,
            user_agent_browser=user_agent.browser,
            user_agent_version=user_agent.version,
            ip_country_code=request.headers.get('CF-IPCountry'),
            ip_country_name=None,
            request_headers=sanitize_headers(request.headers),
            request_body=g.get('request_body_for_log', '[omitido]'),
            response_status=response.status_code,
            response_headers=sanitize_headers(response.headers),
            response_body=get_response_body(response),
            duration_ms=duration_ms,
        )
    except Exception:
        current_app.logger.exception('No se pudo guardar el request log')

def log_request_info():
    g.request_started_at = time.perf_counter()
    g.request_body_for_log = get_request_body()
    current_app.logger.debug("Cabeceras de solicitud: %s", sanitize_headers(request.headers))

    if g.request_body_for_log == '[demasiado grande]':
        current_app.logger.debug("Cuerpo de solicitud: [demasiado grande]")
    elif g.request_body_for_log != '[omitido]':
        current_app.logger.debug("Cuerpo de solicitud (JSON): %s", g.request_body_for_log)
    else:
        current_app.logger.debug("Cuerpo de solicitud: [omitido]")

def log_response_info(response):
    current_app.logger.debug("Cabeceras de respuesta: %s", sanitize_headers(response.headers))
    response_body = get_response_body(response)

    if response_body == '[HTML omitido]':
        current_app.logger.debug("Cuerpo de respuesta: [HTML omitido]")
    elif response_body == '[stream omitido]':
        current_app.logger.debug("Cuerpo de respuesta: [stream omitido]")
    else:
        current_app.logger.debug("Cuerpo de respuesta: %s", response_body)
    
    store_request_info(response)
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
