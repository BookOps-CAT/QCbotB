# # -*- coding: utf-8 -*-

from context import datastore as db
import datetime


def enter_test_data(session):
    b1 = db.Bibs(
        c_format='pr',
        c_dewey=None,
        b_type='a',
        c_lang='eng',
        b_date=datetime.datetime(2017, 12, 7, 0, 0),
        c_audn='a',
        id=1,
        c_type='fic',
        author=None,
        title='TEST1: fiction without cutter; ',
        subject_person=None,
        c_cutter=False,
        subjects=u'African American families -- Mississippi -- Fiction.',
        b_format='print',
        c_division=None,
        b_lang='eng',
        crit_work=False,
        b_call=u'FIC')

    b2 = db.Bibs(
        c_format='pr',
        c_dewey=u'635.965',
        b_type=u'a',
        c_lang='eng',
        b_date=datetime.datetime(2017, 12, 7, 0, 0),
        c_audn='a',
        id=2,
        c_type='dew',
        author='LEE',
        title='TEST2: non-fic without cutter; ',
        subject_person=None,
        c_cutter=False,
        subjects=u'Indoor gardening.~Indoor gardens.',
        b_format='print',
        c_division='ss',
        b_lang='eng',
        crit_work=False,
        b_call=u'635.965')

    b3 = db.Bibs(
        c_format='pr',
        c_dewey=u'746.434',
        b_type=u'a',
        c_lang='eng',
        b_date=datetime.datetime(2017, 12, 7, 0, 0),
        c_audn='a',
        id=3,
        c_type='dew',
        author='DELANEY',
        title=u'Design your own crochet projects : magic formulas for creating custom scarves, cowls, hats, socks, mittens, and gloves / Sara Delaney.',
        subject_person=None,
        c_cutter=True,
        subjects=u'Crocheting -- Patterns.',
        b_format='print',
        c_division='ar',
        b_lang='eng',
        crit_work=False,
        b_call=u'746.434 D')

    b4 = db.Bibs(
        c_format='pr',
        c_dewey=u'895.11',
        b_type=u'a',
        c_lang=u'chi',
        b_date=datetime.datetime(2017, 12, 7, 0, 0),
        c_audn='a',
        id=4,
        c_type='dew',
        author='KIM',
        title=u'Ai qing wu li xue / Jin Yinyu zhu ; Liu Yun yi = Sarang \u016di mullihak / Kim In-yuk.',
        subject_person=None,
        c_cutter=True,
        subjects=u'Poetry. lcgft',
        b_format='print',
        c_division='ll',
        b_lang=u'chi',
        crit_work=False,
        b_call=u'CHI 895.11 K')

    b5 = db.Bibs(
        c_format='pr',
        c_dewey=u'320.951',
        b_type=u'a',
        c_lang=u'chi',
        b_date=datetime.datetime(2017, 12, 7, 0, 0),
        c_audn='a',
        id=5,
        c_type='dew',
        author='LI',
        title=u'Zong li da wei zheng duo zhan / Li Ke bian zhu.',
        subject_person='XI',
        c_cutter=True,
        subjects=u'880-05 Xi, Jinping.~880-06 Li, Keqiang.~880-07 Wang, Qishan, 1948-~China -- Politics and government -- 21st century.~Political corruption -- China -- 21st century.~2000-2099 fast',
        b_format='print',
        c_division='ss',
        b_lang=u'chi',
        crit_work=False,
        b_call=u'CHI 320.951 L')

    b6 = db.Bibs(
        c_format='pr',
        c_dewey=u'895.11',
        b_type=u'a',
        c_lang=u'chi',
        b_date=datetime.datetime(2017, 12, 7, 0, 0),
        c_audn='a',
        id=6,
        c_type='dew',
        author='KIM',
        title=u'Ai qing wu li xue / Jin Yinyu zhu ; Liu Yun yi = Sarang \u016di mullihak / Kim In-yuk.',
        subject_person=None,
        c_cutter=True,
        subjects=u'Poetry. lcgft',
        b_format='print',
        c_division='ll',
        b_lang=u'chi',
        crit_work=False,
        b_call=u'CHI 895.11 K')

    session.bulk_save_objects([b1, b2, b3, b4, b5, b6])
    session.commit()

    c1 = db.Orders(
        b_id=1,
        o_branch=u'14,21,22,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,42,43,44,45,46,47,48,49,50,51,52,53,55,56,57,60,61,62,65,66,67,69,70,71,72,74,76,77,78,79,80,81,82,83,85,87',
        copies=59,
        o_date=datetime.datetime(2017, 7, 20, 0, 0),
        o_audn=None,
        o_shelf=None,
        ven_note=None,
        id=1)

    c2 = db.Orders(
        b_id=2,
        o_branch=u'16,43,55,78,79,87',
        copies=6,
        o_date=datetime.datetime(2017, 7, 24, 0, 0),
        o_audn=None,
        o_shelf=None,
        ven_note=None,
        id=2)

    c3 = db.Orders(
        b_id=3,
        o_branch=u'24,42,51',
        copies=3,
        o_date=datetime.datetime(2017, 8, 3, 0, 0),
        o_audn='a',
        o_shelf=u'nf',
        ven_note=u'n',
        id=3)

    c4 = db.Orders(
        b_id=4,
        o_branch=u'14',
        copies=1,
        o_date=datetime.datetime(2017, 8, 11, 0, 0),
        o_audn='a',
        o_shelf=u'wl',
        ven_note=None,
        id=4)

    c5 = db.Orders(
        b_id=5,
        o_branch=u'51,55,67',
        copies=3,
        o_date=datetime.datetime(2017, 8, 11, 0, 0),
        o_audn='a',
        o_shelf=u'wl',
        ven_note=None,
        id=5)

    c6 = db.Orders(
        b_id=6,
        o_branch=u'44,51,55,67,71,74,82',
        copies=7,
        o_date=datetime.datetime(2017, 8, 14, 0, 0),
        o_audn='a',
        o_shelf=u'wl',
        ven_note=None,
        id=6)
    session.bulk_save_objects([c1, c2, c3, c4, c5, c6])
    session.commit()

    
