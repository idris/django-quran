"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

import doctest
from quran import buckwalter
from django.test import TestCase

class BuckwalterTest(TestCase):
    def test_buckwalter(self):
        """
        Test the buckwalter.py library.
        """
        doctest.testmod(buckwalter)