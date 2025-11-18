from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer
from posts.models import Post
from posts.permissions import CanAccessPosts
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes =  (CanAccessPosts, IsAuthenticated)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response({
                    "detail": "Post successfully created",
                    "Post": serializer.data
                }, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response({
            "detail": "Post successfully deleted",
        }, status=status.HTTP_200_OK)



