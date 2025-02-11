# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Batches(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    programs = models.ForeignKey('Programs', models.DO_NOTHING, db_column='Programs_ID')  # Field name made lowercase.
    current_level = models.CharField(db_column='Current_Level', max_length=45)  # Field name made lowercase.
    is_active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'batches'


class CaSechedule(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    start_date = models.DateField(db_column='Start_date')  # Field name made lowercase.
    criterias = models.ForeignKey('Criterias', models.DO_NOTHING, db_column='criterias_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ca_sechedule'


class Courses(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    semesters = models.ForeignKey('Semesters', models.DO_NOTHING, db_column='Semesters_ID')  # Field name made lowercase.
    subjects = models.ForeignKey('Subjects', models.DO_NOTHING, db_column='Subjects_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'courses'


class CoursesBatches(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    courses = models.ForeignKey(Courses, models.DO_NOTHING, db_column='Courses_ID')  # Field name made lowercase.
    batches = models.ForeignKey(Batches, models.DO_NOTHING, db_column='Batches_ID')  # Field name made lowercase.
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'courses_batches'


class CoursesLecturer(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=45)  # Field name made lowercase.
    lectures = models.ForeignKey('Lecturers', models.DO_NOTHING, db_column='Lectures_ID')  # Field name made lowercase.
    courses = models.ForeignKey(Courses, models.DO_NOTHING, db_column='Courses_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'courses_lecturer'


class CoursesStudent(models.Model):
    enroll_id = models.AutoField(db_column='Enroll_Id', primary_key=True)  # Field name made lowercase.
    marks = models.DecimalField(db_column='Marks', max_digits=10, decimal_places=0)  # Field name made lowercase.
    students = models.ForeignKey('Students', models.DO_NOTHING, db_column='Students_ID')  # Field name made lowercase.
    courses = models.ForeignKey(Courses, models.DO_NOTHING, db_column='Courses_ID')  # Field name made lowercase.
    level = models.IntegerField(db_column='Level')  

    class Meta:
        managed = False
        db_table = 'courses_student'


class Criterias(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nature = models.CharField(db_column='Nature', max_length=8)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=2)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45)  # Field name made lowercase.
    weights = models.IntegerField(db_column='Weights')  # Field name made lowercase.
    courses = models.ForeignKey(Courses, models.DO_NOTHING, db_column='Courses_ID')  # Field name made lowercase.
    max_mark = models.IntegerField(db_column='Max_mark', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'criterias'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Lecturers(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    phone_number = models.CharField(db_column='Phone_number', max_length=12)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100)  # Field name made lowercase.
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'lecturers'


class Programs(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    level = models.IntegerField(db_column='Level')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'programs'


class RepeatEnrollments(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    attemp_no = models.IntegerField(db_column='Attemp_no')  # Field name made lowercase.
    repeat_date = models.DateField(db_column='Repeat_date')  # Field name made lowercase.
    assessment_type = models.CharField(db_column='Assessment_type', max_length=2, blank=True, null=True)  # Field name made lowercase.
    students = models.ForeignKey('Students', models.DO_NOTHING, db_column='Students_ID')  # Field name made lowercase.
    courses = models.ForeignKey(Courses, models.DO_NOTHING, db_column='Courses_ID')  # Field name made lowercase.
    lecturers = models.ForeignKey(Lecturers, models.DO_NOTHING, db_column='Lecturers_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'repeat_enrollments'


class Results(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    grade = models.CharField(db_column='Grade', max_length=20, blank=True, null=True)  # Field name made lowercase.
    s_grade = models.CharField(db_column='S_grade', max_length=45, blank=True, null=True)  # Field name made lowercase.
    courses = models.ForeignKey(Courses, models.DO_NOTHING, db_column='Courses_ID')  # Field name made lowercase.
    students = models.ForeignKey('Students', models.DO_NOTHING, db_column='Students_ID')  # Field name made lowercase.
    parent_id = models.IntegerField(db_column='Parent_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'results'


class Semesters(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    start_date = models.DateField(db_column='Start_date')  # Field name made lowercase.
    end_date = models.DateField(db_column='End_date')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'semesters'


class Students(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    index_no = models.CharField(db_column='Index_No', max_length=45, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    batches = models.ForeignKey(Batches, models.DO_NOTHING, db_column='batches_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'students'


class StudentsCriterias(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    students = models.ForeignKey(Students, models.DO_NOTHING, db_column='Students_ID')  # Field name made lowercase.
    criterias = models.ForeignKey(Criterias, models.DO_NOTHING, db_column='Criterias_ID')  # Field name made lowercase.
    mark = models.CharField(db_column='Mark', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'students_criterias'


class Subjects(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=45)  # Field name made lowercase.
    total_credit = models.IntegerField(db_column='Total_credit', blank=True, null=True)  # Field name made lowercase.
    theory_credit = models.IntegerField(db_column='Theory_credit', blank=True, null=True)  # Field name made lowercase.
    practical_credit = models.IntegerField(db_column='Practical_credit', blank=True, null=True)  # Field name made lowercase.
    level = models.IntegerField(db_column='Level')  # Field name made lowercase.
    programs = models.ForeignKey(Programs, models.DO_NOTHING, db_column='Programs_ID')  # Field name made lowercase.
    ca = models.IntegerField(db_column='CA')  # Field name made lowercase.
    fe = models.IntegerField(db_column='FE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'subjects'
