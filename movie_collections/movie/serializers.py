from rest_framework import serializers
from . models import Collection

class CollectionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)