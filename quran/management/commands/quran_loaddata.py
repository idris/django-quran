from django.core.management.base import NoArgsCommand
from quran.data import *

class Command(NoArgsCommand):
    help = "Load initial Quran data."

    def handle_noargs(self, **options):
        if Aya.objects.count() > 0:
            print 'The quran database must be empty before running quran_loaddata. Running tests.'
            test_data(verbosity=options['verbosity'])
            return

        print "----- importing quran data (Tanzil) -----"
        import_quran()

        print "----- done importing quran data (Tanzil). starting translations -----"
        import_translations()

        print "----- done importing translations. starting morphology -----"
        import_morphology()

        print "----- done importing morphology. running tests -----"
        test_data(verbosity=options['verbosity'])