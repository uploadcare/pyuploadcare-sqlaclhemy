# coding: utf-8
from sqlalchemy.types import TypeDecorator, UnicodeText

from pyuploadcare.api_resources import File, FileGroup
from pyuploadcare.exceptions import InvalidRequestError

__ALL__ = ('FileType',)

EMPTY_VALUES = ('', None)


class FileType(TypeDecorator):
    impl = UnicodeText

    def process_bind_param(self, value, dialect):
        if not value or value in EMPTY_VALUES:
            return value

        if isinstance(value, File):
            return value.cdn_url

        if isinstance(value, (basestring, unicode)):
            return File(value).cdn_url

        raise ValueError('Invalid type of value: {}'.format(type(value)))

    def process_result_value(self, value, dialect):
        if not value or value in EMPTY_VALUES:
            return value

        return File(value)

    def copy(self):
        return FileType(self.impl.length)
