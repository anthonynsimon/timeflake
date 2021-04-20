import uuid

import timeflake
from django import forms
from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeflakeBinary(models.UUIDField):
    description = "Timeflake UUID (128-bit)"

    def to_python(self, value):
        value = super().to_python(value)
        if value is not None:
            if isinstance(value, uuid.UUID):
                return timeflake.Timeflake(from_bytes=value.bytes)
            else:
                raise exceptions.ValidationError(
                    self.error_messages['invalid'],
                    code='invalid',
                    params={'value': value},
                )
        return value


class TimeflakePrimaryKeyBinary(TimeflakeBinary):
    def __init__(self, *args, **kwargs):
        kwargs["primary_key"] = True
        kwargs["editable"] = False
        kwargs["default"] = timeflake.random
        super(TimeflakePrimaryKeyBinary, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(TimeflakePrimaryKeyBinary, self).deconstruct()
        del kwargs["primary_key"]
        del kwargs["editable"]
        del kwargs["default"]
        return name, path, args, kwargs
