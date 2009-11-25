import doctest
from quran import buckwalter
from django.test import TestCase

class BuckwalterTest(TestCase):
    def test_buckwalter(self):
        """
        Test the buckwalter.py library.
        """
        doctest.testmod(buckwalter)