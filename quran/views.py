from django.shortcuts import get_object_or_404, render_to_response
from quran.models import *

def index(request, template_name='quran/index.html'):
    suras = Sura.objects.all()
    return render_to_response(template_name, {'suras': suras})

def sura(request, sura_number, template_name='quran/sura.html'):
    try:
        sura = get_object_or_404(Sura, number=sura_number)
        ayas = sura.ayas.all()
    except Sura.DoesNotExist:
        raise Http404
    return render_to_response(template_name, {'sura': sura, 'ayas': ayas})

def aya(request, sura_number, aya_number, template_name='quran/aya.html'):
    try:
        sura = get_object_or_404(Sura, number=sura_number)
        aya = get_object_or_404(Aya, sura=sura, number=aya_number)
        words = aya.words.all()
    except Sura.DoesNotExist, Aya.DoesNotExist:
        raise Http404
    return render_to_response(template_name, {'sura': sura, 'aya': aya, 'words': words})

def word(request, sura_number, aya_number, word_number, template_name='quran/word.html'):
    aya = get_object_or_404(Aya, sura=sura_number, number=aya_number)
    word = get_object_or_404(Word, aya=aya, number=word_number)
    root = word.root
    return render_to_response(template_name, {'word': word, 'aya': aya, 'root': root})

def lemma(request, lemma_id, template_name='quran/lemma.html'):
    lemma = get_object_or_404(Lemma, pk=lemma_id)
    root = lemma.root
    words = lemma.word_set.all()
    ayas = lemma.ayas.distinct()
    return render_to_response(template_name, {'lemma': lemma, 'root': root, 'words': words, 'ayas': ayas})

def root(request, root_id, template_name='quran/root.html'):
    root = get_object_or_404(Root, pk=root_id)
    lemmas = root.lemmas.all()
    ayas = root.ayas.distinct()
    return render_to_response(template_name, {'root': root, 'lemmas': lemmas, 'ayas': ayas})