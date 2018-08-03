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
        res = worker.run_query(self.session, self.queries[1])
        ids = sorted([1, 34])
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
        ids = sorted([10])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error9_time_table_in_russian_literature(self):
        res = worker.run_query(self.session, self.queries[9])
        ids = sorted([12])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error10_crit_or_coll_in_american_genre(self):
        res = worker.run_query(self.session, self.queries[10])
        ids = sorted([13])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error11_crit_or_coll_in_english_genre(self):
        res = worker.run_query(self.session, self.queries[11])
        ids = sorted([14])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error12_crit_or_coll_in_spanish_genre(self):
        res = worker.run_query(self.session, self.queries[12])
        ids = sorted([15])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

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

    def test_error17_missing_philospher_name_in_call_number(self):
        res = worker.run_query(self.session, self.queries[17])
        ids = sorted([21])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error18_likely_fiction(self):
        res = worker.run_query(self.session, self.queries[18])
        ids = sorted([22, 23])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error19_criticism_missing_authors_name_in_call_number(self):
        res = worker.run_query(self.session, self.queries[19])
        ids = sorted([23])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error20_annotated_edition_not_ficiton(self):
        res = worker.run_query(self.session, self.queries[20])
        ids = sorted([24, 24, 24])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

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

    def test_error24_score_without_Mu_prefix(self):
        res = worker.run_query(self.session, self.queries[24])
        ids = sorted([29])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error25_not_guidebook_in_911_919_dewey_range(self):
        res = worker.run_query(self.session, self.queries[25])
        ids = sorted([30, 30])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error26_bible_missing_b52(self):
        res = worker.run_query(self.session, self.queries[26])
        ids = sorted([31])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error27_garfield_comic_strip_not_in_7xx(self):
        res = worker.run_query(self.session, self.queries[27])
        ids = sorted([32])
        hits = sorted([r.bid for r in res])
        self.assertEqual(hits, ids)

    def test_error28_JE_call_num_vs_order_shelves(self):
        res = worker.run_query(self.session, self.queries[28])
        # matching ids is a list of tuples with bib id and order id
        ids = sorted([(33, 7), (33, 34)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error29_general_juvenile_call_number_with_wrong_shelf_location(self):
        res = worker.run_query(self.session, self.queries[29])
        ids = sorted([(17, 38)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error30_adult_young_adult_call_number_with_wrong_shelf_location(self):
        res = worker.run_query(self.session, self.queries[30])
        ids = sorted([(24, 36)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error31_biograpy_call_number_with_wrong_order_shelf_location(self):
        res = worker.run_query(self.session, self.queries[31])
        ids = sorted([(35, 39), (35, 41)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error32_non_fic_call_number_with_wrong_order_shelf_location(self):
        res = worker.run_query(self.session, self.queries[32])
        ids = sorted([(30, 31)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error33_fiction_call_number_with_wrong_order_shelf_location(self):
        res = worker.run_query(self.session, self.queries[33])
        ids = sorted([(24, 36)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error34_bilingual_order_shelf_location_with_language_prefix_in_call_number(self):
        res = worker.run_query(self.session, self.queries[34])
        ids = sorted([(17, 18)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error35_SST_order_location_with_wrong_dewey_range_in_call_number(self):
        res = worker.run_query(self.session, self.queries[35])
        ids = sorted([(2, 2), (31, 32)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_36_HBR_order_location_with_wrong_dewey_range_in_call_number(self):
        res = worker.run_query(self.session, self.queries[36])
        ids = sorted([(30, 31), (30, 40)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_37_AMS_order_location_with_wrong_dewey_range_in_call_number(self):
        res = worker.run_query(self.session, self.queries[37])
        ids = sorted([(35, 41)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_38_LL_order_location_with_wrong_dewey_range_in_call_number(self):
        res = worker.run_query(self.session, self.queries[38])
        ids = sorted([(36, 42)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_39_BOOK_CD_order_with_incorrect_call_number(self):
        res = worker.run_query(self.session, self.queries[39])
        ids = sorted([(37, 43)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_40_SST_core_coll_has_16_as_location(self):
        res = worker.run_query(self.session, self.queries[40])
        ids = sorted([(39, 45)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_41_easy_reader_po_per_line_with_incorrect_shelf_codes(self):
        res = worker.run_query(self.session, self.queries[41])
        ids = sorted([(40, 46)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_42_reference_po_per_line_with_incorrect_shelf_codes(self):
        res = worker.run_query(self.session, self.queries[42])
        ids = sorted([(39, 47)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_43_bio_po_per_line_with_incorrect_shelf_codes(self):
        res = worker.run_query(self.session, self.queries[43])
        ids = sorted([(41, 48)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_44_assigment_po_per_line_with_incorrect_shelf_codes(self):
        res = worker.run_query(self.session, self.queries[44])
        ids = sorted([(42, 49)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_45_romance_po_per_line_with_incorrect_shelf_codes(self):
        res = worker.run_query(self.session, self.queries[45])
        ids = sorted([(43, 50)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_46_mystery_po_per_line_with_incorrect_shelf_codes(self):
        res = worker.run_query(self.session, self.queries[46])
        ids = sorted([(44, 51)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_47_sciencefiction_po_per_line_with_incorrect_shelf_codes(self):
        res = worker.run_query(self.session, self.queries[47])
        ids = sorted([(45, 52)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_48_shortstories_po_per_line_with_incorrect_shelf_codes(self):
        res = worker.run_query(self.session, self.queries[48])
        ids = sorted([(46, 53)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_49_graphicnovel_po_per_line_with_incorrect_shelf_codes(self):
        res = worker.run_query(self.session, self.queries[49])
        ids = sorted([(47, 54)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_50_picture_book_po_per_line_with_incorrect_shelf_codes(self):
        res = worker.run_query(self.session, self.queries[50])
        ids = sorted([(48, 55)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_51_missing_or_unused_call_number_type(self):
        res = worker.run_query(self.session, self.queries[51])
        ids = sorted([(49, 56)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_52_UND_as_lang_prefix(self):
        res = worker.run_query(self.session, self.queries[52])
        ids = sorted([(50, 57)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertEqual(hits, ids)

    def test_error_53_graphicnovel_po_per_line_with_additianal_subjects(self):
        res = worker.run_query(self.session, self.queries[49])
        ids = sorted([(56)])
        hits = sorted([(r.bid, r.oid) for r in res])
        self.assertNotIn(hits, ids)


if __name__ == '__main__':
    unittest.main()
