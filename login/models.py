from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
import random


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )



class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_code = models.PositiveIntegerField(validators=[MinValueValidator(100000), MaxValueValidator(999999)])
    created_at = models.DateTimeField(default=now)
    is_used = models.BooleanField(default=False)

    @staticmethod
    def generate_otp():
        return random.randint(100000, 999999)

    class Meta:
        ordering = ['-created_at']

