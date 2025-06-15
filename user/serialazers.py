from rest_framework import serializers
from user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'phone_number')
