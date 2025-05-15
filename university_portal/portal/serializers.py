from rest_framework import serializers
from .models import Announcement, Event, ScientificIdea, Comment


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class ScientificIdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScientificIdea
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
