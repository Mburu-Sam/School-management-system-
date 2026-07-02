from django import forms
from django.contrib.auth.models import User
from .models import Student, Teacher, Class, Attendance, Grade, Subject, FeeStatement, AdmissionApplication, Assignment, AssignmentSubmission

class StudentForm(forms.ModelForm):
    classes = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        empty_label="Select a class",
        required=False,
    )

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'classes']

    def save(self, commit=True):
        student = super().save(commit=False)
        selected_class = self.cleaned_data.get('classes')
        if commit:
            student.save()
            if selected_class:
                student.classes.add(selected_class)
        return student

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'email', 'subject']

class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'email', 'subject']

class TeacherSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']

class TeacherClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'subject']

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['subject'].queryset = Subject.objects.filter(teacher=teacher)

class StudentSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    classes = forms.ModelChoiceField(queryset=Class.objects.all(), empty_label="Select a class")

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() or Student.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields did not match.")
        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        student = Student.objects.create(
            user=user,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
        )
        selected_class = self.cleaned_data.get('classes')
        if selected_class:
            student.classes.add(selected_class)
        return user

class AdminSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields did not match.")
        return cleaned_data

    def save(self):
        return User.objects.create_superuser(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )

class TeacherSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=50)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() or Teacher.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields did not match.")
        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
        )
        Teacher.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email'],
            subject=self.cleaned_data['subject'],
        )
        return user

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'teacher', 'subject']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'class_obj', 'date', 'present']

class TeacherAttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'class_obj', 'date', 'present']

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            classes = Class.objects.filter(teacher=teacher)
            self.fields['class_obj'].queryset = classes
            self.fields['student'].queryset = Student.objects.filter(classes__in=classes).distinct()

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'class_obj', 'grade']

class TeacherGradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'class_obj', 'grade']

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            classes = Class.objects.filter(teacher=teacher)
            self.fields['class_obj'].queryset = classes
            self.fields['student'].queryset = Student.objects.filter(classes__in=classes).distinct()

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'teacher', 'description']

class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'email', 'subject']

class StudentProfileUpdateForm(forms.ModelForm):
    classes = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        empty_label="Select a class",
        required=False,
    )

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'classes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['classes'].initial = self.instance.classes.first()

    def save(self, commit=True):
        student = super().save(commit=False)
        selected_class = self.cleaned_data.get('classes')
        if commit:
            student.save()
            student.classes.clear()
            if selected_class:
                student.classes.add(selected_class)
        return student

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['class_obj', 'title', 'description', 'due_date', 'file']

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['assignment', 'file', 'note']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['class_obj', 'title', 'description', 'due_date', 'file']

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['class_obj'].queryset = Class.objects.filter(teacher=teacher)

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['file', 'note']

class FeeStatementForm(forms.ModelForm):
    class Meta:
        model = FeeStatement
        fields = ['student', 'month', 'amount_due', 'amount_paid', 'due_date']

class AdmissionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = ['full_name', 'email', 'phone', 'desired_class', 'message']
