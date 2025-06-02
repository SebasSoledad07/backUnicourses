from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Course
from .serializers import CourseSerializer
from accounts.permissions import IsAdminOrReadOnly

# Create your views here.

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'career', 'description']
    ordering_fields = ['title', 'career', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True)
        
        # Filtrar por carrera si se proporciona
        career = self.request.query_params.get('career', None)
        if career:
            queryset = queryset.filter(career=career)
            
        # Filtrar por intereses si se proporcionan
        interest_ids = self.request.query_params.getlist('interests', [])
        if interest_ids:
            queryset = queryset.filter(interests__id__in=interest_ids).distinct()
            
        return queryset
