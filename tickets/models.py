from django.db import models
from django.conf import settings
from django.utils import timezone


class Ticket(models.Model):
    STATUS_CHOICES = (
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Closed", "Closed"),
        ("Resolved", "Resolved"),
    )
    PRIORITY_CHOICES = (
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_tickets",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Open")
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="Medium"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sla_deadline = models.DateTimeField(null=True, blank=True)
    version = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.pk:
            now = timezone.now()
            if self.priority == "High":
                self.sla_deadline = now + timezone.timedelta(hours=24)
            elif self.priority == "Medium":
                self.sla_deadline = now + timezone.timedelta(hours=48)
            else:
                self.sla_deadline = now + timezone.timedelta(days=72)
        super().save(*args, **kwargs)


class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class TicketHistory(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="history")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    field_changed = models.CharField(max_length=100)
    old_value = models.CharField(max_length=255)
    new_value = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

