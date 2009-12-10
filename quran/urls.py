from django.conf.urls.defaults import *

urlpatterns = patterns('quran.views',
    url(r'^$', 'index', name='quran_index'),
    url(r'^(?P<sura_number>\d+)/$', 'sura', name='quran_sura'),
    url(r'^(?P<sura_number>\d+)/(?P<aya_number>\d+)/$', 'aya', name='quran_aya'),
    url(r'^(?P<sura_number>\d+)/(?P<aya_number>\d+)/(?P<word_number>\d+)/$', 'word', name='quran_word'),

    url(r'^lemma/(?P<lemma_id>\d+)/$', 'lemma', name='quran_lemma'),
    url(r'^root/(?P<root_id>\d+)/$', 'root', name='quran_root'),
    url(r'^root/$', 'root_index', name='quran_root_list'),
)