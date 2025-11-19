from rest_framework import serializers
from comments.models import Comment
from posts.models import Post

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), write_only=True, required=False, allow_null=True)
    username = serializers.CharField(source="user.username", read_only=True)
    text = serializers.CharField(required=True, allow_blank=False)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id','username','text', 'created_at', 'parent','post', 'replies']
        read_only_fields = ['id' ,'user','created_at']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data #refers to replies of a comment in the same table using fk relationship
        return []


