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
        # db.dal.con_string = 'sqlite:///test_datastore.db'
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
        res = worker.run_query(self.session, self.queries[1])
        ids = sorted([1, 2])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error2_digit_for_cutter(self):
        res = worker.run_query(self.session, self.queries[2])
        ids = sorted([2])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error3_je_title_entry_with_cutter(self):
        res = worker.run_query(self.session, self.queries[3])
        ids = sorted([3])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error4_trailing_zero_in_dewey(self):
        res = worker.run_query(self.session, self.queries[4])
        ids = sorted([4])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error5_time_table_in_american_literature(self):
        res = worker.run_query(self.session, self.queries[5])
        ids = sorted([5, 6])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error6_time_table_in_english_literature(self):
        res = worker.run_query(self.session, self.queries[6])
        hits = [8]
        ids = sorted([8])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error7_time_table_in_spanish_literature(self):
        res = worker.run_query(self.session, self.queries[7])
        ids = sorted([9])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error8_time_table_in_chinese_literature(self):
        res = worker.run_query(self.session, self.queries[8])
        ids = sorted([4, 10]) # false positive for 4, but that ok
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error9_time_table_in_russian_literature(self):
        res = worker.run_query(self.session, self.queries[9])
        ids = sorted([12])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    # def test_error10_crit_or_coll_in_american_genre(self):
    #     res = worker.run_query(self.session, self.queries[10])
    #     ids = sorted([13])
    #     hits = sorted([r.bid for r in res])
    #     self.assertEqual(hits, ids)

    # def test_error11_crit_or_coll_in_english_genre(self):
    #     res = worker.run_query(self.session, self.queries[11])
    #     ids = sorted([14])
    #     hits = sorted([r.bid for r in res])
    #     self.assertEqual(hits, ids)

    # def test_error12_crit_or_coll_in_spanish_genre(self):
    #     res = worker.run_query(self.session, self.queries[12])
    #     ids = sorted([15])
    #     hits = sorted([r.bid for r in res])
    #     self.assertEqual(hits, ids)

    def test_error13_lang_prefix_for_textbooks_for_english_speakers(self):
        res = worker.run_query(self.session, self.queries[13])
        ids = sorted([17, 17])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error14_missing_program_lang_in_call_number(self):
        res = worker.run_query(self.session, self.queries[14])
        ids = sorted([18])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error15_missing_device_name_in_call_number(self):
        res = worker.run_query(self.session, self.queries[15])
        ids = sorted([19])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error16_missing_OS_name_in_call_number(self):
        res = worker.run_query(self.session, self.queries[16])
        ids = sorted([20])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    # def test_error17_missing_philospher_name_in_call_number(self):
    #     res = worker.run_query(self.session, self.queries[17])
    #     ids = sorted([21])
    #     hits = sorted([r.bid for r in res])
    #     self.assertEqual(hits, ids)

    def test_error18_likely_fiction(self):
        res = worker.run_query(self.session, self.queries[18])
        ids = sorted([22, 23])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    # def test_error19_criticism_missing_authors_name_in_call_number(self):
    #     res = worker.run_query(self.session, self.queries[19])
    #     ids = sorted([23])
    #     hits = sorted([r.bid for r in res])
    #     self.assertEqual(hits, ids)

    # def test_error20_annotated_edition_not_ficiton(self):
    #     res = worker.run_query(self.session, self.queries[20])
    #     ids = sorted([24, 24, 24])
    #     hits = sorted([r.bid for r in res])
    #     self.assertEqual(hits, ids)

    def test_error21_shakespares_individual_works(self):
        res = worker.run_query(self.session, self.queries[21])
        ids = sorted([25])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error22_shakespeare_quotiations(self):
        res = worker.run_query(self.session, self.queries[22])
        ids = sorted([27])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error23_shakespeare_criticism(self):
        res = worker.run_query(self.session, self.queries[23])
        ids = sorted([28])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    # def test_error24_score_without_Mu_prefix(self):
    #     res = worker.run_query(self.session, self.queries[24])
    #     ids = sorted([29])
    #     hits = sorted([r.bid for r in res])
    #     self.assertEqual(hits, ids)

    # def test_error25_not_guidebook_in_911_919_dewey_range(self):
    #     res = worker.run_query(self.session, self.queries[25])
    #     ids = sorted([30])
    #     hits = sorted([r.bid for r in res])
    #     self.assertEqual(hits, ids)

    # def test_error26_bible_missing_b52(self):
    #     res = worker.run_query(self.session, self.queries[26])
    #     ids = sorted([31])
    #     hits = sorted([r.bid for r in res])
    #     self.assertEqual(hits, ids)

    # def test_error27_garfield_comic_strip_not_in_7xx(self):
    #     res = worker.run_query(self.session, self.queries[27])
    #     ids = sorted([32])
    #     hits = sorted([r.bid for r in res])
    #     self.assertEqual(hits, ids)

    def test_error28_JE_call_num_vs_order_shelves(self):
        res = worker.run_query(self.session, self.queries[28])
        # matching ids is a list of tuples with bib id and order id
        ids = sorted([(33, 7), (33, 34)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    # def test_error29_02_central_location_without_juvenile_call_number(self):
    #     res = worker.run_query(self.session, self.queries[29])
    #     # matching ids is a list of tuples with bib id and order id
    #     ids = sorted([(24, 36), (24, 37)])
    #     hits = sorted([(r.bid, r.oid) for r in res])
    #     self.assertEqual(hits, ids)

    def test_error30_general_juvenile_call_number_with_wrong_shelf_location(self):
        res = worker.run_query(self.session, self.queries[30])
        ids = sorted([(17, 38)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error31_adult_young_adult_call_number_with_wrong_shelf_location(self):
        res = worker.run_query(self.session, self.queries[31])
        ids = sorted([(24, 36)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    # def test_error32_biograpy_call_number_with_wrong_order_shelf_location(self):
    #     pass

if __name__ == '__main__':
    unittest.main()
