from orders.models import OrderEvent

import redis
import json


def reconstruct_state(order_id):
    """
    Reconstructs the state of an aggregate (order) from the event log.
    """
    events = OrderEvent.objects.filter(order_id=order_id).order_by("timestamp")
    state = {}

    for event in events:
        if event.event_type == "CREATED":
            state = event.payload
        elif event.event_type == "UPDATED":
            state.update(event.payload)
        elif event.event_type == "CANCELLED":
            state["status"] = "Cancelled"

    return state


# Initialize Redis connection
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

STREAM_NAME = "order_events"  # Name of the Redis Stream


def append_event(order_id, event_type, payload):
    """
    Appends an event to the event log and pushes it to Redis Stream.
    """
    event = OrderEvent.objects.create(
        order_id=order_id, event_type=event_type, payload=payload
    )

    # Publish the event to Redis Stream for CDC
    redis_client.xadd(
        STREAM_NAME,
        {
            "order_id": str(order_id),
            "event_type": event_type,
            "payload": json.dumps(payload),
        },
    )

    return event
