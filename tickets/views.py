from rest_framework import status
from django.utils import timezone
from .models import Ticket, Comment, TicketHistory
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, BooleanFilter
from .serializers import TicketSerializer, CommentSerializer, TicketListSerializer
from .permissions import IsOwnerOrReadOnly, IsAgent, IsAdmin
from .filters import TicketFilter


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TicketFilter
    search_fields = ["title", "description", "comments__text"]
    ordering_fields = ["created_at", "updated_at", "priority"]

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        return TicketSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ["agent", "admin"]:
            return Ticket.objects.all()
        return Ticket.objects.filter(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        ticket = self.get_object()
        version = request.data.get("version")

        if version is not None and int(version) != ticket.version:
            return Response(
                {
                    "error": {
                        "code": "CONFLICT",
                        "message": "Ticket has been modified by another user.",
                    }
                },
                status=status.HTTP_409_CONFLICT,
            )

        old_status = ticket.status
        old_assigned_to = ticket.assigned_to
        old_priority = ticket.priority

        serializer = self.get_serializer(ticket, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_ticket = serializer.save()

        new_status = updated_ticket.status
        new_assigned_to = updated_ticket.assigned_to
        new_priority = updated_ticket.priority

        if old_status != new_status:
            TicketHistory.objects.create(
                ticket=updated_ticket,
                user=request.user,
                field_changed="status",
                old_value=old_status,
                new_value=new_status,
            )

        if old_assigned_to != new_assigned_to:
            TicketHistory.objects.create(
                ticket=updated_ticket,
                user=request.user,
                field_changed="assigned_to",
                old_value=old_assigned_to.username if old_assigned_to else "Unassigned",
                new_value=new_assigned_to.username if new_assigned_to else "Unassigned",
            )

        if old_priority != new_priority:
            TicketHistory.objects.create(
                ticket=updated_ticket,
                user=request.user,
                field_changed="priority",
                old_value=old_priority,
                new_value=new_priority,
            )

        updated_ticket.version += 1
        updated_ticket.save()

        # We need to re-serialize the object to include the updated version number
        final_serializer = self.get_serializer(updated_ticket)
        return Response(final_serializer.data)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(ticket_id=self.kwargs["ticket_pk"])

    def perform_create(self, serializer):
        ticket = Ticket.objects.get(pk=self.kwargs["ticket_pk"])
        serializer.save(user=self.request.user, ticket=ticket)
