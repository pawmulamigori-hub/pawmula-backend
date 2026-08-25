from django.http import JsonResponse

def root_view(request):
    return JsonResponse({
        "status": "ok",
        "service": "Pawmula API",
        "version": "1.0.0",
        "endpoints": {
            "admin": "/admin/",
            "api": "/api/",
            "auth": "/api/auth/",
            "events": "/api/events/",
            "destinations": "/api/destinations/"
        }
    })
