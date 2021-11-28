from json.encoder import JSONEncoder
from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import ExtendedUser, StudentSubmission
from datetime import datetime, timezone,date
import pytz
from pytz import timezone
from .models import Batch, BatchClass, Task, FileStored
import random
import json
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import make_aware
from .calendar_operations import add_task, get_sum_weight_in_range,get_weight_on_particular_date
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, views
from rest_framework import permissions
from rest_framework import authentication
from django.views.decorators.csrf import csrf_exempt
import sys
from django.utils.timezone import now as current_datetime_aware_object
from django.urls import reverse
from django.http import HttpResponseRedirect

CALENDAR_START_DATE = datetime(year = 1981, month = 1, day = 1,hour=1,minute= 1)
CALENDAR_END_DATE = datetime(year = 2102, month =3, day = 5,hour=1,minute=1)

def set_datetime(parameter_list,time_zone):
    pass
def check_is_faculty(user):
    return (user.is_anonymous is False) and  ( user.extended_reverse.is_student is False)
def check_is_student(user):
    return (user.is_anonymous is False) and  ( user.extended_reverse.is_student is True)

def generate_random_string(length):
    arr = [chr(random.randrange(65,91) ) for _ in range(length)]
    return "".join(arr)
def register(request):
    if 'register' in request.POST:
        #try:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        date_of_birth = request.POST['date_of_birth']#month day year
        type_of_user = request.POST['type_of_user']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        print(request.FILES)
        profile_photo = request.FILES['profile_photo']
        #except Exception as e:
        #    return render(request,'register.html',{'error_message':"Please fill all form parameters"})
        try:
            (month,day,year) = map(int,date_of_birth.strip().split("/"))
        except Exception as e:
            print(e)
            return render(request,'register.html',{'error_message':"Invalid Date Format"})
        #print(username,password1,password2,date_of_birth,type_of_user)
        if password1 == password2:
            if User.objects.filter(username = username).exists():
                print("already Exists")
                return render(request,'register.html',{'error_message':"Username already taken"})
            else:
                user= User.objects.create_user(username = username, password = password1,email = email, first_name= first_name, last_name = last_name)
                user.save()
                naive_dob = datetime(year= year,month=month,day=day)#,timezone= pytz.timezone('Asia/Kolkata')
                aware_dob = make_aware(naive_dob, timezone= pytz.timezone('Asia/Kolkata'))
                user.extended_reverse.dob = aware_dob
                user.extended_reverse.image = profile_photo
                if type_of_user == "faculty":
                    user.extended_reverse.is_student = False
                user.extended_reverse.save()
                return redirect('/login/')
        else:
            return render(request,'register.html',{'error_message':"Password does not match"})
    return render(request,'register.html')

def login(request):
    if 'login' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user != None:
            auth.login(request,user)
            if user.extended_reverse.is_student:
                return redirect('/student_home/')
            else:
                return redirect('/faculty_home/')
        else:
            return render(request, 'login.html', {'error_message': "Invalid Credentials"})
    return render(request, 'login.html')

@user_passes_test(check_is_faculty,login_url='/login/')
def faculty_home(request):
    return render(request,'faculty_home.html')

@user_passes_test(check_is_student,login_url='/login/')
def student_home(request):
    return render(request,'student_home.html')

@user_passes_test(check_is_faculty,login_url='/login/')
def join_create(request):
    return render(request,'join_create.html')

@user_passes_test(check_is_student,login_url='/login/')
def join_class_batch_student(request):
    return render(request,'join_class_batch_student.html')

