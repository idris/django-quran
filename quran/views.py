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
    sura = get_object_or_404(Sura, number=sura_number)
    aya = get_object_or_404(Aya, sura=sura, number=aya_number)
    word = get_object_or_404(Word, aya=aya, number=word_number)
    root = word.root
    ayas = []
    return render_to_response(template_name, {'word': word, 'root': root, 'ayas': ayas})

def distinct_word(request, distinct_word_id, template_name='quran/distinct_word.html'):
    word = get_object_or_404(DistinctWord, pk=distinct_word_id)
    root = word.root
    words = word.word_set.all()
    return render_to_response(template_name, {'word': word, 'root': root, 'words': words})

def root(request, root_id, template_name='quran/root.html'):
    root = get_object_or_404(Root, pk=root_id)
    words = root.words.all()
    return render_to_response(template_name, {'root': root, 'words': words})