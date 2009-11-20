from django.conf.urls.defaults import *

urlpatterns = patterns('quran.views',
    (r'^$', 'index'),
    (r'^(?P<sura_number>\d+)/$', 'sura'),
    (r'^(?P<sura_number>\d+)/(?P<aya_number>\d+)/$', 'aya'),
    (r'^(?P<sura_number>\d+)/(?P<aya_number>\d+)/(?P<word_number>\d+)/$', 'word'),

    (r'^word/(?P<word_id>\d+)/$', 'unique_word'),
    (r'^root/(?P<root_id>\d+)/$', 'root'),
)