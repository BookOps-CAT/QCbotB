# -*- coding: utf-8 -*-

import unittest
from context import datastore as db
from context import db_worker as worker
from prep_datastore import enter_test_data
from prep_conflict_queries import queries


class TestConflictQueries(unittest.TestCase):
    """local datastore tests"""

    @classmethod
    def setUpClass(cls):
        db.dal.conn_string = 'sqlite:///:memory:'
        db.dal.connect()
        init_session = db.dal.Session()
        enter_test_data(init_session)
        init_session.close()

    def setUp(self):
        # if not using session manager (context_session)
        # don't forget to commit each action
        self.session = db.dal.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_error1_no_cutter(self):
        res = worker.run_query(self.session, queries[1]).first()
        self.assertEqual(res.title, 'TEST1: fiction without cutter')

    def test_error2_non_fic_without_cutter(self):
        res = worker.run_query(self.session, queries[2]).first()
        self.assertEqual(res.title, 'TEST2: non-fic with digit for cutter')

    def test_error3_je_title_entry_with_cutter(self):
        res = worker.run_query(self.session, queries[3]).first()
        self.assertEqual(res.title, 'J-E title entry book with a cutter in the call number')

    def test_error4_trailing_zero_in_dewey(self):
        res = worker.run_query(self.session, queries[4]).first()
        self.assertEqual(res.title, 'Trailing zero in Dewey number in the call number')


if __name__ == '__main__':
    unittest.main()