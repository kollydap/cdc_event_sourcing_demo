import redis
import json
import time
from django.core.management.base import BaseCommand

# Initialize Redis connection
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

STREAM_NAME = "notification_events"
GROUP_NAME = "notification_group"
CONSUMER_NAME = "notification_consumer"


class Command(BaseCommand):
    help = "Listens for order events and sends notifications"

    def handle(self, *args, **kwargs):
        """Main function that runs the Notification Service"""
        self.stdout.write(self.style.SUCCESS("📢 Notification Service Listening..."))

        # Create a consumer group if it doesn't exist
        try:
            redis_client.xgroup_create(STREAM_NAME, GROUP_NAME, mkstream=True)
        except redis.exceptions.ResponseError:
            pass  # Ignore if the group already exists

        while True:
            try:
                # Read new events from Redis stream
                events = redis_client.xreadgroup(
                    GROUP_NAME, CONSUMER_NAME, {STREAM_NAME: ">"}, count=1, block=5000
                )

                for stream, messages in events:
                    for message_id, message_data in messages:
                        order_id = message_data["order_id"]
                        event_type = message_data["event_type"]

                        if event_type in ["PAID", "SHIPPED"]:
                            self.send_notification(order_id, event_type)

                        # Acknowledge the event
                        redis_client.xack(STREAM_NAME, GROUP_NAME, message_id)

            except Exception as e:
                self.stderr.write(f"Error in Notification Service: {e}")
                time.sleep(2)  # Prevents excessive retries

    def send_notification(self, order_id, event_type):
        """Simulates sending a notification (email/SMS)"""
        self.stdout.write(
            self.style.SUCCESS(
                f"📢 Notification: Order {order_id} - {event_type} update sent!"
            )
        )
