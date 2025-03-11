import redis
import json

# Initialize Redis connection
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

STREAM_NAME = "order_events"
GROUP_NAME = "analytics_group"
CONSUMER_NAME = "analytics_consumer"

# Create consumer group if it doesn't exist
try:
    redis_client.xgroup_create(STREAM_NAME, GROUP_NAME, mkstream=True)
except redis.exceptions.ResponseError:
    pass  # Ignore if the group already exists

print("Analytics Service Listening...")


def store_event(order_id, event_type, payload):
    """Simulates storing analytics data."""
    print(
        f"📊 Analytics: Order {order_id} - {event_type} recorded with data: {payload}"
    )


while True:
    try:
        # Read events
        events = redis_client.xreadgroup(
            GROUP_NAME, CONSUMER_NAME, {STREAM_NAME: ">"}, count=1, block=5000
        )

        for stream, messages in events:
            for message_id, message_data in messages:
                order_id = message_data["order_id"]
                event_type = message_data["event_type"]
                payload = json.loads(message_data["payload"])

                store_event(order_id, event_type, payload)

                # Acknowledge the event
                redis_client.xack(STREAM_NAME, GROUP_NAME, message_id)

    except Exception as e:
        print(f"Error in Analytics Service: {e}")
