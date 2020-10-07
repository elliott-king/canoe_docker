from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

ACCEPTED = ['HF', 'PL', 'VC', 'RE', 'PC']

class Client(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    permission = models.JSONField()

    def __str__(self):
        return '{} - {}'.format(self.name, self.permission)

    def can_view(self, fund):
        return fund.type_field in self.permission

# Note that validators only run on the application side
# If you create an instance in the shell, it will not run validation
def validate_type(value):
    if value not in ACCEPTED:
        raise ValidationError(
            gettext_lazy('%(value)s is not an accepted type'),
            params={'value': value},
        )

class Fund(models.Model):
    name = models.CharField(max_length=80)

    # using reserved words as fields
    # https://stackoverflow.com/questions/47630356
    type_field = models.CharField('type', db_column='type', max_length=2, validators=[validate_type])
    inception_date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return '{} ({}) - {}'.format(self.name, self.type_field, self.inception_date)

    def obfuscate(self):
        obfuscated = Fund(type_field=self.type_field, name='***', inception_date='*****', description='******')
        return obfuscated

class Investment(models.Model):
    name = models.CharField(max_length=80)
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=11, decimal_places=2)

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({}) - {}'.format(self.name, self.amount, self.date)

    # Decimals serialize a bit weirdly
    def current_value(self):
        try:
            latest_cf = self.cashflow_set.latest('date')
        except CashFlow.DoesNotExist:
            return float(self.amount)
        return float(self.amount) + (float(self.amount) * 0.01 * float(latest_cf.return_field))

class CashFlow(models.Model):
    date = models.DateTimeField()

    # project pdf seems to imply that percentages could be stored as whole numbers
    # for our purposes, I will indicate a return of 5% as 5.00
    # argument could also be made that 5% should be indicated by 0.05
    # I decided to try and follow the prompt from the pdf
    return_field = models.DecimalField('return', db_column='return', max_digits=11, decimal_places=2)

    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.date, self.return_field)