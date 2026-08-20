from __future__ import annotations

import math
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class CitySpec:
    name: str
    latitude: float
    longitude: float
    demand_multiplier: float


CITY_SPECS: dict[str, CitySpec] = {
    "Bengaluru": CitySpec("Bengaluru", 12.9716, 77.5946, 1.35),
    "Delhi": CitySpec("Delhi", 28.6139, 77.2090, 1.25),
    "Mumbai": CitySpec("Mumbai", 19.0760, 72.8777, 1.30),
    "Hyderabad": CitySpec("Hyderabad", 17.3850, 78.4867, 1.12),
    "Pune": CitySpec("Pune", 18.5204, 73.8567, 0.96),
    "Kolkata": CitySpec("Kolkata", 22.5726, 88.3639, 1.05),
    "Chennai": CitySpec("Chennai", 13.0827, 80.2707, 1.00),
    "Bhubaneswar": CitySpec("Bhubaneswar", 20.2961, 85.8245, 0.84),
}


def demand_weight(city_name: str) -> float:
    return CITY_SPECS[city_name].demand_multiplier


def random_coordinate(city_name: str, radius_km: float = 12.0) -> tuple[float, float]:
    city = CITY_SPECS[city_name]
    distance = random.uniform(0.2, radius_km)
    angle = random.uniform(0, 2 * math.pi)
    lat_offset = (distance / 111.0) * math.cos(angle)
    lon_offset = (distance / (111.0 * math.cos(math.radians(city.latitude)))) * math.sin(angle)
    return round(city.latitude + lat_offset, 6), round(city.longitude + lon_offset, 6)

