from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# For Token Authentication
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



# Create your models here.
class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users should have an email")
        if not username:
            raise ValueError("Users should have valid username")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            # normalize means it will convert all the characters in email to lowercase

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self ,email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            # normalize means it will convert all the characters in email to lowercase
            username=username,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user

class Account(AbstractBaseUser):
    email                       = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username                    = models.CharField(max_length=30, unique=True)
    date_joined                 = models.DateTimeField(verbose_name="date_joined",auto_now_add=True)
    last_login                  = models.DateTimeField(verbose_name='last_login',auto_now=True)
    is_admin                    = models.BooleanField(default=False)
    is_active                   = models.BooleanField(default=True)
    is_staff                    = models.BooleanField(default=False)
    is_superuser                = models.BooleanField(default=False)
    first_name                  = models.CharField(max_length=30)


    USERNAME_FIELD = 'email'  #at the time of login what you want the user to write (username or email?)
    REQUIRED_FIELDS = ['username',]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


#Token Authentication
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)