from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from tickets.models import Ticket, Comment
from .serializers import TicketSerializer, CommentSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly, IsAgent, IsAdmin


class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "priority", "assigned_to"]
    search_fields = ["title", "description", "comments__text"]
    ordering_fields = ["created_at", "updated_at", "priority"]

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

        ticket.version += 1
        ticket.save()

        return super().partial_update(request, *args, **kwargs)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(ticket_id=self.kwargs["ticket_pk"])

    def perform_create(self, serializer):
        ticket = Ticket.objects.get(pk=self.kwargs["ticket_pk"])
        serializer.save(user=self.request.user, ticket=ticket)


# class UserRegistrationView(ViewSet):
#     def create(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({"token": token.key}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserLoginView(ViewSet):
#     def create(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         user = authenticate(username=username, password=password)
#         if user:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({"token": token.key})
#         return Response(
#             {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
#         )


class HealthCheckView(ViewSet):
    def list(self, request):
        return Response({"status": "ok"})

