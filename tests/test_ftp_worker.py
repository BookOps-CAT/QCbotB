# -*- coding: utf-8 -*-

import unittest
from datetime import datetime, timedelta

from context import aged_out_report, find_todays_file


class Test_FTP_worker(unittest.TestCase):
    """ Test FTP_worker module functionality"""

    def test_find_today_file(self):
        self.assertIsNone(
            find_todays_file(None))
        todays_fh = 'BookOpsQC.{}'.format(
            datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))
        fh_list = []
        for i in range(5):
            fh_list.append(
                'BookOpsQC.{}'.format(
                    datetime.strftime(
                        datetime.now() - timedelta(days=1), '%Y%m%d%H%M%S')))
        fh_list.append(todays_fh)
        self.assertEqual(
            find_todays_file(fh_list), todays_fh)

    def test_aged_out_report(self):
        fh1 = 'BookOpsQC.{}'.format(
            datetime.strftime(datetime.now() - timedelta(days=15), '%Y%m%d%H%M%S'))
        self.assertTrue(
            aged_out_report(fh1))

        fh2 = 'BookOpsQC.{}'.format(
            datetime.strftime(datetime.now() - timedelta(days=13), '%Y%m%d%H%M%S'))
        self.assertFalse(
            aged_out_report(fh2))

        fh3 = 'BookOpsQC.{}'.format(
            datetime.strftime(datetime.now() - timedelta(days=13), '%Y%m%d'))
        self.assertFalse(
            aged_out_report(fh3))


if __name__ == '__main__':
    unittest.main()
