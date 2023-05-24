import requests
from functools import wraps
from flask import make_response, request


def simple_error_response(msg, status, key="message"):
    return make_response({key: msg}, status)


def fields_errors_response(
    errors,
    msg,
    status,
    msg_key="message",
    errors_key="errors",
):
    return make_response({msg_key: msg, errors_key: errors}, status)


def validation_error_response(
    validation_error,
    msg,
    status=requests.codes.bad_request,
    msg_key="message",
    errors_key="errors",
):
    return make_response({msg_key: msg, errors_key: validation_error.messages}, status)


def permitted_parameters(request_data, permitted_params):
    return dict(filter(lambda pair: pair[0] in permitted_params, request_data.items()))


def missing_required_fields(request_data, required_fields):
    return list(
        map(
            lambda field: field[1],
            filter(
                lambda field: request_data.get(field[0], None) is None, required_fields
            ),
        )
    )


def missing_required_fields_msg(missing_fields):
    return f"Os seguintes campos são obrigatórios: {', '.join(missing_fields)}"


def required_fields(required_fields):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            request_data = request.get_json(force=True, cache=True)

            missing_fields = missing_required_fields(request_data, required_fields)

            if len(missing_fields) > 0:
                return simple_error_response(
                    missing_required_fields_msg(missing_fields),
                    requests.codes.bad_request,
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator
