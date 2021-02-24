from flask import request


def get_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return str(request.environ['REMOTE_ADDR'])
    return str(request.environ['HTTP_X_FORWARDED_FOR'])