@user_passes_test(check_is_faculty,login_url='/login/')
@csrf_exempt
def create_batch(request,batch_name):#teacher only method. create a decorator for the same
    while True:
        batch_teacher_code = generate_random_string(10)#keep it 10 only. I have hardcoded a check for length 10 on frontend
        if Batch.objects.filter(batch_code_teacher = batch_teacher_code).exists() is False:
            break
    while True:
        batch_student_code = generate_random_string(10)
        if Batch.objects.filter(batch_code_student = batch_student_code).exists() is False:
            break
    if Batch.objects.filter(name = batch_name).exists() is True:
        return JsonResponse({
            'is_success': False,
            'message': "A batch with batch name already exists. Please try another name."
            },status = 200)
    new_batch = Batch(batch_code_student = batch_student_code, batch_code_teacher = batch_teacher_code, name= batch_name,owner = request.user)
    new_batch.save()
    new_batch.all_users_in_batch.add(request.user)
    new_batch.save()
    return JsonResponse({
        'is_success': True,
        'student_code': batch_student_code,
        'teacher_code':batch_teacher_code,
        'message': "success"
    },status = 200)

@login_required
@csrf_exempt
def join_batch(request,batch_code):
    if request.user.extended_reverse.is_student is True and Batch.objects.filter(batch_code_student = batch_code).exists() is True:
        curr_batch = Batch.objects.get(batch_code_student = batch_code)
    elif request.user.extended_reverse.is_student is False and Batch.objects.filter(batch_code_teacher = batch_code).exists() is True:
        curr_batch = Batch.objects.get(batch_code_teacher = batch_code)
    else:
        return JsonResponse({
        'is_success': False,
        'message': "No such batch exists"
    },status = 200)
    if request.user in curr_batch.all_users_in_batch.all():
        return JsonResponse({
            'is_success': False,
            'batch_name':curr_batch.name,
            'message': "You are already a part of {batch_name}".format(batch_name = curr_batch.name)
        })
    curr_batch.all_users_in_batch.add(request.user)
    curr_batch.save()
    return JsonResponse({
        'is_success': True,
        'batch_name':curr_batch.name,
        'message': "Successfully joined batch {batch_name}".format(batch_name = curr_batch.name)
    })

@user_passes_test(check_is_faculty,login_url='/login/')
@csrf_exempt
def create_class(request,batch_code,class_name):
    try:
        current_batch = Batch.objects.get(batch_code_teacher = batch_code)
    except:
        return JsonResponse({
        'is_success': False,
        'message': "Batch does not exist"
    }, status = 400)
    if request.user not  in current_batch.all_users_in_batch.all():
        return JsonResponse({
        'is_success': False,
        'message': "You are not a part of the batch"
        }, status = 400)
    elif BatchClass.objects.filter(belongs_to_batch = current_batch,name = class_name).exists() is True:
        return JsonResponse({
        'is_success': False,
        'message': "A class with same name already exists in the current batch. Please Try another name"
        }, status = 400)        
    while True:
        class_code = generate_random_string(10)
        if BatchClass.objects.filter(class_code= class_code).exists() is False:
            break
    while True:
        student_class_code = generate_random_string(10)
        if BatchClass.objects.filter(student_class_code= student_class_code).exists() is False:
            break
    curr_class = BatchClass(owner= request.user,belongs_to_batch= current_batch,name = class_name,class_code = class_code, student_class_code = student_class_code)
    curr_class.save()
    curr_class.teachers.add(request.user)
    curr_class.save()
    return JsonResponse({
        'batch_name':current_batch.name,
        'class_name':curr_class.name,
        'class_code': class_code,
        'student_class_code': student_class_code,
        'is_success':True,
        'message':'Class Created'
    })

@user_passes_test(check_is_faculty,login_url='/login/')
def join_class_teacher(request,class_code):
    try:
        curr_class = BatchClass.objects.get(class_code =class_code)
    except:
        return JsonResponse({
        'is_success': False,
        'message': "Invlaid class code"
        }, status = 200)
    if request.user in curr_class.teachers.all():
        return JsonResponse({
            'is_success': False,
            'message': "You are already part of class "
            }, status = 200)
    curr_batch = curr_class.belongs_to_batch
    if request.user not in curr_batch.all_users_in_batch.all():
        return JsonResponse({
            'is_success': False,
            'message': "You are not a part of the batch {batch_name}. Please join the batch , then join the class".format(batch_name= curr_batch.name)
            }, status = 200)
    curr_class.teachers.add(request.user)
    curr_class.save()
    return JsonResponse({
        'is_success': True,
        'message': "Sucessfully added to class {curr_class_name} belonging to batch {curr_batch_name}".format(curr_class_name = curr_class.name,curr_batch_name= curr_batch.name)
        }, status = 200)

