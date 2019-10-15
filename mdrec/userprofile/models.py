from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-c_time']
