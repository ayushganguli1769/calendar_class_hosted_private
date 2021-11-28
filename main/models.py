from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime
import pytz
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now as current_datetime_aware_object
from django.core.validators import FileExtensionValidator

from django.conf import settings
from firebase_admin import db
firebase_admin = settings.MYDB
from datetime import datetime

CALENDAR_START_DATE = datetime(year = 1951, month = 1, day = 1)
CALENDAR_END_DATE = datetime(year = 2152, month =3, day = 5)#ends 1 day before end date

class ExtendedUser(models.Model):
    linked_user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='extended_reverse',)
    dob = models.DateField(null= True)#date of birth
    is_student = models.BooleanField(default=True)#true for student false for faculty
    image = models.FileField(null= True, validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','svg','webp'])])
    def __str__(self):
        return self.linked_user.username + " Extended User"

class Batch(models.Model):
    owner = models.ForeignKey(User,related_name='batch_owner_reverse',null=True, on_delete=models.PROTECT)
    all_users_in_batch = models.ManyToManyField(User,related_name='all_batch_user_belongs')
    batch_code_student = models.CharField(max_length=200)
    batch_code_teacher = models.CharField(max_length=200)
    name = models.CharField(max_length=500)
    def __str__(self):
        return self.name 

class BatchClass(models.Model):
    owner = models.ForeignKey(User,related_name='class_owner_reverse',null= True, on_delete=models.PROTECT)
    teachers = models.ManyToManyField(User,related_name='classes_teaching')
    belongs_to_batch = models.ForeignKey(Batch,related_name='all_batch_class',on_delete=models.PROTECT)
    third_party_user = models.ManyToManyField(User,related_name='anonymous_classes')#they are classes which are not in users batch but he is attending them
    class_code = models.CharField(max_length=200,null=True)#meant for teachers
    student_class_code = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name + " belongs to " + self.belongs_to_batch.name

class FileStored(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    linked_to = GenericForeignKey('content_type', 'object_id')#can be for student submission or task
    stored_file = models.FileField(null= True)
    name = models.CharField(max_length=200)
    date_of_creation = models.DateTimeField(auto_now_add= True)
    def __str__(self):
        return self.name

class Task(models.Model):
    belongs_to_class = models.ForeignKey(BatchClass,related_name='batch_class_tasks', on_delete = models.PROTECT)
    name = models.CharField(max_length=500)
    start_time = models.DateTimeField( default= current_datetime_aware_object)
    end_time = models.DateTimeField(null= True)
    stress_level = models.IntegerField(default=5)
    description = models.CharField(max_length=15500)
    tagged_file = GenericRelation(FileStored)
    def __str__(self):
        return  self.name + " belonging to class " + self.belongs_to_class.name 

class StudentSubmission(models.Model):
    belongs_to_user = models.ForeignKey(User, related_name='user_task_submission', on_delete=models.CASCADE)
    for_which_task = models.ForeignKey(Task,related_name='task_submissions', on_delete=models.PROTECT)
    time_of_submission = models.DateTimeField(auto_now_add=True)
    tagged_submission = GenericRelation(FileStored)
    submission_time = models.DateTimeField(auto_now_add= True)
    grade = models.CharField(max_length = 100, null= True)#null if not graded
    remark = models.CharField(max_length = 1000, null= True)#null if no remark
    def __str__(self):
        return self.belongs_to_user.username + " submission at " + str(self.time_of_submission)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):#when User object created ExtendedUser also created
    if created:
        my_extended_user = ExtendedUser(linked_user = instance)
        my_extended_user.save()
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):#when user object saved ExtendedUser also saved
    instance.extended_reverse.save()
@receiver(post_save, sender=Batch)
def create_batch(sender, instance, created, **kwargs):
    if created:
        #creating batch calendar 1D array instance
        ref = db.reference(instance.batch_code_teacher)
        length_of_calendar = (CALENDAR_END_DATE - CALENDAR_START_DATE).days
        calendar_arr = [0]*length_of_calendar
        start_date_curr_calendar = {'year':CALENDAR_START_DATE.year,'month': CALENDAR_START_DATE.month,'day':CALENDAR_START_DATE.month}
        end_date_curr_calendar = {'year':CALENDAR_END_DATE.year,'month':CALENDAR_END_DATE.month,'day':CALENDAR_END_DATE.day}
        ref.set({
            'calendar_start_date': start_date_curr_calendar, 
            'calendar_end_date': end_date_curr_calendar, 
            'calendar_arr': calendar_arr
            })
