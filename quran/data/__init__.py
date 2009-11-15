import re
from os import path
from xml.dom.minidom import parse, parseString

from quran.models import *
from quran.buckwalter import *


def import_quran():
    currpath = path.dirname(__file__)
    d = parse(path.join(currpath, 'tanzil/quran-data.xml'))
    d2 = parse(path.join(currpath, 'tanzil/quran-uthmani.xml'))
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


def import_morphology():
    currpath = path.dirname(__file__)
    d = parse(path.join(currpath, 'corpus/quranic-corpus-morphology-0.1.xml'))
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
                p = re.compile('ROOT:(?P<root>[^ "]+)')
                m = p.search(morphology)
                r = ''
                word = None
                if(m):
                    r = m.group('root')
                if(len(r) > 0):
                    r = buckwalter_to_unicode(r)
                    try:
                        root = Root.objects.get(letters=r)
                    except Root.DoesNotExist:
                        root = Root(letters=r)
                        root.save()
                    word = Word(aya=aya, number=number, token=token, root=root)
                else:
                    word = Word(aya=aya, number=number, token=token)
                word.save()

            print "%d:%d" % (sura.number, aya.number)
