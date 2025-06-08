from django.http import HttpResponseServerError, JsonResponse


def ping(request):
    """
    A health check endpoint that returns 'pong'
    """
    return JsonResponse({'response': 'pong'})


def always_500(request):
    """
    A health check endpoint that returns 500
    """
    return HttpResponseServerError()
