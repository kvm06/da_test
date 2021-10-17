from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from .watermark import Watermark
from PIL import Image
from datingapp.settings import BASE_DIR
GENDER = [
        ('man', 'Мужской'),
        ('woman', 'Женский'),
    ]

class CustomUserManager(BaseUserManager):
    
    def create_user(self, first_name, last_name, gender, email, password=None):
        """Создает нового пользователя приложения с сохранением данных об email, имени, фамилии и поле"""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            gender=gender,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, gender, email, password=None):   
        """Создает суперпользователя приложения с сохранением данных об email, имени, фамилии и поле"""
        user = self.create_user(
            first_name,
            last_name,
            gender,
            email,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):

    first_name = models.CharField(verbose_name="Имя", max_length=50)
    last_name = models.CharField(verbose_name="Фамилия",  max_length=50)
    user_picture = models.ImageField(verbose_name = "Загрузить фото", upload_to='user_pictures',  null=True, blank=True)
    gender = models.CharField (verbose_name="Пол", max_length=8, choices=GENDER) 
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender']
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def save(self, *args, **kwargs):
        """Переопределяет метод save() для добавления водяного знака к изображению"""
        if self.user_picture:
            uploaded_img = Image.open(self.user_picture)
            watermark_path = 'users/static/users/images/watermark.png'
            watermark_open = Image.open(watermark_path, 'r')

            uploaded_img = Watermark.add_watermark(uploaded_img, watermark_open)
            uploaded_img.save('C:/Users/koloe/Desktop/datingapp/datingapp/media/user_pictures/' + self.user_picture.name.split('/')[-1])

        super(CustomUser,self).save()

class Matches(models.Model):

    first_user = models.ForeignKey(CustomUser, on_delete=CASCADE, related_name='first_user')
    second_user = models.ForeignKey(CustomUser, on_delete=CASCADE, related_name='second_user')
