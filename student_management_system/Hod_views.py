from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from student_management_app.models import Course, Student, Session_Year, CustomUser, Staff, Subject, Attendance, AttendanceReport, Contact


@login_required(login_url='/')
def Home(request):
    # get all data
    student = Student.objects.all()
    staff = Student.objects.all()
    subject = Subject.objects.all()

    # Retrieve the 5 most recently hired staff members
    recently_hired_staffs = Staff.objects.order_by('-created_at')[:5]

    # Retrieve the 5 most recently admitted students with profile pictures
    recently_admitted_students = Student.objects.order_by('-created_at')[:5]

    # Create a dictionary to store staffs and their subjects
    staff_subjects_dict = {}

    # Retrieve subjects for each of the 5 most recently hired staff members
    for staff in recently_hired_staffs:
        subjects = Subject.objects.filter(staff=staff)
        staff_subjects_dict[staff] = subjects

    # count all the numbers of students, staffs, courses and subjects that are present
    student_count = Student.objects.all().count
    staff_count = Staff.objects.all().count
    course_count = Course.objects.all().count
    subject_count = Subject.objects.all().count

    # for bargraph:
    student_gender_male = Student.objects.filter(gender='Male').count
    student_gender_female = Student.objects.filter(gender='Female').count

    # now after counting we need to pass the output to the template i.e. home.html by creating a dictionary
    context = {
        # data for pie-chart:
        'student_count': student_count,
        'course_count': course_count,
        'staff_count': staff_count,
        'subject_count': subject_count,

        # data for bar-graph:
        'student_gender_male': student_gender_male,
        'student_gender_female': student_gender_female,

        # all data of students, subjects and staffs:
        'student': student,
        'staff': staff,
        'subject': subject,

         # Add recently admitted students, recently hired staffs and their subjects to the context
        'recently_admitted_students': recently_admitted_students,
        'recently_hired_staffs': recently_hired_staffs,
        'staff_subjects_dict': staff_subjects_dict,
    }

    return render(request, 'Hod/home.html', context)


@login_required(login_url='/')
def Add_Students(request):
    # getting all the objects of course and session_year from the admin panel
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    # this is used to get all the input data from add student form and storing in the database
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        print(profile_pic, first_name, last_name, email, username, password, address, gender, course_id, session_year_id)

        # checking the email and username.
        # when adding the student, if email and username matches then
        # new student is not added/created as it already exists

        #checking for email:
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already taken')
            return redirect('add_students')

        #checking for username:
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already taken')
            return redirect('add_students')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=3,
            )
            user.set_password(password)
            user.save()

            # the above code stores all the info to CustomUser/Users
            # adding to student model
            course = Course.objects.get(id=course_id)
            session_year = Session_Year.objects.get(id=session_year_id)

            student = Student(
                admin=user,
                address=address,
                session_year_id=session_year,
                course_id=course,
                gender=gender,
            )
            student.save()
            messages.success(request, user.first_name + "  " + user.last_name + "are successfully saved.")
            return redirect('add_students')

    context = {
        'course': course,
        'session_year': session_year,
    }
    return render(request, 'Hod/add_student.html', context)


@login_required(login_url='/')
def view_students(request):
    student = Student.objects.all()
    if request.method == 'GET':
        st = request.GET.get('search')
        if st!=None:
            multiple_st = Q(Q(admin__first_name__icontains=st)|Q(admin__last_name__icontains=st))
            student = Student.objects.filter(multiple_st)

    page = Paginator(student, 3)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {
        'page': page,
        'student': student,
    }
    return render(request, 'Hod/view_student.html', context)


@login_required(login_url='/')
def Edit_Students(request, id):
    student = Student.objects.filter(id=id)
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    context = {
        'student': student,
        'course': course,
        'session_year': session_year,
    }
    return render(request, 'Hod/edit_student.html', context)


