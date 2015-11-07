from .serializers import HouseSerializer
from .models import House
from rest_framework import viewsets


class HouseViewSet(viewsets.ModelViewSet):
    #import pdb;pdb.set_trace()
    queryset = House.objects.all()
    serializer_class = HouseSerializer
