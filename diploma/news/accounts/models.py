from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE, verbose_name='Пользователь')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    avatar = models.ImageField(null=True, blank=True, default='user_pics/anonymous_user.png', upload_to='user_pics', verbose_name='Аватар')

    def __str__(self):
        return self.get_user_full_name() + "'s Profile"
        
    class Meta:
        verbose_name = 'Профиль' 
        verbose_name_plural = 'Профили'
