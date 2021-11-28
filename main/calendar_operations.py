from datetime import datetime
from datetime import timedelta
import random
from django.utils.timezone import make_aware
import pytz

from django.conf import settings
from firebase_admin import db
firebase_admin = settings.MYDB

def add_task(datetime_object,weight,batch_code):
    calendar_start_date = db.reference("/{batch_code}/calendar_start_date/".format(batch_code = batch_code)).get()
    calendar_start_date_datetime_object = datetime(year= calendar_start_date['year'], month = calendar_start_date['month'],day= calendar_start_date['day'])
    calendar_start_date_datetime_object = make_aware(calendar_start_date_datetime_object, timezone= pytz.timezone('Asia/Kolkata'))
    index = (datetime_object - calendar_start_date_datetime_object).days
    reference_curr_date = db.reference("/{batch_code}/calendar_arr/{curr_index}".format(batch_code = batch_code,curr_index = str(index) ) )
    reference_curr_date_val = reference_curr_date.get()
    reference_curr_date.set(reference_curr_date_val + weight)
    return reference_curr_date.get()

def get_sum_weight_in_range(batch_code,start_interval,end_interval,previous_days,next_days):#range here is inclusive,start_interval,end_interval here are naive
    CALENDAR = db.reference('/{batch_code}/calendar_arr/'.format(batch_code= batch_code)).get()
    calendar_start_date_dict  = db.reference('/{batch_code}/calendar_start_date/'.format(batch_code= batch_code)).get()
    print(calendar_start_date_dict)
    CALENDAR_START_DATE = datetime(year= calendar_start_date_dict['year'],month= calendar_start_date_dict['month'],day = calendar_start_date_dict['day'])
    #not making it aware here as we input a naive datetime object only
    curr_time_delta1 = timedelta(days= previous_days)
    curr_time_delta2 = timedelta(days= next_days)
    start_date = start_interval - curr_time_delta1
    end_date = end_interval + curr_time_delta2
    duration_inclusive = (end_date - start_date) + timedelta(days= 1)
    time_delta_add = (start_date - CALENDAR_START_DATE)
    index_add = time_delta_add.days
    weight_arr = CALENDAR[index_add:index_add+duration_inclusive.days]
    maxi = 0
    #print(weight_arr)
    #print(weight_arr)
    for i in range(1,len(weight_arr)):
        weight_arr[i] += weight_arr[i-1]
    #print(weight_arr)
    weight_dict = {}
    start_interval_index_weight_arr = (start_interval- start_date).days
    end_interval_index_weight_arr = (end_interval-start_date).days
    #print(start_interval_index_weight_arr)
    for i in range(start_interval_index_weight_arr,end_interval_index_weight_arr+1):
        current_date = CALENDAR_START_DATE + time_delta_add + timedelta(days= i)
        if i-previous_days -1 >= 0:
            curr_val = weight_arr[i+next_days] - weight_arr[i-previous_days -1]
        else:
            curr_val = weight_arr[i+next_days]
        #print(current_date,curr_val)
        curr_date_string = "{year}#{month}#{day}".format(year = str(current_date.year),month = str(current_date.month),day = str(current_date.day) )
        #weight_dict[(current_date.year,current_date.month,current_date.day)] = curr_val
        maxi = max(maxi,curr_val)
        weight_dict[curr_date_string] = curr_val
    #print(weight_dict)
    return weight_dict, maxi
def get_weight_on_particular_date(datetime_object,batch_code):
    calendar_start_date = db.reference("/{batch_code}/calendar_start_date/".format(batch_code = batch_code)).get()
    calendar_start_date_datetime_object = datetime(year= calendar_start_date['year'], month = calendar_start_date['month'],day= calendar_start_date['day'])
    calendar_start_date_datetime_object = make_aware(calendar_start_date_datetime_object, timezone= pytz.timezone('Asia/Kolkata'))
    index = (datetime_object - calendar_start_date_datetime_object).days
    reference_curr_date = db.reference("/{batch_code}/calendar_arr/{curr_index}".format(batch_code = batch_code,curr_index = str(index) ) )
    return reference_curr_date.get()