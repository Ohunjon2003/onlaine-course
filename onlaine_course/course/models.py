from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, ValidationError
from django.db import models

class Direction(models.Model):
    '''bu model yo'nalishlar nomi va qisqacha malumotlar yozish uchun'''
    name = models.CharField(max_length=100, verbose_name="Yonalish nomi")
    description = models.TextField(verbose_name="Yonalishlar haqida malumot")

    def __str__(self):
        return self.name

class Courses(models.Model):
    '''bu model kurslarni va ular haqidagi malumotlar yozish uchun'''
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
    '''bu model darslarni o'tadigan ustozlar haqida malumotlarni kiritish uchun'''
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='teacher_profile')
    full_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='teachers/', verbose_name="Rasimi")
    phone = models.CharField(max_length=13, verbose_name="Telfon raqami")
    address = models.CharField(max_length=100, verbose_name="Yashash joyi")
    experience = models.CharField(max_length=50, verbose_name="ish tajribasi")

    def __str__(self):
        return self.full_name

class Lesson(models.Model):
    '''bu model darslarni kiritish uchun'''
    course = models.ForeignKey(Courses, on_delete=models.SET_NULL, null=True, related_name='lessons')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='lessons')
    title = models.CharField(max_length=100, verbose_name="Dars mavzusi")
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, verbose_name="dars yuklangan vaqti")
    update = models.DateTimeField(auto_now=True, verbose_name="Darsga o'zgartirish kiritilgan vaqti")
    independent_work = models.FileField(upload_to='lesson/independent_work/',null=True,blank=True, verbose_name="mustaqil ishlar uchun")

    def __str__(self):
        return self.title

class UploadVideo(models.Model):
    '''bu model darslar uchun qo'yiladigan vidyolarni kiritish uchun '''
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, related_name='videos')
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    video = models.FileField(upload_to='lesson/videos/', validators=[
        FileExtensionValidator(allowed_extensions=['mp4', 'wmv'])
    ])
    def clean(self):
        self.file_size_validator()

    def file_size_validator(self):
        '''bu funksiya yuklanayotgan vidyo hajmini belgilash uchun'''
        limit = 300 * 1024 * 1024
        if self.video.size > limit:
            raise ValidationError("Yuklanayotgan vidyo hajmi 300 mb dan kam bo'lishi kerak")

    def __str__(self):
        return f"{self.lesson.title} uchun vidyo"



class Like(models.Model):
    '''bu model o'tilgan darslarga foydalanuvchilar baho berib ketishi uchun'''
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    like_or_dislike = models.BooleanField()

    def __str__(self):
        return f"{self.user} ni {self.lesson} ga bergan bahosi"



class Comments(models.Model):
    '''bu model darslarga  foydalanuvchilar yozgan izohlarni kiritib ketishi uchun'''
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="kim yozgani", related_name='comments')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="qaysi dars uchun", related_name='comments')
    text = models.TextField(verbose_name="Matn")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Kiritilgan vaqti")

    def __str__(self):
        return f"{self.author} ni {self.lesson}ga yozgan commenti"

class Notifications(models.Model):
    '''bu model foydalanuvchilarga yuborilgan bildirishnomalarni yozib ketish uchun'''
    title = models.CharField(max_length=200,null=True,blank=True)
    message = models.TextField(verbose_name="Xabar")
    created = models.DateTimeField(auto_now_add=True,verbose_name='yuborilgan vaqt')
    def __str__(self):
        return self.title

