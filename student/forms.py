from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import *

class StudentRegistrationForm(forms.Form):
    # Form fields for user input
    username = forms.CharField(max_length=150)
    name = forms.CharField(max_length=100)
    index_no = forms.CharField(max_length=45)
    batch = forms.ModelChoiceField(
        queryset=Batches.objects.all().order_by('name'),
        empty_label="Select your batch",
        to_field_name="id"
    )
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        # Get the cleaned data from the form
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Check if passwords match
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")

        # Validate password strength using Django's validator
        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error('password', e)
        
        # Check if username already exists
        if User.objects.filter(username=cleaned_data.get('username')).exists():
            self.add_error('username', 'Username already exists')
        
        # Check if index number already exists
        if Students.objects.filter(index_no=cleaned_data.get('index_no')).exists():
            self.add_error('index_no', 'Index number already exists')

        return cleaned_data
    
    def save(self):
        try:
            # First create the user
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password']
            )
            
            # Add to Student group
            student_group, _ = Group.objects.get_or_create(name='Student')
            user.groups.add(student_group)
            
            # Then create the student record with the user
            student = Students.objects.create(
                index_no=self.cleaned_data['index_no'],
                name=self.cleaned_data['name'],
                auth_user=user,  
                batches=self.cleaned_data['batch']
            )
        
            return user

        except Exception as e:
            # Clean up if anything goes wrong
            if 'student' in locals():
                student.delete()
            if 'user' in locals():
                user.delete()
            raise e