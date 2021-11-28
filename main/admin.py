from django.contrib import admin

from main.views import register
from .models import *
admin.site.register(ExtendedUser)
admin.site.register(Batch)
admin.site.register(BatchClass)
admin.site.register(FileStored)
admin.site.register(Task)
admin.site.register(StudentSubmission)
# Register your models here.
