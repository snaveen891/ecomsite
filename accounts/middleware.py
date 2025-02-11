from django.core.cache import cache
from django.shortcuts import redirect
from django.contrib import messages

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "login" in request.path and request.method == "POST":
            ip = request.META.get("REMOTE_ADDR")
            key = f"rate_limit:{ip}"

            request_count = cache.get(key, 0)
            print("inside rate limit middleware")
            if request_count >= 5:
                messages.error(request, "Too many login attempts. Try again later.")

            cache.incr(key) if cache.get(key) else cache.set(key, 1, timeout=60)

        return self.get_response(request)