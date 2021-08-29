from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager
from django.conf import settings



class CustomUser(AbstractBaseUser):
    CHOICES = (('Male', 'Male'),
               ('Female', 'Female'))
    email = models.EmailField(verbose_name='email address', unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(choices=CHOICES, max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    image = models.ImageField( default='images/image1.jpg', upload_to='images/', blank=True, null=True,)#we have to use default before upload_to. If we don't the default images does not exist in the page.
    # last_login = models.DateTimeField(default=timezone.now())
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'first_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)

        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name



    def has_perm(self, perm, obj=None):#checks whether the user has a specific permission, for example:
        return self.is_staff#If the user is inactive, this method will always return False. For an active superuser, this method will always return True.



    def has_module_perms(self, app_label):#checks whether the user has any permissions for that app, for example:
        return self.is_staff



class AboutUrl(models.Model):
    UrlChoices = (
        ('Important', 'Important'),
        ('Almost Important', 'Almost Important'),
        ('Not Important', 'Not Important')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original_url = models.URLField(max_length=700, default='exapmle.com')
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_published = models.DateTimeField(auto_now=True)
    choices = models.CharField(verbose_name="", max_length=200, choices=UrlChoices)
    class Meta:
        ordering = ['-title']

    def __str__(self):
        return '%s %s' % (self.original_url, self.title)


