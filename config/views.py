from django.http import HttpResponse
from django.conf import settings
import os

def ping(request):
    ping_path = os.path.join(settings.BASE_DIR, "static", "ping.png")
    with open(ping_path, "rb") as f:
        return HttpResponse(f.read(), content_type="image/png")
