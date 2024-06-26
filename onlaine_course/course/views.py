from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import Direction,Courses,Teacher,Lesson,Comments,Notifications,UploadVideo,Like
from .serializers import (DirectionSerializer,CoursesSerializer,TeacherSerializer,LessonSerializer,
                          CommentsSerializer,NotificationSerializer,UploadVideoSerializer,LikeSerializer)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class DirectionViewSet(viewsets.ModelViewSet):
    ''' bu ViewSet orqali yonalishlar va ular haqidagi malumotlarni  chiqarib beradi va adminuserlarga CRUD qilishga,yangi yo'nalishlarni qo'shishga
    imkon beradi, userlar malumotlarni filter qilsa va izlasa bo'ladi'''
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name','description']
    ordering_fields = ['name']


class CoursesViewSet(viewsets.ModelViewSet):
    '''bu ViewSet mavjud kurslar va ular haqidagi to'liq malumotlarni chiqarib beradi va adminuserlarga CRUD qilishga
    imkon beradi, userlar malumotlarni filter qilsa va izlasa bo'ladi'''
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['direction','name','author']
    search_fields = ['author__username','name','direction__name','description']
    ordering_fields = ['beginning','name']

class TeacherViewSet(viewsets.ModelViewSet):
    '''bu ViewSet ustozlar haqidagi malumotlarni chiqarib beradi va adminuserlarga CRUD qilishga,yangi ustozlar va va ular haqidagi malumotlarni
    qo'shishga imkon beradi, userlar malumotlarni filter qilsa va izlasa bo'ladi'''
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['full_name']
    search_fields = ['full_name']
    ordering_fields = ['full_name','experience']

class LessonViewSet(viewsets.ModelViewSet):
    ''' bu ViewSet orqali darsni  chiqarib beradi va adminuserlarga CRUD qilishga,yangi darslarni qo'shishga
    imkon beradi, userlar malumotlarni filter qilsa va izlasa bo'ladi'''
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['course','title']
    search_fields = ['course__name','^title','description']
    ordering_fields = ['created']


class UploadVideoViewSet(viewsets.ModelViewSet):
    ''' bu ViewSet orqali dars uchun vidyolarni  chiqarib beradi va adminuserlarga CRUD qilishga,yangi vidyolarni qo'shishga
    imkon beradi, userlar malumotlarni filter qilsa va izlasa bo'ladi'''
    queryset = UploadVideo.objects.all()
    serializer_class = UploadVideoSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['lesson']
    search_fields = ['lesson']
    ordering_fields = ['lesson']


class CommentsViewSet(viewsets.ModelViewSet):
    ''' bu ViewSet orqali darslar uchun userlar izohlar qoldirsa boladi royhatdan o'tmaganlar faqat izohlarni kora oladi '''
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['author','lesson']
    search_fields = ['^lesson__title','author__username']
    ordering_fields = ['created','lesson']



class NotificationViewSet(viewsets.ModelViewSet):
    ''' bu ViewSet orqali  userlarga bildirishnomalarni email manzillariga yuborsa bo'ladi'''
    queryset = Notifications.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        notification = serializer.save()

        subject = notification.title
        message = notification.message

        users = User.objects.all()
        recipient_list = [user.email for user in users if user.email]

        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)



class LikeViewSet(viewsets.ViewSet):
    ''' bu ViewSet orqali foydalanuvchilar darslar uchun baho bersa bo'ladi'''
    permission_classes = [IsAuthenticatedOrReadOnly]
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