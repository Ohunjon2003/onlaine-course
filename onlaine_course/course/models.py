from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, ValidationError, MinValueValidator, MaxValueValidator
from django.db import models

class Direction(models.Model):
    name = models.CharField(max_length=100, verbose_name="Yonalish nomi")
    description = models.TextField(verbose_name="Yonalishlar haqida malumot")

    def __str__(self):
        return self.name

class Courses(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=100, verbose_name="kurs nomi")
    duration = models.CharField(max_length=50, verbose_name="Davomiyligi")
    description = models.TextField(verbose_name="curs haqida malumot")
    beginning = models.DateField(verbose_name="Boshlash vaqti")
    ending = models.DateField(verbose_name="tugatilgan vaqt",null=True,blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="kim tomonidan qo'shilgani")

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='teacher_profile')
    full_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='teachers/', verbose_name="Rasimi")
    phone = models.CharField(max_length=13, verbose_name="Telfon raqami")
    address = models.CharField(max_length=100, verbose_name="Yashash joyi")
    experience = models.CharField(max_length=50, verbose_name="ish tajribasi")

    def __str__(self):
        return self.full_name

class Lesson(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.SET_NULL, null=True, related_name='lessons')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='lessons')
    title = models.CharField(max_length=100, verbose_name="Dars mavzusi")
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, verbose_name="dars yuklangan vaqti")
    update = models.DateTimeField(auto_now=True, verbose_name="Darsga o'zgartirish kiritilgan vaqti")
    independent_work = models.FileField(upload_to='lesson/independent_work/', validators=[
        FileExtensionValidator(allowed_extensions=['rar', 'zip','png'])
    ],null=True,blank=True, verbose_name="mustaqil ishlar uchun")

    def __str__(self):
        return self.title

class UploadVideo(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, related_name='videos')
    video = models.FileField(upload_to='lesson/videos/', validators=[
        FileExtensionValidator(allowed_extensions=['mp4', 'wmv'])
    ])

    def clean(self):
        self.file_size_validator()

    def file_size_validator(self):
        limit = 300 * 1024 * 1024
        if self.video.size > limit:
            raise ValidationError("Yuklanayotgan vidyo hajmi 300 mb dan kam bo'lishi kerak")

    def __str__(self):
        return f"{self.lesson.title} uchun vidyo"

class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="kim yozgani", related_name='comments')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="qaysi dars uchun", related_name='comments')
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="Darsni baholash")
    text = models.TextField(verbose_name="Matn")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")

    def __str__(self):
        return f'Comment by {self.author} on {self.lesson}'

class Notifications(models.Model):
    email = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="habar jonatiladigan email",related_name="notifications")
    message = models.TextField(verbose_name="Xabar")
    dispatch = models.BooleanField(default=False,verbose_name="Yuborish")
    created = models.DateTimeField(auto_now_add=True,verbose_name='yuborilgan vaqt')

    def __str__(self):
        return f"Notification to {self.email.email}"