from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
class Record(models.Model):
    title = models.CharField(max_length=30)
    content = RichTextField()
    song_url = models.CharField(max_length=200)
    # bg_img = models.ImageField(upload_to='record/%Y%m%d/', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    c_time = models.DateField()

    def __str__(self):
        return self.title
