from common.config import Settings
from data_generator.generator import QuickDropGenerator


def test_generated_order_has_valid_relationships():
    generator = QuickDropGenerator(Settings())
    order = generator.generate_order()

    assert order.customer_id in generator.customers
    assert order.agent_id in generator.agents
    assert order.product_id in generator.products
    assert round(order.total_amount, 2) == round(order.quantity * order.unit_price, 2)


def test_generated_coordinates_are_valid():
    generator = QuickDropGenerator(Settings())
    order = generator.generate_order()

    assert -90 <= order.delivery_latitude <= 90
    assert -180 <= order.delivery_longitude <= 180

