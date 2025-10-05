from rest_framework import serializers
from .models import Ticket, Comment
from core.models import CustomUser


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Comment
        fields = ["id", "user", "text", "created_at"]


class TicketSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")
    assigned_to = serializers.SlugRelatedField(
        slug_field="username", queryset=CustomUser.objects.all(), required=False
    )
    comments = CommentSerializer(many=True, read_only=True)

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
        ]
        read_only_fields = ["created_at", "updated_at", "sla_deadline", "comments"]


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'password']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
#
#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(**validated_data)
#         return user
