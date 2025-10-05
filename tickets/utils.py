from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_response = {
            'error': {
                'code': '',
                'field': '',
                'message': ''
            }
        }
        if hasattr(exc, 'get_codes'):
            custom_response['error']['code'] = exc.get_codes()
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict):
                field = next(iter(exc.detail))
                custom_response['error']['field'] = field
                custom_response['error']['message'] = exc.detail[field][0]
            else:
                custom_response['error']['message'] = exc.detail

        response.data = custom_response

    return response
