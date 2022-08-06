from rest_framework import serializers

from .models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta():
        model = File
        fields = '__all__'


class FileSerializerPartialUpdate(serializers.ModelSerializer):
    class Meta():
        model = File
        fields = ['request_accept', 'unblocking_information']
