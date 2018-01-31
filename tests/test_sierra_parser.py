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
        self.assertIsNone(
            sierra_parser.verify_bib_id())

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
        self.assertIsNone(
            sierra_parser.verify_ord_id())

    def test_parsing_dates(self):
        date1 = datetime.now().strftime('%m-%d-%Y')
        date2 = datetime.now().strftime('%m-%d-%y')
        self.assertEqual(
            sierra_parser.parse_dates(date1),
            datetime.strptime(date1, '%m-%d-%Y'))
        self.assertEqual(
            sierra_parser.parse_dates(date2),
            datetime.strptime(date2, '%m-%d-%y'))
        self.assertIsNone(
            sierra_parser.parse_dates('some string'))
        self.assertIsNone(
            sierra_parser.parse_dates('  -  -  '))
        self.assertIsNone(
            sierra_parser.parse_dates())

    def test_verify_b_type(self):
        self.assertEqual(
            sierra_parser.verify_b_type(
                'a'), 'a')
        self.assertIsNone(
            sierra_parser.verify_b_type(
                ''))
        self.assertIsNone(
            sierra_parser.verify_b_type(
                ' '))
        self.assertIsNone(
            sierra_parser.verify_b_type(
                1))

    def test_parse_title(self):
        self.assertEqual(
            sierra_parser.parse_title(
                '880-02 [Perush ha-Ramban : ʻal ha-Torah] = Rambanh'),
            '[Perush ha-Ramban : ʻal ha-Torah] = Rambanh')
        self.assertEqual(
            sierra_parser.parse_title(
                'TEST TITLE'), 'TEST TITLE')
        self.assertIsNone(
            sierra_parser.parse_title(
                ''))
        self.assertIsNone(
            sierra_parser.parse_title())

    def test_parse_name(self):
        self.assertEqual(
            sierra_parser.parse_name(
                u'880-01 Shukshĭn, Vasiliĭ, 1929-1974'),
            u'SHUKSHIN')
        self.assertEqual(
            sierra_parser.parse_name(
                u'Ṿalder, Ḥayim.'),
            u'VALDER')
        self.assertEqual(
            sierra_parser.parse_name(
                u'Uderzo.'),
            u'UDERZO')
        self.assertIsNone(
            sierra_parser.parse_name(
                u''))

    def test_parse_subjects(self):
        self.assertEqual(
            sierra_parser.parse_subjects(
                'Automobile racing drivers -- Drama.~NASCAR (Association) -- Drama.~Fourth dimension. fast (OCoLC)fst00933422'),
            'Automobile racing drivers -- Drama.~NASCAR (Association) -- Drama.')
        self.assertEqual(
            sierra_parser.parse_subjects(
                ''), '')

    def test_parse_subject_person(self):
        self.assertIsNone(
            sierra_parser.parse_subject_person(
                'Jackson, Percy (Fictitious character) -- '
                'Juvenile fiction'))
        self.assertEqual(
            sierra_parser.parse_subject_person(
                'Lincoln, Abraham, 1809-1865 -- Military leadership.~Other subject'),
            'Lincoln, Abraham, 1809-1865 -- Military leadership.')
        self.assertEqual(
            sierra_parser.parse_subject_person(
                'Doe, Joe. Title of his work.'),
            'Doe, Joe. Title of his work.')
        self.assertEqual(
            sierra_parser.parse_subject_person(
                'Randolph, Martha Jefferson, 1772-1836.~Women -- United States -- History -- 18th century'),
            'Randolph, Martha Jefferson, 1772-1836.')
        self.assertEqual(
            sierra_parser.parse_subject_person(
                '880-05 Wang, Yangming.~Philosophers -- China -- Biography.'),
            'Wang, Yangming.')
        # -- biography will most likely pick up false positives
        self.assertEqual(
            sierra_parser.parse_subject_person(
                'Wang, Yangming.~Philosophers -- China -- Biography.'),
            'Wang, Yangming.')
        self.assertEqual(
            sierra_parser.parse_subject_person(
                'Wang.~Philosophers -- China -- Biography.'),
            'Wang.')
        self.assertIsNone(
            sierra_parser.parse_subject_person(
                'Some Topic.~Philosophers -- China.'))
        self.assertIsNone(
            sierra_parser.parse_subject_person(
                'History, Millitary.'))
        self.assertIsNone(
            sierra_parser.parse_subject_person(
                'Jews -- Poland -- Warsaw.~Righteous Gentiles in the Holocaust -- Poland -- Warsaw.~Holocaust, Jewish (1939-1945) -- Poland -- Warsaw.~World War, 1939-1945 -- Jews -- Rescue -- Poland -- Warsaw.'))

    def test_parse_branches(self):
        self.assertEqual(
            sierra_parser.parse_branches(
                '03yfc,80yfc,71yfc,65yfc,56yfc'),
            '03,56,65,71,80')
        self.assertEqual(
            sierra_parser.parse_branches(
                '03yfc(10),80   ,none '),
            '03,80')
        self.assertIsNone(
            sierra_parser.parse_branches(
                ''))
        self.assertEqual(
            sierra_parser.parse_branches(
                'elres'), '')

    def test_parse_shelves(self):
        # shelves in a string that is used to compare output
        # must be in alphabetical order
        self.assertEqual(
            sierra_parser.parse_shelves(
                '14anb(2),21anf,23abi,56   '),
            'abi,anb,anf')
        self.assertIsNone(
            sierra_parser.parse_shelves(
                '14   '))
        self.assertIsNone(
            sierra_parser.parse_shelves(
                'none '))
        self.assertEqual(
            sierra_parser.parse_shelves(
                '02jje(10),none ,21jje',), 'jje')

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
                'BOOK & CD RUS J 486.76 C'), 'j')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'BOOK & CD RUS 486.76 C'), 'a')
        self.assertEqual(
            sierra_parser.parse_call_audn(
                'FIC J'), 'a')

    def test_world_language_prefix(self):
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'DVD'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'DVD 909 B'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'DVD B ADAMS A'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'DVD J B ADAMS A'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'DVD CHI'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'DVD CHI J B ADAMS B'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'DVD J'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                ''), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'DVD ARA J'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'DVD ARA J 909 A'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'AUDIO RUS FIC ADAMS'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'AUDIO RUS J FIC ADAMS'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'AUDIO J FIC ADAMS'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'AUDIO FIC ADAMS'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'AUDIO CHI 909 A'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'AUDIO FIC ADA'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'AUDIO RUS B ADAMS A'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'KIT RUS 909 A'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'KIT 909 A'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'KIT J 909 A'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'KIT RUS J 909 A'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'KIT 872.8 H'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'BOOK & CD RUS 811 B'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'BOOK & CD RUS J-E'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'BOOK & CD RUS J FIC A'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'BOOK & CD FIC ADA'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'BOOK & CD RUS B ADAMS A'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'BOOK & CD B ADAMS A'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'BOOK & CD 901 A'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'BOOK & CD J-E ADAMS'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'BOOK & DVD RUS 811 B'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'BOOK & DVD RUS J-E'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'BOOK & DVD RUS J FIC A'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'BOOK & DVD FIC ADA'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'BOOK & DVD RUS B ADAMS A'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'BOOK & DVD B ADAMS A'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'BOOK & DVD 901 A'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'BOOK & DVD RUS B ADA B'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'SPA J-E ADAMS'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'SPA FIC ADAMS'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'CHI J FIC ADAMS'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'POL B ADA J'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'RUS 811 B'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'VIDEO CHI'), True)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'FIC ADAMS'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'B ADAMS J'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'J-E ADAMS'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'J-E'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'FIC F'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'FIC BARTHELME'), False)
        self.assertIs(
            sierra_parser.world_lang_prefix(
                'LIB 711.3 B'), False)

        self.assertIs(
            sierra_parser.world_lang_prefix(
                'FIC JOHNSTONE'), False)

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
        self.assertEqual(
            sierra_parser.parse_call_type(
                'BOOK & CD 468.3421 B'), 'dew')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'BOOK & CD 811 WHITMAN K'), 'des')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'BOOK & CD ARA 428.34927 L'), 'dew')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'BOOK & CD J B ADAMS A'), 'bio')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'AUDIO 225.5208 B582 W'), 'des')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'AUDIO 782.1 WAGNER S'), 'des')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'AUDIO SPA FIC COELHO'), 'fic')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'AUDIO SPA B CRUZ M'), 'bio')
        self.assertEqual(
            sierra_parser.parse_call_type(
                'AUDIO SPA J FIC SAINT-EXUPERY'), 'fic')
        self.assertIsNone(
            sierra_parser.parse_call_type(
                'RUS TROTSKY Z'))

    def test_parse_call_cutter(self):
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'SPA J-E ADAMS'), True)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'J-E'), False)
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
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'AUDIO 226.607'), False)
        self.assertIs(
            sierra_parser.parse_call_cutter(
                'AUDIO 226.607 C'), True)

        self.assertIs(
            sierra_parser.parse_call_cutter(
                'FIC 1'), False)
        # very unlikely sanborn cutters will be pick up
        self.assertIs(
            sierra_parser.parse_call_cutter(
                '973 A211'), True)

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
        self.assertEqual(
            sierra_parser.identify_dewey_range(
                '294.3927 H'), 'hb')

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
        record = sierra_parser.report_data('report_test.txt', 180).next()
        bib_keys = [x for x in record[0]]
        ord_keys = [x for x in record[1]]
        self.assertEqual(bib_keys, [
            'c_format', 'c_dewey', 'b_date', 'c_wl', 'c_audn', 'id',
            'c_type', 'author', 'title', 'subject_person', 'c_cutter',
            'subjects', 'c_division', 'b_type', 'crit_work', 'b_call'])
        self.assertEqual(ord_keys, [
            'bid', 'o_branch', 'copies', 'o_date', 'o_audn',
            'o_shelf', 'ven_note', 'id'])


if __name__ == '__main__':
    unittest.main()
