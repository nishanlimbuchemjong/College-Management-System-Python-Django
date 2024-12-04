from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from django.shortcuts import render, redirect
from student_management_app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from student_management_app.models import CustomUser, Student, Staff, Contact


# base
def Base(request):
    student = Student.objects.all()
    staff = Staff.objects.all()
    user = CustomUser.objects.all()
    context = {
        'student': student,
        'staff': staff,
        'user': user,
    }
    return render(request, 'index.html', context)


# login
def Login(request):
    if request.method == "POST":
        # for contact us:
        if 'contact_form' in request.POST:
            contact = Contact()
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('message')

            # storing the request data into Contact model
            contact.name = name
            contact.email = email
            contact.subject = subject
            contact.save()

            # success messages
            messages.success(request, 'Your messages have been sent successfully.')
            return redirect('login')

        # for amin register:
        elif 'admin_form' in request.POST:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            admin_email = request.POST.get('admin_email')
            admin_password = request.POST.get('admin_password')
            admin_confirm_password = request.POST.get('admin_confirm_password')
            profile_pic = request.FILES.get('profile_pic')
            # checking for email validation:
            if not admin_email.endswith('@gmail.com'):
                messages.warning(request, 'Invalid email format.')
                return redirect('login')
            
            # checkingif password are same
            if admin_password!=admin_confirm_password:
                messages.error(request, 'Passwords doesnot match')
                return redirect('login')
            # checking for email:
            if CustomUser.objects.filter(email=admin_email).exists():
                messages.error(request, 'Email already exists.')
                return redirect('login')

            # checking for username:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('login')
            else:
                try:
                    user = CustomUser(
                        first_name=first_name,
                        last_name=last_name,
                        username=username,
                        email=admin_email,
                        profile_pic=profile_pic,
                        user_type=1,
                    )
                    user.set_password(admin_password)
                    user.save()

                    # success messages
                    messages.success(request, 'Registered successfully as an Admin.')
                    return redirect('login')
                except:
                    # error messages
                    messages.error(request, 'Failed to registered as an Admin.')
                    return redirect('login')
    return render(request, 'login.html')


# doLogin function
def doLogin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user!=None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('hod_home')
            elif user_type == '2':
                return redirect('staff_home')
            elif user_type == '3':
                return redirect('student_home')
            else:
                # alert messages
                messages.error(request, 'Email and Password are invalid !!')
                return redirect('login')
        else:
            # alert Messages
            messages.error(request, 'Email and Password are invalid !!')
            return redirect('login')


def doLogout(request):
    return redirect('login')


# to see profile update
@login_required(login_url='/')
def Profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)


# profile update:
@login_required(login_url='/')
def ProfileUpdate(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            Customuser = CustomUser.objects.get(id=request.user.id)
            Customuser.first_name = first_name
            Customuser.last_name = last_name

            if password != None and password != '':
                Customuser.set_password(password)
            if profile_pic != None and profile_pic != '':
                Customuser.profile_pic = profile_pic
            Customuser.save()
            messages.success(request, 'Profile updated successfully !')
            return redirect('profile')
        except:
            messages.error(request, 'Failed to Update your Profile !!')
    return render(request, 'profile.html')

def reset_password(request):
    return render(request, 'password_reset_form.html')


# confirm password reset confirm:
def custom_password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset. You can now log in with your new password.')
                return redirect('password_reset_complete')
            else:
                messages.error(request, 'Passwords do not match. Please try again.')
                return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
        else:
            return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('password_reset')

