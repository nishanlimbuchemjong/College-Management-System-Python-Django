from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class UserModel(UserAdmin):
    list_display = ['username', 'user_type', 'profile_pic']


admin.site.register(CustomUser, UserModel)
admin.site.register(Course)
admin.site.register(Session_Year)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Staff)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(Contact)


