from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from student_management_app.models import Staff, Subject, Session_Year, Student, Attendance, AttendanceReport, Course


@login_required(login_url='/')
def Staff_Home(request):
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
        print(staff_subjects_dict)

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
    return render(request, 'Staff/home.html', context)


@login_required(login_url='/')
def feature_view_course(request):
    course = Course.objects.all()
    if request.method == 'GET':
        cr = request.GET.get('search')  # cr=course
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
    return render(request, 'Staff/staff_view_courses.html', context)


@login_required(login_url='/')
def feature_view_students(request):
    student = Student.objects.all()
    if request.method == 'GET':
        st = request.GET.get('search')
        if st != None:
            multiple_st = Q(Q(admin__first_name__icontains=st) | Q(admin__last_name__icontains=st))
            student = Student.objects.filter(multiple_st)

    page = Paginator(student, 3)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {
        'page': page,
        'student': student,
    }
    return render(request, 'Staff/staff_view_student.html', context)


@login_required(login_url='/')
def feature_view_staffs(request):
    staff = Staff.objects.all()
    # adding pagination
    if request.method == 'GET':
        st = request.GET.get('search')
        if st != None:
            multiple_st = Q(Q(admin__first_name__icontains=st) | Q(admin__last_name__icontains=st))
            staff = Staff.objects.filter(multiple_st)

    page = Paginator(staff, 3)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context = {
        'page': page,
        'staff': staff,
    }
    return render(request, 'Staff/staff_view_staff.html', context)


@login_required(login_url='/')
def feature_view_subjects(request):
    subject = Subject.objects.all()
    # adding pagination
    if request.method == 'GET':
        sub = request.GET.get('search')  # sub = subject
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
    return render(request, 'Staff/staff_view_subject.html', context)


@login_required(login_url='/')
def feature_view_sessions(request):
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
    return render(request, 'Staff/staff_view_session.html', context)



# take_attendance function:
@login_required(login_url='/')
def Take_Attendance(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    subject = Subject.objects.filter(staff=staff_id)
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')

    get_subject = None
    get_session_year = None
    students = None
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')

            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)
            subject = Subject.objects.filter(id=subject_id)
            for i in subject:
                student_id = i.course.id
                students = Student.objects.filter(course_id=student_id)

    context = {
        'subject': subject,
        'session_year': session_year,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'action': action,
        'students': students,
    }

    return render(request, 'Staff/take_attendance.html', context)


@login_required(login_url='/')
def Save_Attendance(request):
    if request.method == "POST":
        subject_id = request.POST.get('sub_id')
        session_year_id = request.POST.get('session_year_id')
        attendance_date = request.POST.get('attendance_date')
        student_id = request.POST.getlist('student_id')

        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session_Year.objects.get(id=session_year_id)

        attendance = Attendance(
            subject_id=get_subject,
            attendance_date=attendance_date,
            session_year_id=get_session_year
        )
        attendance.save()
        messages.success(request, 'Attendance saved successfully.')

        for i in student_id:
            stud_id = i
            int_stu = int(stud_id)
            p_students = Student.objects.get(id=int_stu)  #p_student -> present students
            attendance_report = AttendanceReport(
                student_id=p_students,
                attendance_id=attendance,
            )
            attendance_report.save()
    return redirect('take_attendances')


@login_required(login_url='/')
def View_Staff_Attendance(request):
    subject = Subject.objects.all()
    session_year = Session_Year.objects.all()

    action = request.GET.get('action')

    get_subject = None
    get_session_year = None
    attendance_date = None
    attendance_report = None
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')
            attendance_date = request.POST.get('attendance_date')

            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)

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
    return render(request, 'Staff/view_attendance.html', context)



