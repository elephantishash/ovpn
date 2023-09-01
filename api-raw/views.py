from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from account.models import Account, Server
from .serializers import AccountSerializer, ServerSerializer
from django.http import JsonResponse

@api_view(['GET', 'POST'])
def getData(request, format=None):
    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response({'accounts': serializer.data})
    elif request.method == 'POST':
        serializer = ServerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
