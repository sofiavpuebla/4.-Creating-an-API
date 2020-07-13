from flask import request

class APIError(Exception):
    statusCode=500

class Error404(APIError):
    statusCode=404

