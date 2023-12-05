from django.test import TestCase

from myfinances.apps import MyFinancesConfig


class AppConfigTest(TestCase):
    def test(self):
        self.assertEqual(MyFinancesConfig.name, 'myfinances')
