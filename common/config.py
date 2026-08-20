from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "quickdrop"
    postgres_user: str = "quickdrop"
    postgres_password: str = "quickdrop"

    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic: str = "orders"
    kafka_group_id: str = "quickdrop-consumer"

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:5173"

    demo_mode: bool = True
    orders_per_second: int = 2
    number_of_customers: int = 500
    number_of_agents: int = 80
    number_of_products: int = 120
    supported_cities: str = Field(
        default="Bengaluru,Delhi,Mumbai,Hyderabad,Pune,Kolkata,Chennai,Bhubaneswar"
    )
    seed_history_count: int = 240
    alert_delivery_minutes_threshold: int = 45
    alert_cancellation_rate_threshold: float = 15.0
    alert_orders_per_minute_threshold: int = 30
    alert_revenue_per_hour_threshold: float = 150000.0

    @property
    def supported_city_list(self) -> list[str]:
        return [city.strip() for city in self.supported_cities.split(",") if city.strip()]

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

