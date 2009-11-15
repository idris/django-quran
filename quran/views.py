from django.shortcuts import get_object_or_404, render_to_response
from quran.models import *

def index(request):
    suras = Sura.objects.all()
    return render_to_response('quran/index.html', {'suras': suras})

def sura(request, sura_number):
    try:
        sura = get_object_or_404(Sura, number=sura_number)
        ayas = sura.aya_set.all()
    except Sura.DoesNotExist:
        raise Http404
    return render_to_response('quran/sura.html', {'sura': sura, 'ayas': ayas})

def aya(request, sura_number, aya_number):
    try:
        sura = get_object_or_404(Sura, number=sura_number)
        aya = get_object_or_404(Aya, sura=sura, number=aya_number)
        words = aya.word_set.all()
    except Sura.DoesNotExist, Aya.DoesNotExist:
        raise Http404
    return render_to_response('quran/aya.html', {'aya': aya, 'words': words})

def word(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    root = word.root
    ayas = []
    return render_to_response('quran/word.html', {'word': word, 'root': root, 'ayas': ayas})

def root(request, root_id):
    root = get_object_or_404(Root, pk=root_id)
    words = root.word_set.all()
    return render_to_response('quran/root.html', {'root': root, 'words': words})