"""
URL configuration for student_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views, Hod_views, Staff_views, Student_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.Base, name='base'),

    # login path:

    path('', views.Login, name='login'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='Logout'),

    # reset password:
    path('reset_password/', views.reset_password, name='reset_password'),

    # profile update path:
    path('Profile', views.Profile, name='profile'),
    path('Profile/update', views.ProfileUpdate, name='profile_update'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', views.custom_password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    #####################################################
    # This is admin panel urls:
    # path of Dashboard (Home):
    path('hod/home', Hod_views.Home, name='hod_home'),

    # path of Students:
    path('hod/Students/Add', Hod_views.Add_Students, name='add_students'),
    path('hod/Students/View', Hod_views.view_students, name='view_students'),
    path('hod/Students/Edit/<str:id>', Hod_views.Edit_Students, name='edit_students'),
    path('hod/Students/Update', Hod_views.Update_Students, name='update_students'),
    path('hod/Students/Delete/<str:admin>', Hod_views.Delete_Students, name='delete_students'),

    # path of Staffs:
    path('hod/Staffs/Add', Hod_views.Add_Staffs, name='add_staffs'),
    path('hod/Staffs/View', Hod_views.View_Staffs, name='view_staffs'),
    path('hod/Staffs/Edit/<str:id>', Hod_views.Edit_Staffs, name='edit_staffs'),
    path('hod/Staffs/Update/', Hod_views.Update_Staffs, name='update_staffs'),
    path('hod/Staffs/Delete/<str:admin>', Hod_views.Delete_Staffs, name='delete_staffs'),

    # path of Courses:
    path('hod/Courses/Add', Hod_views.Add_Courses, name="add_courses"),
    path('hod/Courses/View', Hod_views.View_Courses, name="view_courses"),
    path('hod/Courses/Edit/<str:id>', Hod_views.Edit_Courses, name="edit_courses"),
    path('hod/Courses/Update', Hod_views.Update_Courses, name="update_courses"),
    path('hod/Courses/Delete/<str:id>', Hod_views.Delete_Courses, name="delete_courses"),


    # path of Subjects:
    path('hod/Subjects/Add', Hod_views.Add_Subjects, name="add_subjects"),
    path('hod/Subjects/View', Hod_views.View_Subjects, name="view_subjects"),
    path('hod/Subjects/Edit/<str:id>', Hod_views.Edit_Subjects, name="edit_subjects"),
    path('hod/Subjects/Update/', Hod_views.Update_Subjects, name="update_subjects"),
    path('hod/Subjects/Delete/<str:id>', Hod_views.Delete_Subjects, name="delete_subjects"),

    # path of Session:
    path('hod/Session/Add', Hod_views.Add_Sessions, name='add_sessions'),
    path('hod/Session/View', Hod_views.View_Sessions, name='view_sessions'),
    path('hod/Session/Edit/<str:id>', Hod_views.Edit_Sessions, name='edit_sessions'),
    path('hod/Session/Update', Hod_views.Update_Sessions, name='update_sessions'),
    path('hod/Session/Delete/<str:id>', Hod_views.Delete_Sessions, name='delete_sessions'),

    # path of Attendance:
    path('hod/Attendance/View', Hod_views.view_attendance, name='view_attendances'),

    # path of contact:
    path('hod/Contact/View', Hod_views.View_Contacts, name='view_contacts'),
    path('hod/Contact/Delete/<str:id>', Hod_views.Delete_Contacts, name='delete_contacts'),


    #####################################################
    # This is staff panel urls:
    path('staff/home', Staff_views.Staff_Home, name='staff_home'),

    # path for take attendance:
    path('staff/course_view', Staff_views.feature_view_course, name='feature_view_courses'),
    path('staff/student_view', Staff_views.feature_view_students, name='feature_view_students'),
    path('staff/staff_view', Staff_views.feature_view_staffs, name='feature_view_staffs'),
    path('staff/subject_view', Staff_views.feature_view_subjects, name='feature_view_subjects'),
    path('staff/session_view', Staff_views.feature_view_sessions, name='feature_view_sessions'),

    path('staff/take_attendance', Staff_views.Take_Attendance, name='take_attendances'),
    path('staff/save_attendance', Staff_views.Save_Attendance, name='save_attendances'),
    path('staff/view_attendance', Staff_views.View_Staff_Attendance, name='view_staff_attendances'),

    #####################################################
    # This is student panel urls:
    path('student/home', Student_views.Student_Home, name='student_home'),

    path('student/view_attendance', Student_views.Student_View_Attedance, name='student_view_attendance'),
    path('student/view_students', Student_views.View_Students, name='student_view_students'),
    path('student/view_courses', Student_views.View_Courses, name='student_view_courses'),
    path('student/view_staffs', Student_views.View_Staffs, name='student_view_staffs'),
    path('student/view_subjects', Student_views.View_Subjects, name='student_view_subjects'),
    path('student/view_sessions', Student_views.View_Sessions, name='student_view_sessions'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)