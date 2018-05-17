# -*- coding: utf-8 -*-

import unittest

from context import conflict2dict


class TestConflictParser(unittest.TestCase):
    """ functional tests of conflict_parser"""

    def test_default_xml_contains_rules(self):
        res = conflict2dict()
        self.assertIsNot(res, [])

    def test_conflict2dict_ouput_type(self):
        res = conflict2dict('conflicts_test.xml')
        self.assertEqual(type(res), list)

    def test_conflict2dict_output_unit_dict_keys(self):
        res = conflict2dict('conflicts_test.xml')
        keys = [k for u in res for k in u]
        self.assertEqual(keys, ['tier', 'query', 'code', 'description', 'id'])

    def test_conflict2dict_output_values(self):
        res = conflict2dict('conflicts_test.xml')
        c = res[0]
        self.assertEqual(c['id'], 1)
        self.assertEqual(c['code'], 'ErrA001')
        self.assertEqual(c['tier'], 'bib-ord')
        self.assertEqual(c['query'], 'SELECT * FROM bibs WHERE bibs.c_cutter = 0 AND bibs.c_type != "fea" AND (bibs.c_type != "eas" AND bibs.author IS NULL)')


if __name__ == '__main__':
    unittest.main()
