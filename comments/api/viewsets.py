from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .serializers import CommentSerializer
from comments.models import Comment
from comments.permissions import CanAccessComments
from rest_framework.response import Response

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CanAccessComments]
    http_method_names = ['get', 'put', 'patch', 'delete']

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response({
            "detail": "Comment successfully deleted",
        }, status=status.HTTP_200_OK)

