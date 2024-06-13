from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (DirectionViewSet,CoursesViewSet,CommentsViewSet,TeacherViewSet,
                    UploadVideoViewSet,LessonViewSet,NotificationViewSet,LikeViewSet)

router = DefaultRouter()
router.register(r'direction', DirectionViewSet)
router.register(r'courses', CoursesViewSet)
router.register(r'comments', CommentsViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'lesson', LessonViewSet)
router.register(r'video', UploadVideoViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'likes', LikeViewSet,basename='likes')

urlpatterns = [
    path('', include(router.urls)),
]
