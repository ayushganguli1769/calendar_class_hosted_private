"""calendar_class URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
app_name = 'main'
urlpatterns = [
    path('logout/', LogoutView.as_view(), name="logout"),
    path('test/',views.test,name='test'),
    path('test2/',views.test2,name='test2'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('faculty_home/',views.faculty_home,name='faculty_home'),
    path('join_create/',views.join_create,name='join_create'),
    path('create_batch/<str:batch_name>/', views.create_batch,name='create_batch'),
    path('join_batch/<str:batch_code>/',views.join_batch,name='join_batch'),
    path('create_class/<str:batch_code>/<str:class_name>/',views.create_class,name='create_classs'),
    path('join_class_teacher/<str:class_code>/',views.join_class_teacher,name='join_class_teacher'),
    path('view_schedule/',views.view_schedule,name='view_schedule' ),
    path('add_tasks_event/<str:batch_code>/<int:year>/<int:month>/<int:day>/<int:weight>/',views.add_task_view,name='add_task_view'),
    path('show_calendar_plan/',views.show_calendar_plan,name='show_calendar_plan'),
    path('add_task_page/',views.add_task_page, name='add_task_page'),
    path('batch_class_list/<str:batch_code>/',views.all_batch_classes,name='batch_class_list'),
    path('add_task_form_handler/', views.add_task_form_handler,name='add_task_form_handler'),
    path('get_all_tasks_on_day/',views.get_all_tasks_on_day,name='get_all_tasks_on_day'),
    path('delete_task/<int:task_id>/', views.delete_task,name="delete_task"),
    path('join_class_batch_student/',views.join_class_batch_student,name='join_class_batch_student'),
    path('join_class_student/<str:class_code>/', views.join_class_student,name='join_class_student'),
    path('student_submit_task/<int:task_id>/',views.student_task_submission_page,name='student_task_submission'),
    path('all_user_batches/', views.all_user_batches,name='all_user_batches'),
    path('all_submissions_for_task/<int:task_id>/<int:show_all>/',views.all_submissions_for_task,name='all_submissions_for_task'),
    path('all_classes_teacher/',views.all_classes_teacher, name='all_classes_teacher'),
    path('batch_view/<int:batch_id>/',views.batch_view, name='batch_view'),
    path('all_class_tasks/<int:class_id>/',views.all_class_tasks,name='all_class_tasks'),
    path('all_batch_classes_table_page/<int:batch_id>/', views.all_batch_classes_table_page, name='all_batch_classes_table_page'),
    path('user_profile_page/<int:user_id>/', views.user_profile_page , name='user_profile_page'),
    path('view_student_submission/<int:submission_id>', views.view_student_submission,name='view_student_submission'),
    path('student_home/', views.student_home, name='student_home'),
    path('grade_view_submitted_task/<int:submission_id>/' , views.grade_view_submitted_task, name='grade_view_submitted_task'),
    path('anonymous_classes/', views.all_anonymous_classes,name='anonymous_classes'),

]