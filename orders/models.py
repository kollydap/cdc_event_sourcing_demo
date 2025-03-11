import uuid
from django.db import models
from django.utils.timezone import now


class OrderEvent(models.Model):
    EVENT_TYPES = [
        ("CREATED", "Created"),
        ("PAID", "Paid"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.UUIDField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    payload = models.JSONField()  # Stores event-specific data
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.event_type} - {self.order_id}"

    class Meta:
        ordering = ["timestamp"] 