from io import BytesIO

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .models import Student, Teacher, Class, Attendance, Grade, Subject, FeeStatement, AdmissionApplication, Assignment, AssignmentSubmission
from .forms import StudentForm, TeacherForm, ClassForm, AttendanceForm, GradeForm, SubjectForm, FeeStatementForm, AdmissionApplicationForm, StudentSignupForm, TeacherSignupForm, StudentProfileUpdateForm, AdminSignupForm, TeacherProfileUpdateForm, TeacherSubjectForm, TeacherClassForm, TeacherAttendanceForm, TeacherGradeForm, AssignmentForm, AssignmentSubmissionForm


def is_admin(user):
    return user.is_authenticated and user.is_staff


def is_teacher(user):
    return user.is_authenticated and hasattr(user, 'teacher_profile')


def is_student(user):
    return user.is_authenticated and hasattr(user, 'student_profile')


def homepage(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_classes = Class.objects.count()
    recent_students = Student.objects.order_by('-id')[:5]
    return render(
        request,
        'home.html',
        {
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_classes': total_classes,
            'recent_students': recent_students,
        },
    )


def make_pdf_response(filename, lines):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    y = 760
    for line in lines:
        pdf.drawString(40, y, line)
        y -= 18
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def home(request):
    return redirect('homepage')


def signup_choice(request):
    return render(request, 'signup_choice.html')

# Public admissions form

def admission_apply(request):
    if request.method == 'POST':
        form = AdmissionApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = AdmissionApplicationForm()
    return render(request, 'admission_apply.html', {'form': form})

# Public student signup

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = StudentSignupForm()
    return render(request, 'student_signup.html', {'form': form})

# Public teacher signup

def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = TeacherSignupForm()
    return render(request, 'teacher_signup.html', {'form': form})


def admin_signup(request):
    if request.method == 'POST':
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = AdminSignupForm()
    return render(request, 'admin_signup.html', {'form': form})


@login_required
def role_redirect(request):
    if request.user.is_staff:
        return redirect('homepage')
    if is_teacher(request.user):
        return redirect('teacher_dashboard')
    if is_student(request.user):
        return redirect('student_dashboard')
    return redirect('homepage')

# Admin-only student registration
@user_passes_test(is_admin)
def student_register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_register.html', {'form': form})

# Admin-only list of students
@user_passes_test(is_admin)
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

# Admin-only teacher registration
@user_passes_test(is_admin)
def teacher_register(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'teacher_register.html', {'form': form})

# Admin-only list of teachers
@user_passes_test(is_admin)
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher_list.html', {'teachers': teachers})

# Admin-only class creation
@user_passes_test(is_admin)
def class_create(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = ClassForm()
    return render(request, 'class_create.html', {'form': form})

# Admin-only class list
@user_passes_test(is_admin)
def class_list(request):
    classes = Class.objects.all()
    return render(request, 'class_list.html', {'classes': classes})

# Admin-only subject creation
@user_passes_test(is_admin)
def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'subject_create.html', {'form': form})

# Admin-only subject list
@user_passes_test(is_admin)
def subject_list(request):
    subjects = Subject.objects.select_related('teacher').all()
    return render(request, 'subject_list.html', {'subjects': subjects})

# Admin-only enrollment (add student to class)
@user_passes_test(is_admin)
def enroll_student(request, student_id, class_id):
    student = Student.objects.get(id=student_id)
    class_obj = Class.objects.get(id=class_id)
    student.classes.add(class_obj)
    return redirect('student_list')

# Admin-only attendance creation
@user_passes_test(is_admin)
def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'attendance_create.html', {'form': form})

# Admin-only attendance list
@user_passes_test(is_admin)
def attendance_list(request):
    attendance = Attendance.objects.select_related('student', 'class_obj').all()
    return render(request, 'attendance_list.html', {'attendance': attendance})

