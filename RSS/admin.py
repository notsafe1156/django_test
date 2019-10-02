from django.contrib import admin

# Register your models here.
from django.contrib import admin
from RSS.models import Data
from RSS.models import Source


class Data_Modeladmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'source', 'category', 'tag', 'display']


admin.site.register(Data, Data_Modeladmin)
admin.site.register(Source)
