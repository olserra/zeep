from rest_framework import serializers
from .models import House


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ['id', 'fuid', 'vraagprijs', 'postcode', 'link', 'rdx', 'rdy', 'geom']