# Admin-only grades creation
@user_passes_test(is_admin)
def grade_create(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('grade_list')
    else:
        form = GradeForm()
    return render(request, 'grade_create.html', {'form': form})

# Admin-only grade list
@user_passes_test(is_admin)
def grade_list(request):
    grades = Grade.objects.select_related('student', 'class_obj').all()
    return render(request, 'grade_list.html', {'grades': grades})

# Admin-only fee statement creation
@user_passes_test(is_admin)
def fee_statement_create(request):
    if request.method == 'POST':
        form = FeeStatementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fee_statement_list')
    else:
        form = FeeStatementForm()
    return render(request, 'fee_statement_create.html', {'form': form})

# Admin-only fee list
@user_passes_test(is_admin)
def fee_statement_list(request):
    statements = FeeStatement.objects.select_related('student').all()
    return render(request, 'fee_statement_list.html', {'statements': statements})

# Teacher dashboard for grades of their students
@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    classes = Class.objects.filter(teacher=teacher)
    students = Student.objects.filter(classes__in=classes).distinct()
    grades = Grade.objects.filter(class_obj__in=classes).select_related('student', 'class_obj')
    attendance = Attendance.objects.filter(class_obj__in=classes).select_related('student', 'class_obj')
    assignments = Assignment.objects.filter(teacher=teacher).select_related('class_obj')
    return render(request, 'teacher_dashboard.html', {'teacher': teacher, 'classes': classes, 'students': students, 'grades': grades, 'attendance': attendance, 'assignments': assignments})

# Student dashboard/profile
@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    attendance = Attendance.objects.filter(student=student).select_related('class_obj')
    grades = Grade.objects.filter(student=student).select_related('class_obj')
    fee_statements = FeeStatement.objects.filter(student=student)
    classes = student.classes.all()
    subjects = Subject.objects.filter(classes__in=classes).distinct()
    assignments = Assignment.objects.filter(class_obj__in=classes).distinct()
    return render(request, 'student_dashboard.html', {'student': student, 'attendance': attendance, 'grades': grades, 'fee_statements': fee_statements, 'classes': classes, 'subjects': subjects, 'assignments': assignments})

# Student profile update
@login_required
@user_passes_test(is_student)
def student_profile_update(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == 'POST':
        form = StudentProfileUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')
    else:
        form = StudentProfileUpdateForm(instance=student)
    return render(request, 'student_profile_update.html', {'form': form, 'student': student})

@login_required
@user_passes_test(is_teacher)
def teacher_profile_update(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    if request.method == 'POST':
        form = TeacherProfileUpdateForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = TeacherProfileUpdateForm(instance=teacher)
    return render(request, 'teacher_profile_update.html', {'form': form, 'teacher': teacher})

@login_required
@user_passes_test(is_teacher)
def teacher_subject_create(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    if request.method == 'POST':
        form = TeacherSubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.teacher = teacher
            subject.save()
            return redirect('teacher_dashboard')
    else:
        form = TeacherSubjectForm()
    return render(request, 'subject_create.html', {'form': form})

@login_required
@user_passes_test(is_teacher)
def teacher_class_create(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    if request.method == 'POST':
        form = TeacherClassForm(request.POST, teacher=teacher)
        if form.is_valid():
            class_obj = form.save(commit=False)
            class_obj.teacher = teacher
            class_obj.save()
            return redirect('teacher_dashboard')
    else:
        form = TeacherClassForm(teacher=teacher)
    return render(request, 'class_create.html', {'form': form})

@login_required
@user_passes_test(is_teacher)
def teacher_attendance_create(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    if request.method == 'POST':
        form = TeacherAttendanceForm(request.POST, teacher=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = TeacherAttendanceForm(teacher=teacher)
    return render(request, 'attendance_create.html', {'form': form})

@login_required
@user_passes_test(is_teacher)
def teacher_grade_create(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    if request.method == 'POST':
        form = TeacherGradeForm(request.POST, teacher=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = TeacherGradeForm(teacher=teacher)
    return render(request, 'grade_create.html', {'form': form})

@login_required
@user_passes_test(is_teacher)
def teacher_assignment_create(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, teacher=teacher)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = teacher
            assignment.save()
            return redirect('teacher_dashboard')
    else:
        form = AssignmentForm(teacher=teacher)
    return render(request, 'assignment_create.html', {'form': form})

@login_required
@user_passes_test(is_student)
def assignment_submit(request, assignment_id):
    student = get_object_or_404(Student, user=request.user)
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = student
            submission.save()
            return redirect('student_dashboard')
    else:
        form = AssignmentSubmissionForm()
    return render(request, 'assignment_submit.html', {'form': form, 'assignment': assignment})

# Download transcript for student
@login_required
@user_passes_test(is_student)
def download_transcript(request):
    student = get_object_or_404(Student, user=request.user)
    grades = Grade.objects.filter(student=student).select_related('class_obj')
    lines = [f"Transcript for {student.first_name} {student.last_name}", "", "Grades:"]
    for grade in grades:
        lines.append(f"{grade.class_obj}: {grade.grade}")
    return make_pdf_response(f"transcript_{student.id}.pdf", lines)

@login_required
@user_passes_test(is_student)
def download_attendance_report(request):
    student = get_object_or_404(Student, user=request.user)
    attendance = Attendance.objects.filter(student=student).select_related('class_obj')
    lines = [f"Attendance Report for {student.first_name} {student.last_name}", "", "Attendance:"]
    for item in attendance:
        status = 'Present' if item.present else 'Absent'
        lines.append(f"{item.date} - {status} - {item.class_obj}")
    return make_pdf_response(f"attendance_report_{student.id}.pdf", lines)

@login_required
@user_passes_test(is_student)
def download_fee_statement_report(request):
    student = get_object_or_404(Student, user=request.user)
    fee_statements = FeeStatement.objects.filter(student=student)
    lines = [f"Fee Statement Report for {student.first_name} {student.last_name}", "", "Fee Statements:"]
    for statement in fee_statements:
        lines.append(f"{statement.month} - Due: {statement.amount_due} - Paid: {statement.amount_paid} - Balance: {statement.balance} - Due Date: {statement.due_date}")
    return make_pdf_response(f"fee_statement_report_{student.id}.pdf", lines)
