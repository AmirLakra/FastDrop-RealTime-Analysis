from pathlib import Path

import psycopg

from common.config import Settings
from common.schemas import OrderEvent


def postgres_dsn(settings: Settings) -> str:
    return (
        f"host={settings.postgres_host} "
        f"port={settings.postgres_port} "
        f"dbname={settings.postgres_db} "
        f"user={settings.postgres_user} "
        f"password={settings.postgres_password}"
    )


def initialize_database(settings: Settings) -> None:
    schema_sql = Path("database/schema.sql").read_text(encoding="utf-8")
    views_sql = Path("database/views.sql").read_text(encoding="utf-8")
    with psycopg.connect(postgres_dsn(settings), autocommit=True) as connection:
        with connection.cursor() as cursor:
            cursor.execute(schema_sql)
            cursor.execute(views_sql)


def insert_order(settings: Settings, order: OrderEvent) -> None:
    query = """
        INSERT INTO orders (
            order_id, customer_id, agent_id, product_id, city, quantity, unit_price, total_amount,
            order_timestamp, pickup_timestamp, delivery_timestamp, promised_delivery_timestamp,
            delivery_latitude, delivery_longitude, distance_km, order_status, payment_method, event_timestamp
        ) VALUES (
            %(order_id)s, %(customer_id)s, %(agent_id)s, %(product_id)s, %(city)s, %(quantity)s,
            %(unit_price)s, %(total_amount)s, %(order_timestamp)s, %(pickup_timestamp)s,
            %(delivery_timestamp)s, %(promised_delivery_timestamp)s, %(delivery_latitude)s,
            %(delivery_longitude)s, %(distance_km)s, %(order_status)s, %(payment_method)s, %(event_timestamp)s
        )
        ON CONFLICT (order_id) DO NOTHING
    """
    with psycopg.connect(postgres_dsn(settings), autocommit=True) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, order.model_dump(mode="python"))

