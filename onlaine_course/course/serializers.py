from rest_framework import serializers
from .models import Direction,Courses,Teacher,Comments,Lesson, Notifications,UploadVideo


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'

class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class UploadVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadVideo
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'



class LikeSerializer(serializers.Serializer):
    lesson = serializers.IntegerField()
    like = serializers.BooleanField()
    dislike = serializers.BooleanField()