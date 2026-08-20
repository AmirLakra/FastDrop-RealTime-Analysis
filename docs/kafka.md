# Kafka

The MVP Kafka topic is `orders`.

Modules:

- `kafka/producer.py`
- `kafka/consumer.py`

Expected flow:

```text
Python generator -> Kafka orders topic -> Kafka consumer -> PostgreSQL
```

