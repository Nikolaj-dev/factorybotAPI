from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message


class RegistrationUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'password1', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ['owner']

    def create(self, validated_data):
        # Получить текущего пользователя из запроса
        user = self.context['request'].user

        # Добавить текущего пользователя как владельца сообщения
        validated_data['owner'] = user

        # Создать и вернуть объект сообщения
        message = Message.objects.create(**validated_data)
        return message
