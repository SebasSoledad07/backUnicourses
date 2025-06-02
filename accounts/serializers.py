from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Interest
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name']

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    nombres = serializers.CharField(required=True)
    apellidos = serializers.CharField(required=True)
    interests = InterestSerializer(many=True, read_only=True)
    interest_ids = serializers.PrimaryKeyRelatedField(
        queryset=Interest.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='interests'
    )

    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'nombres', 'apellidos', 'role', 'career_interest', 
                 'interests', 'interest_ids', 'profile_picture']
        read_only_fields = ['role']

    def update(self, instance, validated_data):
        if 'interests' in validated_data:
            instance.interests.set(validated_data.pop('interests'))
        return super().update(instance, validated_data)

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    password = serializers.CharField(write_only=True, required=False)
    password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'password_confirm', 'profile']
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate(self, attrs):
        if 'password' in attrs:
            if attrs['password'] != attrs.get('password_confirm'):
                raise serializers.ValidationError({"password": "Las contraseñas no coinciden"})
            validate_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        
        # Crear usuario con email como username
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email']
        )
        user.set_password(password)
        user.save()
        
        # Crear perfil
        UserProfile.objects.create(
            user=user,
            nombres=profile_data['nombres'],
            apellidos=profile_data['apellidos'],
            role=profile_data.get('role', 'student')
        )
        
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        
        if 'profile' in validated_data:
            profile_data = validated_data.pop('profile')
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
            
        return super().update(instance, validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    nombres = serializers.CharField(required=True)
    apellidos = serializers.CharField(required=True)
    interest_ids = serializers.PrimaryKeyRelatedField(
        queryset=Interest.objects.all(),
        many=True,
        required=False,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'nombres', 'apellidos', 'interest_ids']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        interest_ids = validated_data.pop('interest_ids', [])
        nombres = validated_data.pop('nombres')
        apellidos = validated_data.pop('apellidos')
        
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        profile = UserProfile.objects.create(
            user=user,
            nombres=nombres,
            apellidos=apellidos,
            role='student'
        )
        
        if interest_ids:
            profile.interests.set(interest_ids)
        
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        if hasattr(user, 'profile'):
            token['role'] = user.profile.role
            token['nombres'] = user.profile.nombres
            token['apellidos'] = user.profile.apellidos
        return token

    def validate(self, attrs):
        attrs['username'] = attrs.get('email')
        return super().validate(attrs)