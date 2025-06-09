from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User
from .serialazers import TelegramTokenSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError, NotFound

class TelegramTokenView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=TelegramTokenSerializer)
    def post(self, request):
        serializer = TelegramTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        telegram_id = serializer.validated_data['telegram_id']

        try:
            user = User.objects.get(user_telegram_id=str(telegram_id))
        except User.DoesNotExist:
            raise ValidationError({"telegram_id": "Bunday telegram_id li foydalanuvchi mavjud emas"})

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })

