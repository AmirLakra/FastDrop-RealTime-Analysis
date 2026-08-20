from __future__ import annotations

import argparse
import json

from common.config import get_settings
from data_generator.generator import QuickDropGenerator


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a finite QuickDrop dataset.")
    parser.add_argument("--count", type=int, default=100)
    args = parser.parse_args()

    generator = QuickDropGenerator(get_settings())
    orders = generator.generate_batch(args.count, backfill=True)
    print(json.dumps([order.model_dump(mode="json") for order in orders], indent=2))


if __name__ == "__main__":
    main()

