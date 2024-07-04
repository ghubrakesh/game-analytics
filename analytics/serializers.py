from rest_framework import serializers
from datetime import datetime
from .models import *


class CustomDateField(serializers.Field):
    def to_representation(self, value):
        return value.strftime('%b %d, %Y')

    def to_internal_value(self, data):
        try:
            return datetime.strptime(data, '%b %d, %Y').date()
        except ValueError:
            raise serializers.ValidationError("date format should be: 'Oct 21, 2008'")

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class GameDataSerializer(serializers.ModelSerializer):
    release_date = CustomDateField()
    supported_languages = serializers.ListField(
        child = serializers.CharField()
    )
    class Meta:
        model = GameData
        fields = '__all__'
