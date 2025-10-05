from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, CommentViewSet

router = DefaultRouter()
router.register(r"tickets", TicketViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "tickets/<int:ticket_pk>/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="ticket-comments",
    ),
]
