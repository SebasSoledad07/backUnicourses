from rest_framework import serializers
from .models import Course
from accounts.serializers import InterestSerializer
from accounts.models import Interest

class CourseSerializer(serializers.ModelSerializer):
    interests = InterestSerializer(many=True, read_only=True)
    interest_ids = serializers.PrimaryKeyRelatedField(
        queryset=Interest.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='interests'
    )

    class Meta:
        model = Course
        fields = ['id', 'title', 'career', 'description', 'interests', 
                 'interest_ids', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        interests = validated_data.pop('interests', [])
        course = Course.objects.create(**validated_data)
        if interests:
            course.interests.set(interests)
        return course

    def update(self, instance, validated_data):
        if 'interests' in validated_data:
            instance.interests.set(validated_data.pop('interests'))
        return super().update(instance, validated_data) 