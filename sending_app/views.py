import json
from django.contrib.auth import login, authenticate
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from uuid import uuid4
from .serializers import RegistrationUserSerializer, MessageSerializer
from .models import Token, TelegramUser, Message
from sending_app.management.commands.telegrambot import bot as tel_bot


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationUserSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'message': 'User registered successfully',
                'access_token': access_token,
                'refresh_token': refresh_token,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_telegram_message(chat_id, message_text):
    bot = tel_bot
    bot.send_message(chat_id=chat_id, text=message_text)


class TokenGenerationView(views.APIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = json.loads(request.body)
        user = request.user
        try:
            telegram_given_id = data.get('telegram_given_id')
            try:
                telegram_user = TelegramUser.objects.get(user_id=telegram_given_id)
                token_value = uuid4()
                Token.objects.create(user=user, token=token_value, telegram_user=telegram_user)
                message_text = f'Вы успешно зарегистрировались в чате. Теперь вы можете писать сообщения через приложение, а я буду их дублировать здесь.'
                send_telegram_message(telegram_user.chat_id, message_text)
                return Response({'message': 'Token created successfully'}, status=status.HTTP_201_CREATED)
            except:
                return Response({'message': 'Account already exists!'}, status=status.HTTP_403_FORBIDDEN)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class MessageCreateAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )

    def perform_create(self, serializer):
        # Получить текущего пользователя
        user = self.request.user
        # Получить текущий токен пользователя
        try:
            current_token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            return Response({'error': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)

        # Получить чат ID пользователя из токена
        chat_id = current_token.telegram_user.chat_id

        # Получить текст сообщения из запроса
        message_text = self.request.data.get('body', '')

        # Создать объект сообщения
        serializer.save(body=message_text)

        # Отправить сообщение в Telegram
        send_telegram_message(chat_id, f"{user.first_name} {user.last_name}, я получил от тебя сообщение:\n{message_text}")

        return Response({'message': 'Message sent successfully'}, status=status.HTTP_201_CREATED)


class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        # Получить текущего пользователя из запроса
        user = self.request.user

        # Фильтровать сообщения для текущего пользователя
        queryset = Message.objects.filter(owner=user)

        return queryset

