# coding: utf-8
import mock

from sqlalchemy import Table, Column
from sqlalchemy.exc import StatementError
from sqlalchemy.sql import select

from pyuploadcare.api_resources import File, FileGroup

from pyuploadcare_sqlalchemy import FileType, ImageType, FileGroupType

from tests.base import TableBasedTestCase

EMPTY_VALUES = ('', None)


class FileTypeTestCase(TableBasedTestCase):
    cols = dict(file=FileType())

    valid_uuid = 'ebff57dd-6f79-427b-9b43-e7109f055666'

    def test_invalid_uuid(self):
        self.assertRaisesRegexp(StatementError,
                                "Couldn't find UUID",
                                self.connection.execute,
                                self.insert, file='invalid')

    def test_empty_values(self):
        for i, v in enumerate(EMPTY_VALUES, 1):
            result = self.connection.execute(self.insert, file=v)
            self.assertEqual(i, result.lastrowid)

            result = self.connection.execute(select([self.table])).fetchall()
            field = result[i-1][0]
            self.assertEqual(field, v)

    @mock.patch('pyuploadcare_sqlalchemy.types.File.is_stored')
    @mock.patch('pyuploadcare_sqlalchemy.types.File.store')
    def test_valid_uuid(self, store, is_stored):
        is_stored.return_value = False

        result = self.connection.execute(self.insert, file=self.valid_uuid)
        self.assertEqual(result.lastrowid, 1)

        result = self.connection.execute(select([self.table])).fetchall()
        self.assertEqual(len(result), 1)

        field = result[0][0]

        self.assertIsInstance(field, File)
        self.assertTrue(store.called)
        self.assertTrue(store.is_stored)


class FileGroupTypeTestCase(FileTypeTestCase):
    cols = dict(file=FileGroupType())

    valid_uuid = 'ebff57dd-6f79-427b-9b43-e7109f055666~12'

    def test_invalid_uuid(self):
        self.assertRaisesRegexp(StatementError,
                                "Couldn't find group id",
                                self.connection.execute,
                                self.insert, file='invalid')

    @mock.patch('pyuploadcare_sqlalchemy.types.FileGroup.is_stored')
    @mock.patch('pyuploadcare_sqlalchemy.types.FileGroup.store')
    def test_valid_uuid(self, store, is_stored):
        is_stored.return_value = False

        result = self.connection.execute(self.insert, file=self.valid_uuid)
        self.assertEqual(result.lastrowid, 1)

        result = self.connection.execute(select([self.table])).fetchall()
        self.assertEqual(len(result), 1)

        field = result[0][0]

        self.assertIsInstance(field, FileGroup)
        self.assertTrue(store.called)
        self.assertTrue(store.is_stored)


class ImageTypeTestCase(FileTypeTestCase):
    effects = '-/resize/200x300/-/autorotate/yes/'
    cols = dict(file=ImageType(effects=effects))

    def test_invalid_effects(self):
        self.assertRaisesRegexp(ValueError,
                                "Invalid value for effects param",
                                ImageType,
                                effects='invalid')

        self.assertRaisesRegexp(ValueError,
                                "Value of effects must be a string type",
                                ImageType,
                                effects=99)

    @mock.patch('pyuploadcare_sqlalchemy.types.File.is_image')
    def test_is_not_image(self, is_image):
        is_image.return_value = False
        self.assertRaisesRegexp(StatementError,
                                "This is not image",
                                self.connection.execute,
                                self.insert,
                                file=self.valid_uuid)

    @mock.patch('pyuploadcare_sqlalchemy.types.File.is_image')
    def test_valid_uuid(self, is_image):
        is_image.return_value = True
        super(ImageTypeTestCase, self).test_valid_uuid()

    @mock.patch('pyuploadcare_sqlalchemy.types.File.is_image')
    @mock.patch('pyuploadcare_sqlalchemy.types.File.is_stored')
    @mock.patch('pyuploadcare_sqlalchemy.types.File.store')
    def test_check_effects(self, store, is_stored, is_image):
        is_stored.return_value = True
        is_image.return_value = True

        result = self.connection.execute(self.insert, file=self.valid_uuid)
        self.assertEqual(result.lastrowid, 1)

        result = self.connection.execute(select([self.table])).fetchall()
        field = result[0][0]

        self.assertTrue(field.cdn_url.endswith(self.effects))
