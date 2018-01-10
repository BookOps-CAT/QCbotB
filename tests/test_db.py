# -*- coding: utf-8 -*-

import unittest
from context import datastore as db
from context import db_worker as worker
from prep_datastore import enter_test_data


class TestDatastore(unittest.TestCase):
    """local datastore tests"""

    @classmethod
    def setUpClass(cls):
        db.dal.conn_string = 'sqlite:///:memory:'
        db.dal.connect()
        db.dal.session = db.dal.Session()
        enter_test_data(db.dal.session)
        db.dal.session.close()

    def setUp(self):
        db.dal.session = db.dal.Session()

    def tearDown(self):
        db.dal.session.rollback()
        db.dal.session.close()

    def test_delete_table_data(self):
        self.assertEqual(worker.delete_table_data(db.Bibs), 6)
        self.assertEqual(worker.delete_table_data(db.Orders), 6)





if __name__ == '__main__':
    unittest.main()
