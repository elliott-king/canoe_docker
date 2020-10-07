import json

from demo.models import Client, Fund, Investment, CashFlow
from demo.serializers import ClientSerializer, FundSerializer, InvestmentSerializer
from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.middleware.csrf import get_token
from django.utils import dateparse

def index(request):
    clients = Client.objects.all()
    clients_serializer = ClientSerializer(clients, many=True)
    return JsonResponse({'clients': clients_serializer.data})

def detail(request, client_id):
    if request.method == 'GET':
        client = get_object_or_404(Client, pk=client_id)
        funds = Fund.objects.all()
        funds = map(lambda f: f if client.can_view(f) else f.obfuscate(), funds)

        client_serializer = ClientSerializer(client)
        funds_serializer = FundSerializer(funds, many=True)
        response = {
            'client': client_serializer.data,
            'funds': funds_serializer.data,
        }
        return JsonResponse(response)

    
# Note that for the form to dynamically change depending on the selections,
# we need to pass pretty much everything to the frontend. This will cause
# scaling issues in large databases.

# One way to fix this is by making a request whenever a dropdown is changed
# (a bit slow). Alternatively, if auth was in-built, we could just show values
# for current logged in user.
def cash_flow(request):
    if request.method == 'GET':
        get_token(request) # Inserts CRSF token into response
        clients = Client.objects.all()
        fund_types = {}
        for client in clients:
            fund_types[client.id] = client.permission
        investments = Investment.objects.all()

        clients_serializer = ClientSerializer(clients, many=True)
        investments_serializer = InvestmentSerializer(investments, many=True)
        response = {
            'clients': clients_serializer.data,
            'investments': investments_serializer.data,
            'fund_types': fund_types,
        }
        return JsonResponse(response)
    if request.method == 'POST':
        params = json.loads(request.body)
        CashFlow.objects.create(
            date=dateparse.parse_datetime(params['date']),
            investment_id=params['investment_id'],
            return_field=params['return'])
        investments = Investment.objects.all()
        investments_serializer = InvestmentSerializer(investments, many=True)
        return JsonResponse({'investments': investments_serializer.data})