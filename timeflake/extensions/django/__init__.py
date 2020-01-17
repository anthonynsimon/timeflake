import uuid

import timeflake
from django.db import models


def _parse(value) -> timeflake.Timeflake:
    if value is None:
        return value
    elif isinstance(value, timeflake.Timeflake):
        return value
    elif isinstance(value, bytes):
        return timeflake.parse(from_bytes=value)
    elif isinstance(value, int):
        return timeflake.parse(from_int=value)
    elif isinstance(value, str):
        size = len(value)
        # hex
        if size == 32:
            return timeflake.parse(from_hex=value)
        # base62
        elif size == 22:
            return timeflake.parse(from_base62=value)
    elif isinstance(value, uuid.UUID):
        return timeflake.parse(from_bytes=value.bytes)
    raise ValueError(f"Could not parse Timeflake from {value}")


class TimeflakeBinary(models.Field):
    description = "Timeflake UUID (128-bit)"

    def __init__(self, *args, **kwargs):
        super(TimeflakeBinary, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, args, kwargs

    def db_type(self, connection):
        vendor = connection.vendor
        if vendor == "mysql":
            return "binary(16)"
        elif vendor == "sqlite":
            return "blob"
        elif vendor == "postgresql":
            return "uuid"
        raise NotImplementedError(
            f"Unsupported database vendor: {vendor} for field: TimeflakeBinary"
        )

    def rel_db_type(self, connection):
        return self.db_type(connection)

    def from_db_value(self, value, expression, connection):
        return _parse(value)

    def to_python(self, value):
        return _parse(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        value = super().get_db_prep_value(value, connection, prepared)
        if value is not None:
            if connection.vendor == "postgresql":
                return value.uuid
            return value.bytes
        return value


class TimeflakePrimaryKeyBinary(TimeflakeBinary):
    def __init__(self, *args, **kwargs):
        kwargs["primary_key"] = True
        kwargs["editable"] = False
        kwargs["default"] = timeflake.random
        super(TimeflakePrimaryKeyBinary, self).__init__(*args, **kwargs)
