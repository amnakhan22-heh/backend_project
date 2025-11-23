from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer
from posts.models import Post
from posts.permissions import CanAccessPosts
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import action



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().prefetch_related('comments__replies',
    'comments__user'
)
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
        except serializers.ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response({
            "detail": "Post successfully deleted",
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods = ['post'])
    def reaction(self, request, pk=None):
        user = self.request.user
        post = self.get_object()

        if user in post.likes.all():
            post.likes.remove(user)
            return Response({"status":"unliked post successfully"}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response({"status":"liked post successfully"}, status=status.HTTP_200_OK)





