from django_filters.rest_framework import FilterSet, BooleanFilter
from django.utils import timezone
from .models import Ticket


class TicketFilter(FilterSet):
    is_breached = BooleanFilter(method="filter_is_breached", label="Is Breached")

    class Meta:
        model = Ticket
        fields = ["status", "priority", "assigned_to"]

    def filter_is_breached(self, queryset, name, value):
        if value:
            return queryset.filter(sla_deadline__lt=timezone.now()).exclude(
                status="Closed"
            )
        return queryset

