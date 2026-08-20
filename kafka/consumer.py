from __future__ import annotations

import json
import logging

from common.config import get_settings
from common.schemas import OrderEvent
from database.postgres import insert_order

try:
    from confluent_kafka import Consumer
except ImportError:  # pragma: no cover
    Consumer = None


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("quickdrop.kafka.consumer")


class KafkaOrderConsumer:
    def __init__(self) -> None:
        self.settings = get_settings()
        if Consumer is None:
            raise RuntimeError("confluent-kafka is not installed.")
        self.consumer = Consumer(
            {
                "bootstrap.servers": self.settings.kafka_bootstrap_servers,
                "group.id": self.settings.kafka_group_id,
                "auto.offset.reset": "earliest",
                "enable.auto.commit": False,
            }
        )
        self.consumer.subscribe([self.settings.kafka_topic])

    def run(self) -> None:
        while True:
            message = self.consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                logger.error("Kafka error: %s", message.error())
                continue
            try:
                payload = json.loads(message.value().decode())
                order = OrderEvent.model_validate(payload)
                insert_order(self.settings, order)
                self.consumer.commit(message=message, asynchronous=False)
                logger.info("Stored %s", order.order_id)
            except Exception as exc:
                logger.warning("Invalid or failed order event: %s", exc)


if __name__ == "__main__":
    KafkaOrderConsumer().run()

