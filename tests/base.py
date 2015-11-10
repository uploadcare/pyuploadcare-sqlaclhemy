# coding: utf-8
from unittest import TestCase

from sqlalchemy import create_engine, Table, Column, MetaData

engine = create_engine('sqlite:///:memory:', echo=False)
connection = engine.connect()
metadata = MetaData()


def create_table(name, **kwargs):
    cols = [Column(k, v, nullable=True) for k, v in kwargs.items()]
    table = Table(name, metadata, *cols)
    metadata.create_all(engine)
    return table


class TableBasedTestCase(TestCase):
    cols = None

    @classmethod
    def setUpClass(cls):
        assert isinstance(cls.cols, dict)
        cls.table = create_table(cls.__name__.lower(), **cls.cols)
        cls.connection = connection

    def setUp(self):
        self.insert = self.table.insert()

    def tearDown(self):
        connection.execute(self.table.delete())
