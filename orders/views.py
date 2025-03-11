from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
from orders.helpers import append_event, reconstruct_state


class OrderAPIView(APIView):
    """Handles Order Creation and State Reconstruction"""

    def post(self, request, *args, **kwargs):
        """Create a new order event"""
        order_id = uuid.uuid4()
        event = append_event(order_id, "PAID", {"description": "New order created"})

        return Response(
            {"order_id": str(order_id), "event": event.event_type},
            status=status.HTTP_201_CREATED,
        )

    def get(self, request, order_id, *args, **kwargs):
        """Get order state by reconstructing from event history"""
        state = reconstruct_state(order_id)
        return Response({"order_id": order_id, "state": state})
