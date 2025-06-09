from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TelegramTokenSerializer(serializers.Serializer):
    telegram_id = serializers.CharField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if not user.user_telegram_id:
            raise serializers.ValidationError("Telegram ID yo‘q!")

        token = super().get_token(user)
        token['telegram_id'] = user.user_telegram_id
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token
