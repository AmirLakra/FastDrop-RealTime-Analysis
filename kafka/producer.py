from __future__ import annotations

import argparse
import json
import logging
import time

from common.config import get_settings
from data_generator.generator import QuickDropGenerator

try:
    from confluent_kafka import Producer
except ImportError:  # pragma: no cover
    Producer = None


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("quickdrop.kafka.producer")


class KafkaOrderProducer:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.generator = QuickDropGenerator(self.settings)
        if Producer is None:
            raise RuntimeError("confluent-kafka is not installed.")
        self.producer = Producer({"bootstrap.servers": self.settings.kafka_bootstrap_servers})

    def _delivery_report(self, error, message) -> None:
        if error is not None:
            logger.error("Failed to publish order event: %s", error)
            return
        logger.info("Published %s", message.key().decode())

    def run(self, rate: int) -> None:
        delay = 1 / max(rate, 1)
        while True:
            order = self.generator.generate_order()
            self.producer.produce(
                topic=self.settings.kafka_topic,
                key=order.order_id.encode(),
                value=json.dumps(order.model_dump(mode="json")).encode(),
                callback=self._delivery_report,
            )
            self.producer.poll(0)
            time.sleep(delay)


def main() -> None:
    settings = get_settings()
    parser = argparse.ArgumentParser(description="Publish QuickDrop orders to Kafka.")
    parser.add_argument("--rate", type=int, default=settings.orders_per_second)
    args = parser.parse_args()
    KafkaOrderProducer().run(args.rate)


if __name__ == "__main__":
    main()

