from rest_framework import serializers
from delve import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Profile
        fields = ['url', 'last_name', 'email', 'groups']


class ComboSerializer(serializers.HyperlinkedModelSerializer):
    xxxtentacion = "sad"
    class Meta:
        model = models.Combo
        fields = ['name']
