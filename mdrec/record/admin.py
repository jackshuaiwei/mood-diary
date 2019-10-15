from django.contrib import admin
from .models import Record

# Register your models here.
class RecordAdmin(admin.ModelAdmin):
    empty_value_display = '-nothing-'
    list_display = ('title','content','song_url')

admin.site.register(Record,RecordAdmin)