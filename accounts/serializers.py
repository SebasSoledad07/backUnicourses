from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Interest

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['email', 'career_interest', 'interests']


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    intereses = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'intereses')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        intereses_data = validated_data.pop('intereses', [])

        # Crear el usuario
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        # Crear el perfil del usuario
        user_profile = UserProfile.objects.create(user=user)

        # Asociar intereses al perfil
        for interest_name in intereses_data:
            interest_obj, created = Interest.objects.get_or_create(name=interest_name)
            user_profile.interests.add(interest_obj)

        return user