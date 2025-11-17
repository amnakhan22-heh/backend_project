from rest_framework import serializers
from comments.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    text = serializers.CharField(required=True, allow_blank=False)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id','username','text', 'created_at', 'parent','post', 'replies']
        read_only_fields = ['id' ,'user','created_at','updated_at','post']

    def get_replies(self, obj):
        if obj.replies is not None:
            return CommentSerializer(obj.replies.all(), many=True).data #refers to replies of a comment in the same table using fk relationship
        return []

