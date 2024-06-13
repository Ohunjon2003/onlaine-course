from django.contrib import admin
from .models import Direction, Courses, Teacher, Lesson, UploadVideo, Comments, Notifications,Like
from django.utils.safestring import mark_safe
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
    list_display = ('full_name', 'phone', 'address', 'experience','get_photo')
    list_display_links = ('full_name',)
    search_fields = ('full_name', 'phone')
    autocomplete_fields = ('user',)
    def get_photo(self,teacher):
        if teacher.photo:
            return mark_safe(f'<img src="{teacher.photo.url}" width="70px;">')
    get_photo.short_description = 'Rasmi'


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
    list_display = ('author', 'lesson', 'created')
    list_display_links = ('author',)
    list_filter = ('created',)
    search_fields = ('author__username', 'lesson__title', 'text')
    autocomplete_fields = ('author', 'lesson')

@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('title','message', 'created')
    list_display_links = ('title',)
    list_filter = ('created',)
    search_fields = ('title','message',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('lesson','user','like_or_dislike')
    list_display_links = ('lesson',)
    list_filter = ('lesson',)
    search_fields = ('lesson','user')

