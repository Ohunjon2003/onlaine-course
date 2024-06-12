from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import Direction,Courses,Teacher,Lesson,Comments,Notifications,UploadVideo
from .serializers import DirectionSerializer,CoursesSerializer,TeacherSerializer,LessonSerializer,CommentsSerializer,NotificationSerializer,UploadVideoSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        notification = serializer.save()
        if notification.dispatch:
            subject = "New Notification"
            message = notification.message
            recipient_list = [notification.email.email]
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            notification.dispatch = True
            notification.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            notification = Notifications.objects.get(id=response.data['id'])
            if notification.dispatch:
                subject = "New Notification"
                message = notification.message
                recipient_list = [notification.email.email]
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
                notification.dispatch = True
                notification.save()
        return response
