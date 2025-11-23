from rest_framework import serializers
from comments.api.serializers import CommentSerializer
from posts.models import Post

class PostSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source='id', read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    content = serializers.CharField(required=True, allow_blank=False)
    comments = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['post_id', 'content', 'username', 'liked_by', 'total_likes', 'created_at', 'comments']

    def get_comments(self, obj):
        top_comments = obj.comments.filter(parent__isnull=True)
        return CommentSerializer(top_comments, many=True).data

    def get_liked_by(self, obj):
        return [user.username for user in obj.likes.all()]

    def get_total_likes(self, obj):
        return obj.likes.count()


