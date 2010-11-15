import re
import unittest
from os import path
import os
from xml.dom.minidom import parse, parseString
from django.db import transaction

from quran.models import *
from quran.buckwalter import *


def path_to(fn):
    return path.join(path.dirname(__file__), fn)

@transaction.commit_on_success
def import_quran():
    d = parse(path_to('tanzil/quran-data.xml'))
    d2 = parse(path_to('tanzil/quran-uthmani.xml'))
    suras = d.getElementsByTagName('sura')
    for s in suras:
        index = int(s.getAttribute('index'))
        ayas = s.getAttribute('ayas')
        start = int(s.getAttribute('start'))
        name = s.getAttribute('name')
        tname = s.getAttribute('tname')
        ename = s.getAttribute('ename')
        type = s.getAttribute('type')
        order = int(s.getAttribute('order'))
        rukus = int(s.getAttribute('rukus'))
        sura_model = Sura(number=index, name=name, tname=tname, ename=ename, type=type, order=order, rukus=rukus)

        sura = d2.getElementsByTagName('sura')[index - 1]
        assert int(sura.getAttribute('index')) == sura_model.number
        sura_model.save()

        ayas = sura.getElementsByTagName('aya')
        bismillah = ayas[0].getAttribute('bismillah')
        for aya in ayas:
            index = int(aya.getAttribute('index'))
            text = aya.getAttribute('text')
            aya_model = Aya(sura=sura_model, number=index, text=text)
            aya_model.save()
            print "%d:%d" % (sura_model.number, index)


@transaction.commit_on_success
def import_translation_txt(path, translation):
    print "Importing %s translation" % (translation.name)
    f = open(path)
    ayas = Aya.objects.all()
    for aya in ayas:
        line = f.readline()
        if len(line) <= 1:
            raise Exception('Translation file [%s] ended preemtively on aya %d:%d' % (path, aya.sura_id, aya.number))
        line = line.strip()
        t = TranslatedAya(sura=aya.sura, aya=aya, translation=translation, text=line)
        t.save()
        print "[%s] %d:%d" % (translation.name, aya.sura_id, aya.number)


def import_translations():
    translator_data = open(path_to('zekr/translator_data.txt'))
    for line in translator_data.readlines():
        name,translator,source_name,source_url,filename = line.strip().split(';')

        translation = QuranTranslation(name=name,translator=translator, source_name=source_name, source_url=source_url)
        translation.save()
        import_translation_txt(path_to('zekr/%s' % filename), translation)


def extract_lem(morphology):
    p = re.compile('LEM:(?P<lem>[^ "]+)')
    m = p.search(morphology)
    r = None
    word = None
    if(m):
        r = buckwalter_to_unicode(m.group('lem'))
    return r


def extract_root(morphology):
    p = re.compile('ROOT:(?P<root>[^ "]+)')
    m = p.search(morphology)
    r = None
    root = None
    if m:
        r = buckwalter_to_unicode(m.group('root'))
    if r:
        try:
            root = Root.objects.get(letters=r)
        except Root.DoesNotExist:
            root = Root(letters=r)
            root.save()
    return root


def import_morphology_xml():
    d = parse(path_to('corpus/quranic-corpus-morphology-0.2.xml'))
    suras = d.getElementsByTagName('chapter')
    for s in suras:
        sura_number = int(s.getAttribute('number'))
        sura = Sura.objects.get(number=sura_number)
        ayas = s.getElementsByTagName('verse')
        for a in ayas:
            aya_number = int(a.getAttribute('number'))
            aya = Aya.objects.get(sura=sura, number=aya_number)
            words = a.getElementsByTagName('word')
            for w in words:
                number = int(w.getAttribute('number'))
                token = w.getAttribute('token')
                morphology = w.getAttribute('morphology')

                lemma = None
                dtoken = token
                root = extract_root(morphology)
                lem = extract_lem(morphology)
                if lem: dtoken = lem

                try:
                    lemma = Lemma.objects.get(token=dtoken)
                except Lemma.DoesNotExist:
                    lemma = Lemma(token=dtoken, root=root)
                    lemma.save()

                word = Word(sura=sura, aya=aya, number=number, token=token, root=root, lemma=lemma)
                word.save()

            print "[morphology] %d:%d" % (sura.number, aya.number)


def import_morphology_txt():
    sura = Sura.objects.get(number=2)
    aya = Aya.objects.get(sura=sura, number=2) # any aya except the first.
    f = open(path_to('corpus/quranic-corpus-morphology-0.2.txt'))

    line = f.readline()
    while len(line) > 0:
        parts = line.strip().split('|')
        sura_number = 0
        try:
            sura_number = int(parts[0])
        except ValueError:
            line = f.readline()
            continue
        aya_number = int(parts[1])
        word_number = int(parts[2])
        token = parts[3]
        morphology = parts[4]

        if aya_number is not aya.number:
            if sura_number is not sura.number:
                sura = Sura.objects.get(number=sura_number)
            aya = Aya.objects.get(sura=sura, number=aya_number)
            print "[morphology] %d:%d" % (sura.number, aya.number)

        lemma = None
        dtoken = token
        root = extract_root(morphology)
        lem = extract_lem(morphology)
        if lem: dtoken = lem

        try:
            lemma = Lemma.objects.get(token=dtoken)
        except Lemma.DoesNotExist:
            lemma = Lemma(token=dtoken, root=root)
            lemma.save()

        word = Word(sura=sura, aya=aya, number=word_number, token=token, root=root, lemma=lemma)
        word.save()

        line = f.readline()


def import_morphology():
    return import_morphology_txt()


def test_data(verbosity):
    verbosity = int(verbosity)
    print verbosity
    test_suite = unittest.TestLoader().loadTestsFromTestCase(DataIntegrityTestCase)
    unittest.TextTestRunner(verbosity=verbosity).run(test_suite)


class DataIntegrityTestCase(unittest.TestCase):
    def check_word(self, sura_number, aya_number, word_number, expected_word):
        sura = Sura.objects.get(number=sura_number)
        aya = sura.ayas.get(number=aya_number)
        word = aya.words.get(number=word_number)
        self.assertEquals(word.token, buckwalter_to_unicode(expected_word))

    def test_first_ayas(self):
        """
        Test the first ayas of some suras
        """
        self.check_word(1, 1, 3, u'{lr~aHoma`ni')
        self.check_word(2, 1, 1, u'Al^m^')
        self.check_word(114, 1, 1, u'qulo')

    def test_last_ayas(self):
        """
        Test the last ayas of some suras
        """
        self.check_word(1, 7, 2, u'{l~a*iyna')
        self.check_word(2, 286, 49, u'{loka`firiyna')
        self.check_word(114, 6, 3, u'wa{ln~aAsi')

    def test_yusuf_ali(self):
        """
        Test some ayas against Yusuf Ali
        """
        sura_number = 112
        aya_number = 4
        sura = Sura.objects.get(number=sura_number)
        aya = sura.ayas.get(number=aya_number)
        translation = QuranTranslation.objects.get(name='Yusuf Ali')
        t = aya.translations.get(translation=translation)
        self.assertEquals(t.text, 'And there is none like unto Him.')