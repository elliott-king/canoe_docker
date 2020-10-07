""" Seedfile
I am hard-coding these options, because it makes testing & development more consistent.

You can call this with `python manage.py seed --mode=[seed or clear]
"""
from django.core.management.base import BaseCommand
from django.utils import timezone

from datetime import datetime

from demo.models import Client, Fund, Investment, CashFlow

class Command(BaseCommand):
    """Controls cli usage"""
    help = "seed or clear database"

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="seed or clear")

    def handle(self, *args, **options):
        mode = options['mode']
        if not mode:
            mode = 'seed'
        if mode not in ['seed', 'clear']:
            raise NameError('Must specify mode of \'seed\' or \'clear\'')
        print('Clearing old data')
        clear_data()
        if mode == 'seed':
            print('Seeding data')
            seed_data()


def clear_data():
    # recommended to first delete models that depend on other models
    CashFlow.objects.all().delete()
    Investment.objects.all().delete()
    Fund.objects.all().delete()
    Client.objects.all().delete()

def seed_data():
    c1 = Client.objects.create(name="Client 1", description="Client 1 can view all funds", permission=['HF', 'PL', 'VC', 'RE', 'PC'])
    c2 = Client.objects.create(name="Client 2", description="Client 2 can only view VC and RE funds", permission=['VC', 'RE'])
    c3 = Client.objects.create(name="Client 3", description="Client 3 can only view PL and PC funds", permission=['PL', 'PC'])

    f1 = Fund.objects.create(name="ABC", type_field="HF", inception_date=timezone.make_aware(datetime(2018, 2, 1)), description="This is a fund of type HF")
    f2 = Fund.objects.create(name="DEF", type_field="VC", inception_date=timezone.make_aware(datetime(2018, 1, 1)), description="This is a fund of type VC")
    f3 = Fund.objects.create(name="XYZ", type_field="RE", inception_date=timezone.make_aware(datetime(2018, 1, 3)), description="This is a fund of type RE")
    f4 = Fund.objects.create(name="LMN", type_field="PC", inception_date=timezone.make_aware(datetime(2018, 1, 7)), description="This is a fund of type PC")
    f5 = Fund.objects.create(name="OPQ", type_field="PL", inception_date=timezone.make_aware(datetime(2018, 1, 18)), description="This is a fund of type PL")
    f6 = Fund.objects.create(name="RST", type_field="HF", inception_date=timezone.make_aware(datetime(2018, 2, 3)), description="This is a fund of type HF")
    f7 = Fund.objects.create(name="IJK", type_field="PC", inception_date=timezone.make_aware(datetime(2018, 1, 3)), description="This is a fund of type PC")

    i11 = Investment.objects.create(name="c1 investment in ABC", date=timezone.make_aware(datetime(2019, 1, 17)), amount=300.00, client=c1, fund=f1)
    i111 = Investment.objects.create(name="c1 second investment in ABC", date=timezone.make_aware(datetime(2019, 1, 23)), amount=400.00, client=c1, fund=f1)
    i12 = Investment.objects.create(name="c1 investment in DEF", date=timezone.make_aware(datetime(2019, 1, 17)), amount=700.00, client=c1, fund=f2)
    i13 = Investment.objects.create(name="c1 investment in XYZ", date=timezone.make_aware(datetime(2019, 1, 22)), amount=125.00, client=c1, fund=f3)
    i14 = Investment.objects.create(name="c1 investment in LMN", date=timezone.make_aware(datetime(2019, 1, 3)), amount=200.00, client=c1, fund=f4)
    i22 = Investment.objects.create(name="c2 investment in DEF", date=timezone.make_aware(datetime(2019, 2, 1)), amount=1000.00, client=c2, fund=f2)
    i23 = Investment.objects.create(name="c2 investment in XYZ", date=timezone.make_aware(datetime(2019, 2, 12)), amount=800.00, client=c2, fund=f3)
    i34 = Investment.objects.create(name="c3 investment in LMN", date=timezone.make_aware(datetime(2019, 3, 3)), amount=250.00, client=c3, fund=f4)
    i35 = Investment.objects.create(name="c3 investment in OPQ", date=timezone.make_aware(datetime(2019, 3, 6)), amount=750.00, client=c3, fund=f5)

    c11 = CashFlow.objects.create(date=timezone.make_aware(datetime(2020, 7,2)), return_field=5.00, investment=i11)
    c111 = CashFlow.objects.create(date=timezone.make_aware(datetime(2020, 7,2)), return_field=5.00, investment=i111)
    c12 = CashFlow.objects.create(date=timezone.make_aware(datetime(2020, 7,2)), return_field=5.00, investment=i12)
    c13 = CashFlow.objects.create(date=timezone.make_aware(datetime(2020, 7,2)), return_field=5.00, investment=i13)
    c14 = CashFlow.objects.create(date=timezone.make_aware(datetime(2020, 7,2)), return_field=5.00, investment=i14)
    c22 = CashFlow.objects.create(date=timezone.make_aware(datetime(2020, 7,2)), return_field=5.00, investment=i22)
    c23 = CashFlow.objects.create(date=timezone.make_aware(datetime(2020, 7,2)), return_field=5.00, investment=i23)
    c34 = CashFlow.objects.create(date=timezone.make_aware(datetime(2020, 7,2)), return_field=5.00, investment=i34)
    c35 = CashFlow.objects.create(date=timezone.make_aware(datetime(2020, 7,2)), return_field=5.00, investment=i35)