from django.core.cache import cache
from rest_framework.response import Response
from django.core.cache import cache
from django.http import HttpResponse


class IdempotencyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and "Idempotency-Key" in request.headers:
            idempotency_key = request.headers["Idempotency-Key"]
            cached = cache.get(idempotency_key)
            if cached:
                resp = HttpResponse(
                    content=cached["content"],
                    status=cached["status"],
                )
                for name, value in cached["headers"].items():
                    resp[name] = value
                return resp

            response = self.get_response(request)

            if 200 <= response.status_code < 300:
                if hasattr(response, "render") and callable(response.render):
                    response = response.render()

                cache.set(
                    idempotency_key,
                    {
                        "content": bytes(response.content),
                        "status": response.status_code,
                        "headers": dict(response.items()),
                    },
                    timeout=3600,
                )

            return response

        return self.get_response(request)


# class IdempotencyMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         if request.method == "POST" and "Idempotency-Key" in request.headers:
#             idempotency_key = request.headers["Idempotency-Key"]
#             cached_response = cache.get(idempotency_key)
#
#             if cached_response:
#                 print("served from cache")
#                 return Response(cached_response, status=200)
#
#             response = self.get_response(request)
#
#             if 200 <= response.status_code < 300:
#                 cache.set(idempotency_key, response.data, timeout=3600)
#
#             return response
#
#         return self.get_response(request)
