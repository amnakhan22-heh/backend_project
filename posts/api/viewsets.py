from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from comments.api.serializers import CommentSerializer
from .serializers import PostSerializer
from posts.models import Post
from posts.permissions import CanAccessPosts
from rest_framework.response import Response
from comments.models import Comment

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes =  (CanAccessPosts, IsAuthenticated)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user)
            return Response({
                    "detail": "Post successfully created",
                    "Post": serializer.data
                }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response({
            "detail": "Post successfully deleted",
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='comments')
    def add_comments(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, post = post)

        return Response({"detail": "Comment successfully added",
                         "comments": serializer.data
                         }, status=status.HTTP_201_CREATED)

    # @action(detail=True, methods=['post'], url_path='reply')
    # def add_replies(self, request, pk=None):
    #     try:
    #         post = self.get_object(id=pk)
    #         parent_comment =
    #

    @action(detail=True, methods=['post'], url_path='comment/(?P<comment_id>[^/.]+)')
    def reply(self, request, pk=None, comment_id=None):
        """
        pk = post_id (from URL)
        comment_id = parent comment id
        """
        post = get_object_or_404(Post, id=pk)
        parent_comment = get_object_or_404(Comment, id=comment_id, post=post)

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, post=post, parent=parent_comment)

        return Response({
            "detail": "Reply successfully created",
            "reply": serializer.data
        }, status=status.HTTP_201_CREATED)




