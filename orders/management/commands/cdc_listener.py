import redis
import json
import time
from django.core.management.base import BaseCommand

# Initialize Redis connection
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

STREAM_NAME = "order_events"
NOTIFICATION_STREAM = "notification_events"
ANALYTICS_STREAM = "analytics_events"
GROUP_NAME = "cdc_group"
CONSUMER_NAME = "consumer_1"

class Command(BaseCommand):
    help = "Listens for CDC events from Redis Streams and forwards them"

    def handle(self, *args, **kwargs):
        """Main function that runs the CDC listener"""
        self.stdout.write(self.style.SUCCESS("🚀 Starting CDC Listener..."))

        # Create a consumer group if it doesn't exist
        try:
            redis_client.xgroup_create(STREAM_NAME, GROUP_NAME, mkstream=True)
        except redis.exceptions.ResponseError:
            pass  # Ignore if group already exists

        while True:
            try:
                # Read new events from the Redis stream
                events = redis_client.xreadgroup(
                    GROUP_NAME, CONSUMER_NAME, {STREAM_NAME: ">"}, count=1, block=5000
                )

                for stream, messages in events:
                    for message_id, message_data in messages:
                        order_id = message_data["order_id"]
                        event_type = message_data["event_type"]
                        payload = json.loads(message_data["payload"])

                        # Log received events
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"CDC Event -> Order: {order_id}, Event: {event_type}, Data: {payload}"
                            )
                        )

                        # ✅ Forward to Notification Service (only relevant events)
                        if event_type in ["PAID", "SHIPPED"]:
                            redis_client.xadd(
                                NOTIFICATION_STREAM,
                                {"order_id": order_id, "event_type": event_type},
                            )
                            self.stdout.write(self.style.WARNING("📢 Sent to Notification Service"))

                        # ✅ Forward to Analytics Service (logs all events)
                        redis_client.xadd(
                            ANALYTICS_STREAM,
                            {"order_id": order_id, "event_type": event_type, "payload": json.dumps(payload)},
                        )
                        self.stdout.write(self.style.WARNING("📊 Sent to Analytics Service"))

                        # Acknowledge the event
                        redis_client.xack(STREAM_NAME, GROUP_NAME, message_id)

            except Exception as e:
                self.stderr.write(f"Error processing CDC event: {e}")
                time.sleep(2)  # Prevents excessive retries on failure
