from rest_framework import serializers
from comments.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    text = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = Comment
        fields = ['id', 'user','username','text', 'created_at', 'updated_at']
        read_only_fields = ['user','created_at','updated_at']
