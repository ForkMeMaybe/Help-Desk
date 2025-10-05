from django.core.mail import BadHeaderError
from rest_framework import viewsets
from rest_framework.response import Response
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
import json
from smtplib import SMTPException
from templated_mail.mail import BaseEmailMessage
from .utils import generate_otp, validate_otp
from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import CustomUser
from .serializers import AgentSerializer


@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON format."})

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"success": False, "message": "Invalid email format."})

        email_otp = generate_otp()
        redis_key = f"otp:{email}"
        cache.set(redis_key, email_otp)

        try:
            message = BaseEmailMessage(
                template_name="emails/otp_template.html",
                context={"email_otp": email_otp},
            )
            message.send([email])
        except (BadHeaderError, SMTPException) as e:
            return JsonResponse(
                {"success": False, "message": f"Failed to send OTP. Error: {str(e)}"}
            )

        return JsonResponse(
            {
                "success": True,
                "message": "OTP sent successfully. Please check your email.",
            }
        )


@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            user_otp = data.get("otp")
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON format."})

        if not email or not user_otp:
            return JsonResponse(
                {"success": False, "message": "Email and OTP are required."}
            )

        redis_key = f"otp:{email}"
        stored_otp = cache.get(redis_key)

        if stored_otp is None:
            return JsonResponse(
                {"success": False, "message": "OTP expired or not found."}
            )

        if validate_otp(stored_otp, user_otp):
            cache.delete(redis_key)
            cache.set(f"otp_verified:{email}", True, timeout=600)
            return JsonResponse(
                {"success": True, "message": "OTP verified successfully."}
            )
        else:
            cache.delete(redis_key)
            return JsonResponse({"success": False, "message": "Invalid OTP."})

    return JsonResponse({"success": False, "message": "Invalid request method."})


class MetaView(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def list(self, request):
        return Response({"name": "HelpDesk Mini", "version": "1.0.0"})


class HealthCheckView(viewsets.ViewSet):
    def list(self, request):
        return Response({"status": "ok"})


from django.http import JsonResponse
from django.conf import settings
import json
import os

def hackathon_json_view(request):
    file_path = os.path.join(settings.BASE_DIR, 'static', '.well-known', 'hackathon.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    return JsonResponse(data)

class AgentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.filter(role='agent')
    serializer_class = AgentSerializer
    permission_classes = [IsAdminUser]
