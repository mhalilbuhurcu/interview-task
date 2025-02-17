from django.http import JsonResponse

def handler404(request, exception):
    return JsonResponse({
        'status_code': 404,
        'error': 'The resource was not found'
    }, status=404)

def handler500(request):
    return JsonResponse({
        'status_code': 500,
        'error': 'Internal server error'
    }, status=500)

def handler403(request, exception):
    return JsonResponse({
        'status_code': 403,
        'error': 'Permission denied'
    }, status=403)

def handler400(request, exception):
    return JsonResponse({
        'status_code': 400,
        'error': 'Bad request'
    }, status=400) 