from __future__ import annotations

import argparse
import asyncio
import json

from common.config import get_settings
from data_generator.generator import QuickDropGenerator


async def stream_orders(rate: int) -> None:
    generator = QuickDropGenerator(get_settings())
    delay = 1 / max(rate, 1)
    while True:
        order = generator.generate_order()
        print(json.dumps(order.model_dump(mode="json")))
        await asyncio.sleep(delay)


def main() -> None:
    settings = get_settings()
    parser = argparse.ArgumentParser(description="Continuously stream QuickDrop orders to stdout.")
    parser.add_argument("--rate", type=int, default=settings.orders_per_second)
    args = parser.parse_args()
    asyncio.run(stream_orders(args.rate))


if __name__ == "__main__":
    main()

