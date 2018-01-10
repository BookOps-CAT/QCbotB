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
        id='12054709',
        c_type='fic',
        author='WARD',
        title=u'Sing, unburied, sing : a novel / Jesmyn Ward.',
        subject_person=None,
        c_cutter=True,
        subjects=u'African American families -- Mississippi -- Fiction.',
        b_format='print',
        c_division=None,
        b_lang='eng',
        crit_work=False,
        b_call=u'FIC WARD')

    b2 = db.Bibs(
        c_format='pr',
        c_dewey=u'635.965',
        b_type=u'a',
        c_lang='eng',
        b_date=datetime.datetime(2017, 12, 7, 0, 0),
        c_audn='a',
        id='12056955',
        c_type='dew',
        author='LEE',
        title=u'Living with plants : a guide to indoor gardening / Sophie Lee ; photography by Leonie Freeman.',
        subject_person=None,
        c_cutter=True,
        subjects=u'Indoor gardening.~Indoor gardens.',
        b_format='print',
        c_division='ss',
        b_lang='eng',
        crit_work=False,
        b_call=u'635.965 L')

    b3 = db.Bibs(
        c_format='pr',
        c_dewey=u'746.434',
        b_type=u'a',
        c_lang='eng',
        b_date=datetime.datetime(2017, 12, 7, 0, 0),
        c_audn='a',
        id=u'12102423',
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
        id=u'12076335',
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
        id=u'12076367',
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
        id=u'12076335',
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
