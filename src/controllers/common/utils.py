from flask import make_response


def simple_error_response(msg, status, key="message"):
    return make_response({key: msg}, status)


def permitted_parameters(request_data, permitted_params):
    filtered_data = {}

    for param, value in request_data.items():
        if param in permitted_params:
            filtered_data[param] = value

    return filtered_data


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
