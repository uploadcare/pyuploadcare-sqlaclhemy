# coding: utf-8
from unittest import TestCase

from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy.exc import StatementError
from sqlalchemy.sql import select

from pyuploadcare.api_resources import File

from pyuploadcare_sqlalchemy import FileType
from pyuploadcare_sqlalchemy.types import EMPTY_VALUES


class FileTypeTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:', echo=True)
        cls.metadata = MetaData()

        cls.table = Table(
            'example', cls.metadata,
            Column('file', FileType()),
        )
        cls.metadata.create_all(cls.engine)
        cls.connection = cls.engine.connect()

    def setUp(self):
        self.insert = self.table.insert()

    def tearDown(self):
        self.connection.execute(self.table.delete())

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

    def test_valid_uuid(self):
        uuid = 'ebff57dd-6f79-427b-9b43-e7109f055666'
        result = self.connection.execute(self.insert, file=uuid)
        self.assertEqual(result.lastrowid, 1)

        result = self.connection.execute(select([self.table])).fetchall()
        self.assertEqual(len(result), 1)

        field = result[0][0]

        self.assertIsInstance(field, File)
