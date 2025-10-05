from rest_framework import serializers
from tickets.models import Ticket, Comment, TicketHistory
from core.models import CustomUser


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Comment
        fields = ["id", "user", "text", "created_at"]


class TicketHistorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = TicketHistory
        fields = ["id", "user", "field_changed", "old_value", "new_value", "timestamp"]


class TicketSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")
    assigned_to = serializers.SlugRelatedField(
        slug_field="username", queryset=CustomUser.objects.all(), required=False
    )
    comments = CommentSerializer(many=True, read_only=True)
    history = TicketHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "description",
            "created_by",
            "assigned_to",
            "status",
            "priority",
            "created_at",
            "updated_at",
            "sla_deadline",
            "version",
            "comments",
            "history",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
            "sla_deadline",
            "comments",
            "history",
        ]
