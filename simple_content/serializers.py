from rest_framework.response import Response

from simple_content.models import Content
from rest_framework import serializers, permissions, authentication


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['pk', 'title', 'slug', 'content', 'parent']
