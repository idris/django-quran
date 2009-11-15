from django.core.management.base import NoArgsCommand
from quran.data import *

class Command(NoArgsCommand):
    help = "Load initial Quran data."

    def handle_noargs(self, **options):
        import_quran()
        print "----- done importing quran data. starting morphology -----"
        import_morphology()