from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer

class RegisterView(APIView):
    def post(self, request):
        data = request.data

        # Validar que no exista el email
        if User.objects.filter(email=data["email"]).exists():
            return Response({"error": "El email ya está registrado"}, status=status.HTTP_400_BAD_REQUEST)

        # Crear usuario
        user = User.objects.create(
            username=data["email"],
            email=data["email"],
            first_name=data.get("fullname", ""),
            password=make_password(data["password"])
        )

        # Crear perfil asociado con intereses y carrera
        UserProfile.objects.create(
            user=user,
            career_interest=data.get("career_interest", ""),
            interests=data.get("intereses", [])
        )

        return Response({"message": "Usuario creado correctamente"}, status=status.HTTP_201_CREATED)
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            return Response({"message": "Login exitoso"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)


class PerfilUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Perfil actualizado con éxito"})
        return Response(serializer.errors, status=400)
    

