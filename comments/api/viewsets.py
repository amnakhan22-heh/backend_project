from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .serializers import CommentSerializer
from comments.models import Comment
from comments.permissions import CanAccessComments
from rest_framework.response import Response
from rest_framework import serializers

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CanAccessComments]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response({'detail':"Comment created successfully", "comment": serializer.data}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response({
            "detail": "Comment successfully deleted",
        }, status=status.HTTP_200_OK)

