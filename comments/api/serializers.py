from rest_framework import serializers
from comments.models import Comment
from posts.models import Post

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.IntegerField(write_only=True)
    parent = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    username = serializers.CharField(source="user.username", read_only=True)
    text = serializers.CharField(required=True, allow_blank=False)
    replies = serializers.SerializerMethodField()
    post_id = serializers.IntegerField(source="post.id",read_only=True)

    class Meta:
        model = Comment
        fields = ['id','username','text', 'created_at', 'parent','post', 'post_id', 'replies']
        read_only_fields = ['id' ,'user','created_at']

    def validate_post(self, value):
        if type(value) is not int:
            raise serializers.ValidationError("Post value must be an integer")
        try:
            post = Post.objects.get(id=value)
        except Post.DoesNotExist:
            raise serializers.ValidationError(f"Post with id {value} does not exist")
        return post

    def validate_parent(self, value):
        if value is None:
            return None
        if type(value) is not int:
            raise serializers.ValidationError("Parent value must be an integer")
        try:
            parent = Comment.objects.get(id=value)
        except Comment.DoesNotExist:
            raise serializers.ValidationError(f"Parent comment with id {value} does not exist")
        return parent

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data #refers to replies of a comment in the same table using fk relationship
        return []


