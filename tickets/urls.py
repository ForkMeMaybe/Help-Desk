from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TicketViewSet,
    CommentViewSet,
    # UserRegistrationView,
    # UserLoginView,
    HealthCheckView,
)

router = DefaultRouter()
router.register(r"tickets", TicketViewSet)
router.register(r"health", HealthCheckView, basename="health")

urlpatterns = [
    path("", include(router.urls)),
    # path('register/', UserRegistrationView.as_view({'post': 'create'}), name='user-registration'),
    # path('login/', UserLoginView.as_view({'post': 'create'}), name='user-login'),
    path(
        "tickets/<int:ticket_pk>/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="ticket-comments",
    ),
]
