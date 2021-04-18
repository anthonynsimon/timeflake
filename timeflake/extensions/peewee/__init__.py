import uuid

import timeflake
from peewee import Field


class TimeflakeBase62Field(Field):

    field_type = "CHAR"

    def db_value(self, value):
        if value is None:
            return value

        if not isinstance(value, timeflake.Timeflake):
            raise ValueError(f"Timeflake expected, got: {value}")

        return value.base62

    def python_value(self, value):
        if value is None:
            return value

        if isinstance(value, timeflake.Timeflake):
            return value

        return timeflake.parse(from_base62=value)


class TimeflakeUUIDField(Field):
    field_type = "UUID"

    def db_value(self, value):
        if value is None:
            return value

        if isinstance(value, timeflake.Timeflake):
            value = value.uuid

        if not isinstance(value, uuid.UUID):
            raise ValueError(f"UUID expected, got: {value}")

        return value.hex

    def python_value(self, value):
        if value is None:
            return value

        if isinstance(value, uuid.UUID):
            return timeflake.parse(from_hex=value.hex)

        return timeflake.parse(from_hex=uuid.UUID(value).hex)