@user_passes_test(check_is_student,login_url='/login/')
def join_class_student(request,class_code):
    try:
        curr_class = BatchClass.objects.get(student_class_code =class_code)
    except:
        return JsonResponse({
        'is_success': False,
        'message': "Invlaid class code"
        }, status = 400)
    if request.user in curr_class.belongs_to_batch.all_users_in_batch.all():
        return JsonResponse({
            'is_success': False,
            'message': "You are already part of the batch {batch_name} which contains the class {class_name}".format(batch_name = curr_class.belongs_to_batch.name, class_name = curr_class.name)
            }, status = 400)        
    elif request.user in curr_class.third_party_user.all():
        return JsonResponse({
            'is_success': False,
            'message': "You are already part of class "
            }, status = 400)
    curr_batch = curr_class.belongs_to_batch
    curr_class.third_party_user.add(request.user)
    curr_class.save()
    return JsonResponse({
        'is_success': True,
        'message': "Sucessfully added to class {curr_class_name} belonging to batch {curr_batch_name}".format(curr_class_name = curr_class.name,curr_batch_name= curr_batch.name)
        }, status = 200)

@api_view(['GET','POST'])
@csrf_exempt#made some changes with max val pls cross verify
def show_calendar_plan(request):#weights are in percentage while returning not absolute
    batch_code = request.data['batch_code']   
    start_interval_year = int(request.data['start_interval_year'])
    start_interval_month = int(request.data['start_interval_month'])
    start_interval_day = int(request.data['start_interval_day'])
    end_interval_year = int(request.data['end_interval_year'])
    end_interval_month = int(request.data['end_interval_month'])
    end_interval_day = int(request.data['end_interval_day'])
    previous_days = int(request.data['previous_days'])
    next_days = int(request.data['next_days'])
    start_interval = datetime(year=start_interval_year,month = start_interval_month,day = start_interval_day)
    end_interval = datetime(year=end_interval_year,month=end_interval_month,day= end_interval_day)
    weight_dict,max_val = get_sum_weight_in_range(batch_code,start_interval,end_interval,previous_days,next_days)
    mini = sys.maxsize
    mini_date_string = None
    #if max_val > 0:
    for curr_date_string in weight_dict:
        if max_val > 0:
            weight_dict[curr_date_string] = (weight_dict[curr_date_string]/max_val) * 100
        else:
            weight_dict[curr_date_string] = 0
        if weight_dict[curr_date_string] < mini:
            mini = weight_dict[curr_date_string]
            mini_date_string = curr_date_string
    try:
        optimal_day_arr = mini_date_string.split("#")
        optimal_date = date(year = int(optimal_day_arr[0]), month = int(optimal_day_arr[1]) , day = int(optimal_day_arr[2]) )
        optimal_date_string = optimal_date.strftime('%A %d %B %Y')
    except:
        optimal_date_string = ""
    start_date_string = "{year}#{month}#{day}".format(year = start_interval_year,month= start_interval_month,day = start_interval_day)
    data = {'message': 'ok','weight_dict': weight_dict,'start_date_string': start_date_string,'optimal_day': optimal_date_string,'maxi_val': max_val}
    return Response(data=data,status= status.HTTP_200_OK)
