from django.middleware.csrf import get_token
from django.http import JsonResponse

def token(request, *args, **kwargs):
    token = get_token(request)
    data = {
        'token' : token
    }
    return JsonResponse( data )