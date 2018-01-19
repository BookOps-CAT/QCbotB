# -*- coding: utf-8 -*-

import unittest
from datetime import datetime

from context import sierra_parser


class TestParser(unittest.TestCase):
    """Test parsing of Sierra lists exported to file"""

    def test_verifying_bib_id(self):
        self.assertEqual(
            sierra_parser.verify_bib_id('b119955209'), 11995520)
        self.assertEqual(
            sierra_parser.verify_bib_id('b12081951x'), 12081951)
        self.assertIsNone(
            sierra_parser.verify_bib_id(''))
        self.assertIsNone(
            sierra_parser.verify_bib_id(None))
        self.assertIsNone(
            sierra_parser.verify_bib_id(11995520))

    def test_verifying_ord_id(self):
        self.assertEqual(
            sierra_parser.verify_ord_id('o19259785'), 1925978)
        self.assertEqual(
            sierra_parser.verify_ord_id('o1926029X'), 1926029)
        self.assertIsNone(
            sierra_parser.verify_ord_id(''))
        self.assertIsNone(
            sierra_parser.verify_ord_id(None))
        self.assertIsNone(
            sierra_parser.verify_ord_id(1199552))

    def test_parsing_dates(self):
        date1 = datetime.now().strftime('%m-%d-%Y')
        date2 = datetime.now().strftime('%m-%d-%y')
        self.assertEqual(
            sierra_parser.parse_dates(date1, 1),
            datetime.strptime(date1, '%m-%d-%Y'))
        self.assertEqual(
            sierra_parser.parse_dates(date2, 1),
            datetime.strptime(date2, '%m-%d-%y'))
        self.assertIsNone(
            sierra_parser.parse_dates('some string', 1))
        self.assertIsNone(
            sierra_parser.parse_dates('  -  -  ', 1))

    def test_parse_bib_format(self):
        # print
        self.assertEqual(
            sierra_parser.find_bib_format(
                'a',
                '170619s2017    mau      b    000 0 eng ccam i ',
                [], 1), 'print')
        # eBook
        self.assertEqual(
            sierra_parser.find_bib_format(
                'a',
                '101207s2010    ilua    ob    001 0 eng d      ',
                [], 1), 'eres')
        # Score
        self.assertEqual(
            sierra_parser.find_bib_format(
                'c',
                '170619s2017    mau      b    000 0 eng ccam i ',
                [], 1), 'score')
        # Libretto
        self.assertEqual(
            sierra_parser.find_bib_format(
                'a',
                '170619s2017    mau      b    000 0 eng ccam i ',
                ['librettos'], 1), 'lib')
        # DVD
        self.assertEqual(
            sierra_parser.find_bib_format(
                'g',
                '171207s2015    cau120            vlrusodngmIi ',
                [], 1), 'dvd')
        # eVideo
        self.assertEqual(
            sierra_parser.find_bib_format(
                'g',
                '070507p20062004nyu092 e      s   vleng d      ',
                [], 1), 'eres')
        # Audio
        self.assertEqual(
            sierra_parser.find_bib_format(
                'i',
                '171207s2015    cau120            vlrusodngmIi ',
                [], 1), 'audio')
        # eAudio
        self.assertEqual(
            sierra_parser.find_bib_format(
                'i',
                '060404s2005    nyunnn  s      f    eng d      ',
                [], 1), 'eres')
        # Music CD
        self.assertEqual(
            sierra_parser.find_bib_format(
                'j',
                '080717s2008    dcublnn  fhi      n eng d      ',
                [], 1), 'cd')
        # microforms
        self.assertEqual(
            sierra_parser.find_bib_format(
                'a',
                '781211d17301734enk x   a     0   a0eng d      ',
                [], 1), 'micro')
        # kit
        self.assertEqual(
            sierra_parser.find_bib_format(
                'o',
                '070814r20071999nyua     b    001 0 eng        ',
                [], 1), 'kit')
        self.assertEqual(
            sierra_parser.find_bib_format(
                'p',
                '070814r20071999nyua     b    001 0 eng        ',
                [], 1), 'kit')
        # photo
        self.assertEqual(
            sierra_parser.find_bib_format(
                'k',
                '020102s1968    nyu               ineng d      ',
                [], 1), 'photo')
        # CD-ROM
        self.assertEqual(
            sierra_parser.find_bib_format(
                'm',
                '130313s2010    nyu     q  d        eng d      ',
                [], 1), 'eres')
        # mifi & other 3-D objects
        self.assertEqual(
            sierra_parser.find_bib_format(
                'r',
                '160930s9999    xx             00 zzzxx d      ',
                [], 1), '3dobj')

    def test_parse_title(self):
        self.assertEqual(
            sierra_parser.parse_title(
                '880-02 [Perush ha-Ramban : ʻal ha-Torah] = Rambanh'),
            '[Perush ha-Ramban : ʻal ha-Torah] = Rambanh')

    def test_parse_name(self):
        self.assertEqual(
            sierra_parser.parse_name(
                u'880-01 Shukshĭn, Vasiliĭ, 1929-1974', 1),
            u'SHUKSHIN')
        self.assertEqual(
            sierra_parser.parse_name(
                u'Ṿalder, Ḥayim.', 1),
            u'VALDER')
        self.assertEqual(
            sierra_parser.parse_name(
                u'Uderzo.', 1),
            u'UDERZO')
        self.assertIsNone(
            sierra_parser.parse_name(
                u'', 1))

    def test_find_main_language(self):
        # bilingual book should be under world language
        # find out how bilingual poetry published in us can be in English
        # find_main_language returns results in alphabetical order
        self.assertEqual(
            sierra_parser.find_main_language(
                '170305s2017    nyu           000 p eng dcamIi ',
                'spa~eng', 1), 'eng~spa')

    def test_parse_subject_person(self):
        self.assertIsNone(
            sierra_parser.parse_subject_person(
                'Jackson, Percy (Fictitious character) -- '
                'Juvenile fiction', 1))
        self.assertEqual(
            sierra_parser.parse_subject_person(
                u'880-11 Heller, Yom Tov Lipmann ben Nathan '
                'ha-Levi ben Wallerstein, 1579-1654.'
                '~Ferdinand II, Holy Roman Emperor, 1578-1637.', 1),
            u'HELLER')

    def test_identify_critical_work(self):
        self.assertIs(
            sierra_parser.idenfity_critical_work(
                'Heidegger, Martin, 1889-1976',
                'Heidegger, Martin, 1889-1976. Sein und Zeit', 1), True)
        self.assertIs(
            sierra_parser.idenfity_critical_work(
                'Heidegger, Martin, 1889-1976. Criticism, '
                'interpretation, etc.',
                '', 1), True)
        self.assertIs(
            sierra_parser.idenfity_critical_work(
                'Heidegger, Martin, 1889-1976',
                '', 1), False)

    def test_parse_branches(self):
        self.assertEqual(
            sierra_parser.parse_branches(
                '03yfc,80yfc,71yfc,65yfc,56yfc', 1),
            '03,56,65,71,80')
        self.assertIsNone(
            sierra_parser.parse_branches(
                '', 1))
        self.assertEqual(
            sierra_parser.parse_branches(
                'elres', 1),
            '')

    def test_parse_shelves(self):
        # shelves in a string that is used to compare output
        # must be in alphabetical order
        self.assertEqual(
            sierra_parser.parse_shelves(
                '14anb(2),21anf,23abi,56   ', 1),
            'abi,anb,anf')

    def test_parse_call_format(self):
        self.assertEqual(
            sierra_parser.parse_call_format(
                'AUDIO B ADAMS C'), 'au')
        self.assertEqual(
            sierra_parser.parse_call_format(
                '818 A'), 'pr')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'B BOOK C'), 'pr')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'DVD RUS J'), 'dv')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'BOOK & DVD 818 D'), 'ki')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'BOOK & CD'), 'ki')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'KIT'), 'ki')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'eBOOK'), 'er')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'eAUDIO'), 'er')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'eJOURNAL'), 'er')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'eMUSIC'), 'er')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'eVIDEO'), 'er')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'DVD-ROM 909 A'), 'er')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'CD-ROM 909 A'), 'er')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'LIB 782.1 AUBER'), 'li')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'Mu 780.4 K'), 'mu')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'NM 010.5 H'), 'nm')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'CD BLUES BO DIDDLEY'), 'cd')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'VIDEO'), 'vi')
        self.assertEqual(
            sierra_parser.parse_call_format(
                'MIFI DEVICE'), 'mi')
        self.assertEqual(
            sierra_parser.parse_call_format(
                ''), 'pr')

    def test_parse_call_audn(self):
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'J-E'), 'e')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'J-E SCIESZKA'), 'e')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'CHI J-E XI'), 'e')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'CHI J-E'), 'e')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'KIT J-E SCIESZKA'), 'e')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'J 811 B'), 'j')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'J B ADAMS W'), 'j')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'DVD J'), 'j')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'DVD RUS J'), 'j')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'DVD SPA J B ADAMS'), 'j')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'KIT J 909 A'), 'j')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'AUDIO J FIC ADAMS'), 'j')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'BOOK & CD J 494 A'), 'j')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'POL J FIC SCIESZKA'), 'j')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'DVD JPN'), 'a')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'B BAJ-EON C'), 'a')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'eBOOK'), 'a')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                '811 J'), 'a')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'B ADAMS J'), 'a')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'DVD'), 'a')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'DVD JPN'), 'a')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'BOOK & CD RUS 486.76 C'), 'a')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'FIC J'), 'a')

    def test_parse_call_lang(self):
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'SPA J-E ADAMS'), 'spa')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'SPA FIC ADAMS'), 'spa')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'CHI J FIC ADAMS'), 'chi')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'POL B ADA J'), 'pol')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'RUS 811 B'), 'rus')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'BOOK & CD RUS 811 B'), 'rus')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'BOOK & DVD RUS B ADA B'), 'rus')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'KIT RUS 811 B'), 'rus')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'AUDIO RUS FIC ADAMS'), 'rus')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'VIDEO CHI'), 'chi')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'DVD CHI'), 'chi')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'DVD CHI J B ADAMS B'), 'chi')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'FIC ADAMS'), 'eng')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'B ADAMS J'), 'eng')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'J-E ADAMS'), 'eng')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'J-E'), 'eng')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'DVD'), 'eng')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'DVD 909 B'), 'eng')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'DVD B ADAMS A'), 'eng')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'DVD J B ADAMS A'), 'eng')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'FIC F'), 'eng')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'FIC BARTHELME'), 'eng')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'LIB 711.3 B'), 'eng')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'KIT 872.8 H'), 'eng')
        self.assertEqual(
            sierra_parser.parse_call_lang(
                'FIC JOHNSTONE'), 'eng')

    def test_parse_call_type(self):
        self.assertEqual(
            sierra_parser.parse_call_type(
                'SPA J-E ADAMS'), 'eas')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'J-E ADAMS'), 'eas')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'J-E'), 'eas')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'KIT J-E ADAMS'), 'eas')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'FIC ADAMS'), 'fic')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'FIC B'), 'fic')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'POL J FIC ADAMS'), 'fic')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'FIC ADAMS'), 'fic')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'B ADAMS A'), 'bio')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'B ADA-BAD A'), 'bio')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'RUS B G\'OGOL A'), 'bio')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'DVD B ADAMS A'), 'bio')
        self.assertEqual(
            sierra_parser.parse_call_type(
                '811 POE B'), 'des')
        self.assertEqual(
            sierra_parser.parse_call_type(
                '641.5 ROB R'), 'des')  # this is incorrect call number
        self.assertEqual(
            sierra_parser.parse_call_type(
                '762.6535 BOWIE B'), 'des')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'DVD 762.6535 BOWIE B'), 'des')
        self.assertEqual(
            sierra_parser.parse_call_type(
                '005.133 SWIFT S'), 'des')
        self.assertEqual(
            sierra_parser.parse_call_type(
                '818 P'), 'dew')
        self.assertEqual(
            sierra_parser.parse_call_type(
                '909.765 P'), 'dew')
        self.assertEqual(
            sierra_parser.parse_call_type(
                '822.33 S52 Q'), 'des')
        # older call number pattern
        self.assertEqual(
            sierra_parser.parse_call_type(
                '929.2 H241 B2'), 'des')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'DVD'), 'fea')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'DVD J'), 'fea')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'DVD SPA'), 'fea')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'DVD SPA J'), 'fea')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'MIFI DEVICE'), 'mif')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'eBOOK'), 'ere')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'CD WORLD JEWISH SHWEKEY'), 'cdm')

    def test_parse_call_cutter(self):
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'SPA J-E ADAMS'), True)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'J B ADAMS J'), True)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'DVD RUS 909 B'), True)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'BOOK & CD 987 J'), True)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'AUDIO FIC ADAMS'), True)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'CD FOLK COHEN'), True)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'WEB SITE 909 B'), True)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                '909 B'), True)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'RUS 811 POE B'), True)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'SPA J-E'), False)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'J FIC'), False)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'FIC'), False)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'J B'), False)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'DVD RUS'), False)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'DVD J'), False)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                '909'), False)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'MIFI DEVICE'), False)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'eBOOK'), False)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                '658.058 D598'), True)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'DVD J 919 D'), True)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'DVD J 919.34'), False)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                '823.33 S52'), False)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                '823.33 S52 A B'), True)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                '226.607 B582'), False)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                '226.607 B582 C'), True)

    def test_parse_dewey(self):
        self.assertEqual(
            sierra_parser.parse_call_dewey(
                '909 B'), '909')
        self.assertEqual(
            sierra_parser.parse_call_dewey(
                'J 909.993 B'), '909.993')
        self.assertEqual(
            sierra_parser.parse_call_dewey(
                'DVD 909.76 B'), '909.76')
        self.assertEqual(
            sierra_parser.parse_call_dewey(
                '004.54 PYTHON B'), '004.54')
        self.assertEqual(
            sierra_parser.parse_call_dewey(
                '220.52 B582 C'), '220.52')
        self.assertIsNone(
            sierra_parser.parse_call_dewey(
                'FIC ADAMS'))
        self.assertIsNone(
            sierra_parser.parse_call_dewey(
                'J B ADAMS C'))
        self.assertIsNone(
            sierra_parser.parse_call_dewey(
                'DVD RUS'))
        self.assertIsNone(
            sierra_parser.parse_call_dewey(
                'J-E ADAMS'))

    def test_identify_dewey_range(self):
        self.assertEqual(
            sierra_parser.identify_dewey_range(
                '060 E'), 'll')
        self.assertEqual(
            sierra_parser.identify_dewey_range(
                '001.9 E'), 'll')
        self.assertEqual(
            sierra_parser.identify_dewey_range(
                '428.4 S'), 'll')
        self.assertEqual(
            sierra_parser.identify_dewey_range(
                '028.9 S'), 'll')
        self.assertEqual(
            sierra_parser.identify_dewey_range(
                '811 S'), 'll')
        self.assertEqual(
            sierra_parser.identify_dewey_range(
                '028.9 S'), 'll')
        self.assertEqual(
            sierra_parser.identify_dewey_range(
                '070.92 S'), 'll')
        self.assertEqual(
            sierra_parser.identify_dewey_range(
                '004.165 RASPBERRY PI R'), 'ss')
        self.assertEqual(
            sierra_parser.identify_dewey_range(
                '190 B'), 'ss')
        self.assertEqual(
            sierra_parser.identify_dewey_range(
                '341.02 D'), 'ss')
        self.assertEqual(
            sierra_parser.identify_dewey_range(
                '509 D'), 'ss')
        self.assertEqual(
            sierra_parser.identify_dewey_range(
                '641.72 D'), 'ss')
        self.assertEqual(
            sierra_parser.identify_dewey_range(
                '208.23 D'), 'hb')
        self.assertEqual(
            sierra_parser.identify_dewey_range(
                '900 D'), 'hb')
        self.assertEqual(
            sierra_parser.identify_dewey_range(
                '391 D'), 'ar')
        self.assertEqual(
            sierra_parser.identify_dewey_range(
                '711 D'), 'ar')

    def test_parse_ord_audn(self):
        self.assertEqual(
            sierra_parser.parse_ord_audn(
                'awl'), 'a')
        self.assertEqual(
            sierra_parser.parse_ord_audn(
                'ynf'), 'y')
        self.assertEqual(
            sierra_parser.parse_ord_audn(
                'jje'), 'j')
        self.assertIsNone(
            sierra_parser.parse_ord_audn(
                ''))
        self.assertEqual(
            sierra_parser.parse_ord_audn(
                'nac'), 'a')
        self.assertEqual(
            sierra_parser.parse_ord_audn(
                'tab'), 'a')
        self.assertEqual(
            sierra_parser.parse_ord_audn(
                'tcp'), 'j')
        self.assertEqual(
            sierra_parser.parse_ord_audn(
                'mfi'), 'a')
        self.assertIsNone(
            sierra_parser.parse_ord_audn(
                ''))

    def test_parsing_of_row_of_sierra_report(self):
        """fuctional tests of sierra report parser"""
        record = sierra_parser.report_data('report_test.txt').next()
        bib_keys = [x for x in record[0]]
        ord_keys = [x for x in record[1]]
        self.assertEqual(bib_keys, [
            'c_format', 'c_dewey', 'b_type', 'c_lang', 'b_date',
            'c_audn', 'id', 'c_type', 'author', 'title',
            'subject_person', 'c_cutter', 'subjects', 'b_format',
            'c_division', 'b_lang', 'crit_work', 'b_call'])
        self.assertEqual(ord_keys, [
            'bid', 'o_branch', 'copies', 'o_date', 'o_audn',
            'o_shelf', 'ven_note', 'id'])


if __name__ == '__main__':
    unittest.main()
