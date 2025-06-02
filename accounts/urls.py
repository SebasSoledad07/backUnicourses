from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, UserProfileViewSet, CreateAdminView,
    ProfilePictureView, InterestViewSet, UserViewSet
)
from .serializers import CustomTokenObtainPairSerializer

router = DefaultRouter()
router.register(r'interests', InterestViewSet)
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('create-admin/', CreateAdminView.as_view(), name='create-admin'),
    path('profile/picture/', ProfilePictureView.as_view(), name='profile-picture'),
    path('login/', TokenObtainPairView.as_view(
        serializer_class=CustomTokenObtainPairSerializer
    ), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]