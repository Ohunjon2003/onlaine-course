from django.contrib import admin
from .models import Direction, Courses, Teacher, Lesson, UploadVideo, Comments, Notifications

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name',)
    search_fields = ('name',)

@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('name', 'direction', 'duration', 'beginning', 'ending', 'author')
    list_display_links = ('name',)
    list_filter = ('direction', 'beginning', 'ending')
    search_fields = ('name', 'description')
    autocomplete_fields = ('direction', 'author')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'address', 'experience')
    list_display_links = ('full_name',)
    search_fields = ('full_name', 'phone')
    autocomplete_fields = ('user',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'teacher', 'created', 'update')
    list_display_links = ('title',)
    list_filter = ('course', 'teacher', 'created', 'update')
    search_fields = ('title', 'description')
    autocomplete_fields = ('course', 'teacher')

@admin.register(UploadVideo)
class UploadVideoAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'video')
    list_display_links = ('lesson',)
    search_fields = ('lesson__title',)
    autocomplete_fields = ('lesson',)

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('author', 'lesson', 'rating', 'created')
    list_display_links = ('author',)
    list_filter = ('rating', 'created')
    search_fields = ('author__username', 'lesson__title', 'text')
    autocomplete_fields = ('author', 'lesson')

@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('email', 'message', 'dispatch', 'created')
    list_display_links = ('email',)
    list_filter = ('dispatch', 'created')
    search_fields = ('email__username', 'message')
    autocomplete_fields = ('email',)


