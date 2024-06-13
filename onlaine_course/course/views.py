from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView

from .models import Direction,Courses,Teacher,Lesson,Comments,Notifications,UploadVideo,Like
from .serializers import DirectionSerializer,CoursesSerializer,TeacherSerializer,LessonSerializer,CommentsSerializer,NotificationSerializer,UploadVideoSerializer,LikeSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class DirectionViewSet(viewsets.ModelViewSet):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CoursesViewSet(viewsets.ModelViewSet):
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer
    permission_classes = [IsAuthorOrReadOnly,IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['direction','name','author']
    search_fields = ['author__username','name','direction__name']
    ordering_fields = ['beginning','name']

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['full_name']
    search_fields = ['full_name']
    ordering_fields = ['full_name','experience']

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['course','title']
    search_fields = ['course__name','^title']
    ordering_fields = ['created']



class UploadVideoViewSet(viewsets.ModelViewSet):
    queryset = UploadVideo.objects.all()
    serializer_class = UploadVideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['lesson']
    search_fields = ['lesson']
    ordering_fields = ['lesson']


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['author','lesson']
    search_fields = ['^lesson__title','author__username']
    ordering_fields = ['created','lesson']



class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        notification = serializer.save()

        subject = notification.title
        message = notification.message

        users = User.objects.all()
        recipient_list = [user.email for user in users if user.email]

        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)






class LikeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            l_value = serializer.validated_data.get('like')
            d_value = serializer.validated_data.get('dislike')
            lesson_id = serializer.validated_data.get('lesson')
            lesson = Lesson.objects.get(pk=lesson_id)

            try:
                like = Like.objects.get(
                    lesson=lesson,
                    user=request.user
                )
                like.delete()
            except Like.DoesNotExist:
                like_or_dislike = True if l_value else False
                Like.objects.create(
                    lesson=lesson,
                    user=request.user,
                    like_or_dislike=like_or_dislike
                )
            return Response({'success': "Muvofaqiyatli!!!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def list(self, request):
        serializer = LikeSerializer()
        return Response(serializer.data)