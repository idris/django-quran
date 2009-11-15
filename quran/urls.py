from django.conf.urls.defaults import *

urlpatterns = patterns('quran.views',
    (r'^$', 'index'),
    (r'^(?P<sura_number>\d+)/$', 'sura'),
    (r'^(?P<sura_number>\d+)/(?P<aya_number>\d+)/$', 'aya'),
    (r'^word/(?P<word_id>\d+)/$', 'word'),
    (r'^root/(?P<root_id>\d+)/$', 'root'),
)