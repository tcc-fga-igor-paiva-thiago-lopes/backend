def simple_error_response(msg, status, key="error"):
    return {key: msg}, status


def permitted_parameters(request_data, permitted_params):
    filtered_data = {}

    for param, value in request_data.items():
        if param in permitted_params:
            filtered_data[param] = value

    return filtered_data
