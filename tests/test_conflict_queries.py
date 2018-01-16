# -*- coding: utf-8 -*-

import unittest
from context import datastore as db
from context import db_worker as worker
from context import conflict2dict
from prep_datastore import enter_test_data


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

        conflicts = conflict2dict('../QCbotB/files/conflicts.xml')
        self.queries = dict()
        for c in conflicts:
            self.queries[c['id']] = c['query']

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_error1_no_cutter(self):
        res = worker.run_query(self.session, self.queries[1]).first()
        self.assertEqual(res.title, 'TEST1: fiction without cutter')

    def test_error2_non_fic_without_cutter(self):
        res = worker.run_query(self.session, self.queries[2]).first()
        self.assertEqual(res.title, 'TEST2: non-fic with digit for cutter')

    def test_error3_je_title_entry_with_cutter(self):
        res = worker.run_query(self.session, self.queries[3]).first()
        self.assertEqual(res.title, 'J-E title entry book with a cutter in the call number')

    def test_error4_trailing_zero_in_dewey(self):
        res = worker.run_query(self.session, self.queries[4]).first()
        self.assertEqual(res.title, 'Trailing zero in Dewey number in the call number')

    def test_error5_time_table_in_american_literature(self):
        res = worker.run_query(self.session, self.queries[5])
        ids = sorted([5, 6])
        hits = sorted([r.id for r in res])
        self.assertEqual(hits, ids)

    def test_error6_time_table_in_english_literature(self):
        res = worker.run_query(self.session, self.queries[6])
        hits = [8]
        ids = sorted([8])
        hits = sorted([r.id for r in res])
        self.assertEqual(hits, ids)

    def test_error7_time_table_in_spanish_literature(self):
        res = worker.run_query(self.session, self.queries[7])
        ids = sorted([9])
        hits = sorted([r.id for r in res])
        self.assertEqual(hits, ids)

    def test_error8_time_table_in_chinese_literature(self):
        res = worker.run_query(self.session, self.queries[8])
        ids = sorted([4, 10]) # false positive for 4, but that ok
        hits = sorted([r.id for r in res])
        self.assertEqual(hits, ids)

    def test_error9_time_table_in_russian_literature(self):
        res = worker.run_query(self.session, self.queries[9])
        ids = sorted([12])
        hits = sorted([r.id for r in res])
        self.assertEqual(hits, ids)

    def test_error10_crit_or_coll_in_american_genre(self):
        res = worker.run_query(self.session, self.queries[10])
        ids = sorted([13])
        hits = sorted([r.id for r in res])
        self.assertEqual(hits, ids)

    def test_error11_crit_or_coll_in_english_genre(self):
        res = worker.run_query(self.session, self.queries[11])
        ids = sorted([14])
        hits = sorted([r.id for r in res])
        self.assertEqual(hits, ids)

    def test_error12_crit_or_coll_in_spanish_genre(self):
        res = worker.run_query(self.session, self.queries[12])
        ids = sorted([15])
        hits = sorted([r.id for r in res])
        self.assertEqual(hits, ids)

    def test_error13_missing_lang_prefix(self):
        res = worker.run_query(self.session, self.queries[13])
        ids = sorted([17])
        hits = sorted([r.id for r in res])
        self.assertEqual(hits, ids)

    def test_error14_missing_program_lang_in_call_number(self):
        res = worker.run_query(self.session, self.queries[14])
        ids = sorted([18])
        hits = sorted([r.id for r in res])
        self.assertEqual(hits, ids)

    def test_error15_missing_device_name_in_call_number(self):
        res = worker.run_query(self.session, self.queries[15])
        ids = sorted([19])
        hits = sorted([r.id for r in res])
        self.assertEqual(hits, ids)

    def test_error16_missing_OS_name_in_call_number(self):
        res = worker.run_query(self.session, self.queries[16])
        ids = sorted([20])
        hits = sorted([r.id for r in res])
        self.assertEqual(hits, ids)

    def test_error17_missing_philospher_name_in_call_number(self):
        res = worker.run_query(self.session, self.queries[17])
        ids = sorted([21])
        hits = sorted([r.id for r in res])
        self.assertEqual(hits, ids)

    def test_error18_likely_fiction(self):
        res = worker.run_query(self.session, self.queries[18])
        ids = sorted([22])
        hits = sorted([r.id for r in res])
        self.assertEqual(hits, ids)


if __name__ == '__main__':
    unittest.main()