@login_required
@csrf_exempt
def all_batch_classes(request,batch_code):
    try:
        if request.user.extended_reverse.is_student:
            curr_batch = Batch.objects.get(batch_code_student = batch_code)
        else:
            curr_batch = Batch.objects.get(batch_code_teacher= batch_code)
    except:
        return JsonResponse({
            'is_success': False,
            'message': "Batch not found"
            }, status = 400)
    all_classes = BatchClass.objects.filter(belongs_to_batch= curr_batch)
    all_classes_list = []
    for curr_class in all_classes:
        if curr_class.owner is not None:
            curr_owner =curr_class.owner.username
        else:
            curr_owner = None
        curr_dict = {
                    'class_name': curr_class.name,
                    'owner_username': curr_owner,
                    'teacher_class_code':curr_class.class_code,
                    'student_class_code': curr_class.student_class_code
        }
        if request.user in curr_class.teachers.all():
            all_classes_list.append(curr_dict)
    return JsonResponse(
        {
            'is_success': True,
            'message':'success',
            'all_classes_list':all_classes_list
        }
    )
@user_passes_test(check_is_faculty,login_url='/login/')
def add_task_form_handler(request):
    #print('called')
    global CALENDAR_START_DATE, CALENDAR_END_DATE
    if request.method == "POST":
        batch_code = request.POST['batch_code_hidden']
        #print(batch_code,'batch code deb')
        class_code_teacher = request.POST['class_code_hidden']
        stress_level = int(request.POST['stress_level_task'] )
        curr_class = BatchClass.objects.get(class_code = class_code_teacher)
        name_title = request.POST['title']
        start_time_string = request.POST['start_task_time']
        content_html_description = request.POST['description_content_hidden']
        if len(start_time_string) > 0:
            try:
                start_datetime_object = datetime.strptime(start_time_string,'%Y/%m/%d %H:%M')
            except Exception as e:
                request.session['message'] = "Inavlid task submission date time format"
                return redirect('main:add_task_page')
        else:
            start_datetime_object = current_datetime_aware_object
        start_datetime_object = make_aware(start_datetime_object, timezone= pytz.timezone('Asia/Kolkata'))
        end_time_string = request.POST['end_task_time']
        if len(end_time_string) > 0:
            try:
                end_datetime_object = datetime.strptime(end_time_string,'%Y/%m/%d %H:%M')
            except:
                request.session['message'] = "Inavlid task submission date time format"
                return redirect('main:add_task_page')
        else:
            end_datetime_object = CALENDAR_END_DATE
        end_datetime_object = make_aware(end_datetime_object, timezone= pytz.timezone('Asia/Kolkata'))

        new_task = Task(belongs_to_class = curr_class,name = name_title,start_time= start_datetime_object,end_time= end_datetime_object,stress_level = stress_level,description = content_html_description)
        new_task.save()
        if request.FILES:
            files_object = request.FILES.items()
            for key_of_file_in_input,name_of_file in files_object:
                print(name_of_file, key_of_file_in_input)
                new_file_retrieved = request.FILES[key_of_file_in_input]
                new_file_obj = FileStored(name = name_of_file,stored_file = new_file_retrieved,linked_to = new_task)
                new_file_obj.save()
        val =add_task(end_datetime_object,stress_level,batch_code)#adding task to firebase calendar
        print(val)
        request.session['message'] = "Your Task has been added. You can add more here now too."
        return redirect('main:add_task_page')
    return redirect('add_task_page')

def add_task_page(request):
    if 'message' in request.session:
        message = request.session['message']
        del request.session['message']
    else:
        message = None
    return render(request,'add_task.html',{'error_message': message})

