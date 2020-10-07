from django.contrib import admin

from .models import Client, Fund, Investment, CashFlow

admin.site.register(Client)
admin.site.register(Fund)
admin.site.register(Investment)
admin.site.register(CashFlow)
