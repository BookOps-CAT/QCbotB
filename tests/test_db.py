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

    def test_run_query(self):
        # print self.session
        resA = worker.run_query(self.session, "SELECT * FROM conflicts").first()
        resB = self.session.execute('SELECT * FROM conflicts').first()
        self.session.commit()
        self.assertEqual(
            resA.code, resB.code)

    def test_delete_table_data(self):
        res = worker.delete_table_data(
            self.session, db.Bibs)
        self.assertEqual(res, 6)
        res = self.session.execute('SELECT * FROM bibs').fetchall()
        self.session.commit()
        self.assertEqual(len(res), 0)

    def test_insert_or_ignore_ignore_scenario(self):
        worker.insert_or_ignore(
            self.session,
            db.Conflicts, id=1, desc='test 1 desc')
        res = self.session.execute('SELECT * FROM conflicts WHERE id = 1').first()
        self.session.commit()
        self.assertEqual(res.desc, 'Test1')

    def test_insert_or_ignore_insert_scenario(self):
        worker.insert_or_ignore(
            self.session,
            db.Conflicts, id = 4, level='bib-ord', code='ErrB002', desc = 'TEST insert')
        self.session.commit()
        self.session.rollback()

        res = self.session.execute('SELECT * FROM conflicts WHERE id = 4').first()
        self.session.commit()
        self.assertEqual(res.id, 4)


    def test_insert_or_update_insert_scenario(self):
        res = self.session.execute('SELECT * FROM conflicts WHERE id = 5').first()
        # self.session.commit()
        self.assertIsNone(res)
        worker.insert_or_update(
            self.session,
            db.Conflicts,
            id = 5, level='bib-ord', code='ErrB003', desc = 'TEST insert on insert_or_update')
        self.session.commit()
        res = self.session.execute('SELECT * FROM conflicts WHERE id = 5').first()
        self.assertEqual(res.id, 5)

    def test_insert_or_update_update_scenario(self):
        worker.insert_or_update(
            self.session,
            db.Conflicts, id = 1, level='bib-ord')
        self.session.commit()
        res = self.session.execute('SELECT * FROM conflicts WHERE id = 5').first()
        self.assertEqual(res.level, 'bib-ord')


if __name__ == '__main__':
    unittest.main()