@api_view(['GET','POST'])
@csrf_exempt
def get_all_tasks_on_day(request):
    curr_user_id = int(request.data['user_id'])
    curr_user = User.objects.get(id= curr_user_id)
    #print(curr_user,'deb')
    #curr_user = User.objects.get(id=10) #fore debugging in postman
    batch_code = request.data['batch_code']
    year = int(request.data['year'])
    month = int(request.data['month'])
    day = int(request.data['day'])
    if curr_user.extended_reverse.is_student is True:
        curr_batch = Batch.objects.get(batch_code_student = batch_code)
    else:
        curr_batch = Batch.objects.get(batch_code_teacher = batch_code)
    all_classes_in_batch = curr_batch.all_batch_class.all()
    task_list = []
    #dict keys in it Task Name,Task Class Name, Task Class Faculty name, Deletable(true/false)
    for curr_class in all_classes_in_batch:
        all_tasks_in_class = curr_class.batch_class_tasks.all()
        for curr_task in all_tasks_in_class:
            curr_task_end_time = curr_task.end_time
            curr_task_end_time =curr_task_end_time.astimezone(timezone('Asia/Kolkata'))
            if curr_task_end_time.year == year and curr_task_end_time.month == month and curr_task_end_time.day == day:
                if curr_class.owner:
                    class_owner_name = curr_class.owner.username
                else:
                    class_owner_name = None
                curr_dict = {
                            'name': curr_task.name,
                            'class_name': curr_class.name,
                            'owner_faculty_name':class_owner_name ,
                            'deletable' : (curr_user in curr_class.teachers.all()),
                            'task_id': curr_task.id,
                        }
                task_list.append(curr_dict)
    curr_date_datetime_object = datetime(year=year,month=month, day=day)
    curr_date_datetime_object = make_aware(curr_date_datetime_object, timezone= pytz.timezone('Asia/Kolkata'))
    stress_level = get_weight_on_particular_date(curr_date_datetime_object,batch_code)
    json_data = {
        'message' : "success",
        'stress_level':stress_level,
        'task_list': task_list
    }
    print(json_data,'before return')
    return Response(data = json_data, status= status.HTTP_200_OK)

@user_passes_test(check_is_faculty,login_url='/login/')
@csrf_exempt
def delete_task(request,task_id):
    curr_task = Task.objects.get(id= task_id)
    curr_task_end_time = curr_task.end_time
    try:
        curr_task_batch = curr_task.belongs_to_class.belongs_to_batch
        curr_batch_code = curr_task_batch.batch_code_teacher
        add_task(curr_task_end_time,-curr_task.stress_level,curr_batch_code)
    except Exception as e:
        print("MOst probably task not part of any batch ")
        return JsonResponse(
            {
                'is_success': False,
                'message':"Task most probably not part of any batch. Exception {curr_exception}".format(curr_exception = str(e) ),
            }, status= 400
        )
    curr_task.delete()
    return JsonResponse(
        {
            'is_success': True,
            'message':'Task {name} deleted'.format(name = curr_task.name),
        }, status= 200
    )
#@user_passes_test(check_is_student,login_url='/login/')
@login_required
def student_task_submission_page(request,task_id):#3 for submiiting or viewing tasks added. 3authentication_handled
    curr_task = Task.objects.get(id= task_id)
    task_class = curr_task.belongs_to_class
    task_batch = task_class.belongs_to_batch
    if request.user.extended_reverse.is_student is True and current_datetime_aware_object() < curr_task.start_time:
        start_time_india = curr_task.end_time.astimezone(timezone('Asia/Kolkata'))
        curr_message = "Task starts at {time_start}. You are too early.".format(time_start = str(start_time_india))
        return render(request,'error_message.html',{'message': curr_message})
    if request.user.extended_reverse.is_student:
        if request.user not in task_class.third_party_user.all() and request.user not in task_batch.all_users_in_batch.all():
            curr_message = "You are not a part of the class or batch. Please join the class or batch to submit"
            return render(request,'error_message.html',{'message': curr_message})
    else:
        if request.user not in task_class.teachers.all() and request.user not in task_batch.all_users_in_batch.all():
            curr_message = "You are not a part of the class or batch. Please join the class or batch to submit"
            return render(request,'error_message.html',{'message': curr_message})           
    all_task_files = curr_task.tagged_file.all()
    if 'submit_task_button' in request.POST:
        new_student_submission = StudentSubmission(belongs_to_user = request.user,for_which_task = curr_task)
        new_student_submission.save()
        if request.FILES:
            files_object = request.FILES.items()
            for key_of_file_in_input,name_of_file in files_object:
                print(name_of_file, key_of_file_in_input)
                new_file_retrieved = request.FILES[key_of_file_in_input]
                new_file_obj = FileStored(name = name_of_file,stored_file = new_file_retrieved,linked_to = new_student_submission)
                new_file_obj.save()
                return render(request,'student_task_submission.html',{'curr_task': curr_task,
                'error_message':"Task Submitted.You can submit another. Your latest one will be considered.",
                'all_task_files':all_task_files
                })
    return render(request,'student_task_submission.html',{'curr_task': curr_task,'all_task_files':all_task_files})

