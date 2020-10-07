"""Run with `python manage.py test demo`"""
from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta

from demo.models import *

class ClientModelTests(TestCase):

    def test_can_view_fund_in_permission(self):
        c1 = Client(permission=['HF'])
        c2 = Client(permission=['HF', 'PV'])
        f = Fund(type_field='HF')

        self.assertTrue(c1.can_view(f))
        self.assertTrue(c2.can_view(f))

    def test_cannot_view_fund_not_in_permission(self):
        c1 = Client(permission=['HF'])
        c2 = Client(permission=['HF', 'PV'])
        f = Fund(type_field='VC')

        self.assertFalse(c1.can_view(f))
        self.assertFalse(c2.can_view(f))
        
class FundModelTests(TestCase):

    def test_validator(self):
        f = Fund(name='General Grevious', inception_date=timezone.now(), type_field='General Kenobi!', description='test')
        with self.assertRaisesRegexp(ValidationError, 'not an accepted type'):
            f.full_clean()

    def test_obfuscator(self):
        fund = Fund(name='General Grevious', inception_date=timezone.now(), type_field='General Kenobi!', description='test')
        f = fund.obfuscate()
        self.assertEqual(f.type_field, 'General Kenobi!')
        self.assertEqual(f.name, '***')
        self.assertEqual(f.inception_date, '*****')
        self.assertEqual(f.description, '******')

class InvestmentModelTests(TestCase):
    def setUp(self):
        self.c = Client.objects.create(name="Client 1", description="Client 1 can view all funds", permission=['HF', 'PL', 'VC', 'RE', 'PC'])
        self.f = Fund.objects.create(name="ABC", type_field="HF", inception_date=timezone.make_aware(datetime(2018, 2, 1)), description="This is a fund of type HF")
        self.i = Investment.objects.create(name="test", date=timezone.now(), amount=500.00, client=self.c, fund=self.f)

    def test_current_value_no_cashflows(self):
        i = Investment(amount=1000.00)
        self.assertEqual(i.current_value(), 1000.00)

    def test_current_value_with_one_cf(self):
        cf = CashFlow.objects.create(return_field=5.00, date=timezone.now(), investment=self.i)
        self.assertEqual(self.i.current_value(), 525.00)

    # There are a few other edge cases I could look at (eg, dates in future).
    # Keeping it simple for now.
    def test_current_value_multiple_cfs(self):
        CashFlow.objects.create(return_field=9.00, date=timezone.now()-timedelta(days=3), investment=self.i)
        CashFlow.objects.create(return_field=1.00, date=timezone.now(), investment=self.i)
        CashFlow.objects.create(return_field=10.00, date=timezone.now()-timedelta(days=2), investment=self.i)
        self.assertEqual(self.i.current_value(), 505.00)