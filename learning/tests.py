from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from learning.forms import AdminSignupForm, AssignmentForm, TeacherClassForm
from learning.models import Class, Subject, Teacher


class AuthFlowTests(TestCase):
    def test_admin_signup_form_creates_staff_user(self):
        form = AdminSignupForm(
            {
                "username": "adminuser",
                "email": "admin@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
                "first_name": "Admin",
                "last_name": "User",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)

    def test_role_redirect_routes_staff_users_to_homepage(self):
        admin = User.objects.create_user(
            username="staffredirect",
            email="staffredirect@example.com",
            password="Secret123!",
            is_staff=True,
        )

        self.client.force_login(admin)
        response = self.client.get(reverse("role_redirect"))

        self.assertRedirects(response, reverse("homepage"))

    def test_teacher_class_form_limits_subjects_to_teacher(self):
        teacher = Teacher.objects.create(name="Test Teacher", email="teacher@example.com", subject="Math")
        owned_subject = Subject.objects.create(name="Algebra", teacher=teacher, description="")
        other_subject = Subject.objects.create(name="Biology", description="")

        form = TeacherClassForm(teacher=teacher)

        self.assertIn(owned_subject, form.fields['subject'].queryset)
        self.assertNotIn(other_subject, form.fields['subject'].queryset)

    def test_teacher_assignment_form_limits_classes_to_teacher(self):
        teacher = Teacher.objects.create(name="Teacher", email="teacher2@example.com", subject="Science")
        allowed_class = Class.objects.create(name="Grade 7", teacher=teacher, subject=None)
        other_class = Class.objects.create(name="Grade 8", teacher=None, subject=None)

        form = AssignmentForm(teacher=teacher)

        self.assertIn(allowed_class, form.fields['class_obj'].queryset)
        self.assertNotIn(other_class, form.fields['class_obj'].queryset)