@login_required
def all_user_batches(request):
    all_batches = request.user.all_batch_user_belongs.all()
    return render(request,'all_user_batches.html',{'all_batches': all_batches})

@login_required
def all_submissions_for_task(request,task_id,show_all):#4task viewing 4authentication_handled 
    curr_task = Task.objects.get(id= task_id)
    all_submissions_for_task = curr_task.task_submissions.all()
    view_all = True
    #print(all_submissions_for_task)
    if request.user.extended_reverse.is_student :
        filtered_submissions = all_submissions_for_task.filter(belongs_to_user = request.user)
    else:
        if request.user not in curr_task.belongs_to_class.teachers.all() and request.user not in curr_task.belongs_to_class.belongs_to_batch.all_users_in_batch.all():
            return render(request,'error_message.html',{'message': "You are not a part of {class_name} or batch of this class".format(class_name = curr_task.belongs_to_class.name)})
        filtered_submissions = all_submissions_for_task.order_by('-submission_time')
        if show_all <= 0:
            view_all = False
            curr_filtered_submissions = filtered_submissions
            filtered_submissions = []
            user_id_set = set()
            for curr in curr_filtered_submissions:
                if curr.belongs_to_user.id not in user_id_set:
                    user_id_set.add(curr.belongs_to_user.id)
                    filtered_submissions.append(curr)
    #print(filtered_submissions)
    return render(request,'all_task_submissions.html',{'filtered_submissions': filtered_submissions,'curr_task': curr_task,'view_all': view_all})

@login_required
def view_student_submission(request, submission_id):
    curr_submission = StudentSubmission.objects.get(id = submission_id)
    temp = "Student {uname} submission to task {task_name}".format(uname = curr_submission.belongs_to_user.username, task_name= curr_submission.for_which_task.name)
    return HttpResponse(temp)

@user_passes_test(check_is_faculty,login_url='/login/')
def all_classes_teacher(request):
    all_classes = request.user.classes_teaching.all()
    #print(all_classes)
    return render(request,'all_faculty_classes.html',{'all_faculty_classes':all_classes})
@login_required
def all_class_tasks(request,class_id):#2all tasks in class 2authentication_handled
    curr_class = BatchClass.objects.get(id= class_id)
    if request.user.extended_reverse.is_student is True:
        if (request.user not in curr_class.third_party_user.all()) and (request.user not in curr_class.belongs_to_batch.all_users_in_batch.all() ):
            curr_message = "You are not a part of this class. Either join the batch which this class belongs to or join the class without being a part of the batch"
            return render(request,'error_message.html', {'message': curr_message})
    else:
        if request.user not in curr_class.teachers.all() and request.user not in curr_class.belongs_to_batch.all_users_in_batch.all():
            curr_message = "You are not a teacher for this class. Please join the batch which this class belongs to and then join the class"
            return render(request,'error_message.html', {'message': curr_message}) 

    all_tasks = curr_class.batch_class_tasks.all()
    batch_class_all_users = curr_class.belongs_to_batch.all_users_in_batch.all()
    batch_class_all_students = batch_class_all_users.filter(extended_reverse__is_student = True)
    all_third_party_class_students = curr_class.third_party_user.filter(extended_reverse__is_student = True)
    all_students = batch_class_all_students.union(all_third_party_class_students)
    all_faculties = curr_class.teachers.all()
    return render(request,'all_class_tasks.html',
                    {'all_students': all_students,
                    'all_faculties': all_faculties,
                    'all_tasks': all_tasks,
                    'curr_class': curr_class}
                )
