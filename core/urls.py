from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"health", views.HealthCheckView, basename="health")
router.register(r"_meta", views.MetaView, basename="meta")

urlpatterns = [
    path("", include(router.urls)),
    path("send_otp/", views.send_otp, name="send_otp"),
    path("verify_otp/", views.verify_otp, name="verify_otp"),
]