@login_required(login_url='/')
def Update_Students(request):
    # this is used to get all the input data from edit student form and storing in the database
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        user = CustomUser.objects.get(id=student_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != '':
            user.set_password(password)
        if profile_pic != None and profile_pic != '':
            user.profile_pic = profile_pic
        user.save()

        student = Student.objects.get(admin=student_id)
        student.address = address
        student.gender = gender

        course = Course.objects.get(id=course_id)
        student.course_id = course

        session_year = Session_Year.objects.get(id=session_year_id)
        student.session_year_id = session_year

        student.save()
        messages.success(request, 'Student record are updated successfully.')

        return redirect('view_students')

    return render(request, 'Hod/edit_student.html')


@login_required(login_url='/')
def Delete_Students(request, admin):
    student = CustomUser.objects.get(id=admin)
    student.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('view_students')


# adding courses:
@login_required(login_url='/')
def Add_Courses(request):
    if request.method == "POST":
        course_name = request.POST.get('course_name')
        print(course_name)

        course = Course(
            name=course_name,
        )
        course.save()
        messages.success(request, 'Course added successfully.')
        return redirect('add_courses')

    return render(request, 'Hod/add_course.html')


@login_required(login_url='/')
def View_Courses(request):
    course = Course.objects.all()
    if request.method == 'GET':
        cr = request.GET.get('search')  #cr=course
        if cr != None:
            multiple_cr = Q(Q(name__icontains=cr))
            course = Course.objects.filter(multiple_cr)

    page = Paginator(course, 3)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    # creating dictionary of courses and passing that dictionary to the template i.e. view_course.html
    context = {
        'page': page,
    }
    return render(request, 'Hod/view_course.html', context)


@login_required(login_url='/')
def Edit_Courses(request, id):
    course = Course.objects.get(id=id)

    # creating dictionary of courses and passing that dictionary to the template i.e. edit_course.html
    context = {
        'course': course,
    }
    return render(request, 'Hod/edit_course.html', context)


@login_required(login_url='/')
def Update_Courses(request):
    if request.method == "POST":
        course_id = request.POST.get('course_id')
        name = request.POST.get('name')

        course = Course.objects.get(id=course_id)
        course.name = name
        course.save()
        messages.success(request, 'Course updated successfully.')
        return redirect('view_courses')
    return render(request, 'Hod/edit_course.html')


@login_required(login_url='/')
def Delete_Courses(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('view_courses')


@login_required(login_url='/')
def Add_Staffs(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        # checking for email:
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists.')
            return redirect('add_staffs')

        # checking for username:
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists.')
            return redirect('add_staffs')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=2,
            )
            user.set_password(password)
            user.save()

            staff = Staff(
                admin=user,
                address=address,
                gender=gender
            )
            staff.save()
            print("Staff",staff)
            messages.success(request, 'Staff added successfully')
            return redirect('add_staffs')
    return render(request, 'Hod/add_staff.html')


@login_required(login_url='/')
def View_Staffs(request):
    staff = Staff.objects.all()
    # adding pagination
    if request.method == 'GET':
        st = request.GET.get('search')
        if st!=None:
            multiple_st = Q(Q(admin__first_name__icontains=st)|Q(admin__last_name__icontains=st))
            staff = Staff.objects.filter(multiple_st)
    page = Paginator(staff, 3)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context = {
        'page': page,
        'staff': staff,
    }
    return render(request, 'Hod/view_staff.html', context)


@login_required(login_url='/')
def Edit_Staffs(request, id):
    staff = Staff.objects.get(id=id)
    context = {
        'staff': staff,
    }
    return render(request, 'Hod/edit_staff.html', context)


@login_required(login_url='/')
def Update_Staffs(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        user = CustomUser.objects.get(id=staff_id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        if password != None and password != '':
            user.set_password(password)
        if profile_pic != None and profile_pic != '':
            user.profile_pic = profile_pic
        user.save()

        staff = Staff.objects.get(admin=staff_id)
        staff.gender = gender
        staff.address = address
        staff.save()
        messages.success(request, 'Updated successfully')
        return redirect('view_staffs')
    return render(request, 'Hod/edit_staff.html')


@login_required(login_url='/')
def Delete_Staffs(request, admin):
    staff = CustomUser.objects.get(id=admin)
    staff.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('view_staffs')


@login_required(login_url='/')
def Add_Subjects(request):
    course = Course.objects.all()
    staff = Staff.objects.all()

    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id=course_id)
        staff = Staff.objects.get(id=staff_id)

        subject = Subject(
            name=subject_name,
            course=course,
            staff=staff,
        )
        subject.save()
        messages.success(request, 'Subject added successfully.')
        return redirect('add_subjects')
    context = {
        'course': course,
        'staff': staff,
    }
    return render(request, 'Hod/add_subjects.html', context)


@login_required(login_url='/')
def View_Subjects(request):
    subject = Subject.objects.all()
    # adding pagination
    if request.method == 'GET':
        sub = request.GET.get('search')  #sub = subject
        if sub != None:
            multiple_cr = Q(Q(name__icontains=sub))
            subject = Subject.objects.filter(multiple_cr)
    page = Paginator(subject, 3)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    # creating dictionary of courses and passing that dictionary to the template i.e. view_course.html
    context = {
        'page': page,
    }
    return render(request, 'Hod/view_subject.html', context)


@login_required(login_url='/')
def Edit_Subjects(request, id):
    subject = Subject.objects.get(id=id)
    course = Course.objects.all()
    staff = Staff.objects.all()

    context = {
        'subject': subject,
        'course': course,
        'staff': staff,
    }
    return render(request, 'Hod/edit_subject.html', context)


@login_required(login_url='/')
def Update_Subjects(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id=course_id)
        staff = Staff.objects.get(id=staff_id)

        subject = Subject(
            id=subject_id,
            name=subject_name,
            course=course,
            staff=staff,
        )
        subject.save()
        messages.success(request, 'Updated successfully.')
        return redirect('view_subjects')


@login_required(login_url='/')
def Delete_Subjects(request, id):
    subject = Subject.objects.get(id=id)
    subject.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('view_subjects')


@login_required(login_url='/')
def Add_Sessions(request):
    if request.method == "POST":
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session_Year(
            session_start=session_year_start,
            session_end=session_year_end,
        )
        session.save()
        messages.success(request, 'Session added successfully.')
        return redirect('add_sessions')
    return render(request, 'Hod/add_session.html')


@login_required(login_url='/')
def View_Sessions(request):
    session = Session_Year.objects.all()
    # adding pagination
    if request.method == 'GET':
        ses = request.GET.get('search')  # sess = session
        if ses != None:
            multiple_st = Q(Q(session_start__icontains=ses) | Q(session_end__icontains=ses))
            session = Session_Year.objects.filter(multiple_st)
    page = Paginator(session, 3)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context = {
        'page': page
    }
    return render(request, 'Hod/view_session.html', context)


@login_required(login_url='/')
def Edit_Sessions(request, id):
    session = Session_Year.objects.filter(id=id)

    context = {
        'session': session,
    }
    return render(request, 'Hod/edit_session.html', context)


@login_required(login_url='/')
def Update_Sessions(request):
    if request.method == "POST":
        session_id = request.POST.get('session_id')
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session_Year(
            id=session_id,
            session_start=session_year_start,
            session_end=session_year_end,
        )
        session.save()
        messages.success(request, 'Updated successfully.')
        return redirect('view_sessions')


@login_required(login_url='/')
def Delete_Sessions(request, id):
    session = Session_Year.objects.get(id=id)
    session.delete()
    messages.success(request, 'Deleted successfully.')
    return redirect('view_sessions')


@login_required(login_url='/')
def view_attendance(request):
    subject = Subject.objects.all()
    session_year = Session_Year.objects.all()

    action = request.GET.get('action')

    get_subject = None
    get_session_year = None
    attendance_date = None
    attendance_report = None

    if action is None:
        # Render the initial form without any processing
        context = {
            'subject': subject,
            'session_year': session_year,
            'action': action,
        }
        return render(request, 'Hod/view_attendance.html', context)

    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        attendance_date = request.POST.get('attendance_date')

        # Validate that all required fields are not empty
        if not subject_id or not session_year_id or not attendance_date:
            messages.error(request, 'All fields are required.')
            return redirect('view_attendances')

        try:
            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)
        except Subject.DoesNotExist or Session_Year.DoesNotExist:
            messages.error(request, 'Invalid subject or session year.')
            return redirect('view_attendances')

        # Now proceed with attendance report retrieval and rendering
        attendance = Attendance.objects.filter(subject_id=get_subject, attendance_date=attendance_date)
        for i in attendance:
            attendance_id = i.id
            attendance_report = AttendanceReport.objects.filter(attendance_id=attendance_id)

    context = {
        'subject': subject,
        'session_year': session_year,
        'action': action,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'attendance_date': attendance_date,
        'attendance_report': attendance_report,
    }
    return render(request, 'Hod/view_attendance.html', context)


@login_required(login_url='/')
def View_Contacts(request):
    contact = Contact.objects.all()

    # adding pagination
    if request.method == 'GET':
        con = request.GET.get('search')  # sess = session
        if con != None:
            multiple_st = Q(Q(name__icontains=con) | Q(email__icontains=con) | Q(subject__icontains=con))
            contact = Contact.objects.filter(multiple_st)

    page = Paginator(contact, 3)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context = {
        'page': page
    }
    return render(request, 'Hod/view_contacts.html', context)

@login_required(login_url='/')
def Delete_Contacts(request, id):
    contact = Contact.objects.get(id=id)
    contact.delete()
    messages.success(request, 'Deleted successfully.')
    return redirect('view_contacts')