@login_required
def all_batch_classes_table_page(request,batch_id):#viewing all classes in a batch #1authentication_handled
    curr_batch = Batch.objects.get(id = batch_id)
    if request.user not in curr_batch.all_users_in_batch.all():
        return render(request, 'error_message.html', {'message':"You are not a part of the batch. Please contact owner for Batch code and join the batch"})
    classes_in_curr_batch = curr_batch.all_batch_class.all()
    all_students = curr_batch.all_users_in_batch.filter(extended_reverse__is_student = True)
    all_faculties = curr_batch.all_users_in_batch.filter(extended_reverse__is_student = False)
    return render(request,'all_batch_classes.html',{'curr_batch': curr_batch,'all_students': all_students,'all_faculties': all_faculties,'all_classes': classes_in_curr_batch})

@user_passes_test(check_is_student,login_url='/login/')
def all_anonymous_classes(request):#viewing all classes in a batch #1authentication_handled
    curr_batch = {'name':"Anonymous Classes"}
    all_anonymous_classes_queryset = request.user.anonymous_classes.all()
    return render(request,'all_batch_classes.html',{'curr_batch': curr_batch,'all_classes': all_anonymous_classes_queryset})

@login_required
def grade_view_submitted_task(request,submission_id):
    view_only = True
    message = None
    curr_submission = StudentSubmission.objects.get(id= submission_id)
    #print(curr_submission.belongs_to_user.username,'debug')
    #print(request.user.username,'debug')
    submission_class = curr_submission.for_which_task.belongs_to_class
    submission_batch = submission_class.belongs_to_batch
    if request.user.extended_reverse.is_student is True:
        if curr_submission.belongs_to_user != request.user:
            return render(request,'error_message.html',{'message':"You are not authorized to view this submission. Please do not try to view others submission and get involvved in unfair practices"})
    else:
        if request.user in submission_class.teachers.all():
            view_only = False
        elif request.user not in submission_batch.all_users_in_batch.all():
            return render(request,'error_message.html',{'message':"You are not authorized to view this submission. Please do not try to view others submission and get involvved in unfair practices"})
    late_submission = curr_submission.submission_time > curr_submission.for_which_task.end_time
    all_submission_files = curr_submission.tagged_submission.all()
    if 'grade_task_button' in request.POST:
        grade = request.POST['grade_form_input']
        remark = request.POST['remark_form_input']
        curr_submission.grade = grade
        curr_submission.remark = remark
        curr_submission.save()
        message = "You have graded the task. To change grade fill, the form fill the"
    return render(request,'grade_view_submitted_task.html',{
        'curr_submission':curr_submission,
        'late_submission': late_submission,
        'submission_time': curr_submission.for_which_task.end_time,
        'all_submission_files': all_submission_files,
        'view_only': view_only,
        'error_message': message
        })
@login_required
def user_profile_page(request,user_id):
    curr_user = User.objects.get(id = user_id)
    return render(request,'profile_page.html',{'curr_user': curr_user})

@login_required
def batch_view(request,batch_id):
    pass

def add_task_view(request,batch_code,year,month,day,weight):
    my_datetime_object = datetime(year=year,month=month,day = day)
    add_task(my_datetime_object,weight,batch_code)
    return JsonResponse({'message': 'ok'})

def main_home(request):
    return render(request,'main_home_page.html')

@user_passes_test(check_is_faculty,login_url='/login/')
def view_schedule(request):
    return render(request,'calendar.html')
def test(request):
    return render(request,'profile_page.html')
def test2(request):
    return render(request,'register.html')

# Create your views here.
