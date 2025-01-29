from django.db import models

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

class Semesters(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  
    start_date = models.DateField(db_column='Start_date')  
    end_date = models.DateField(db_column='End_date')  

    class Meta:
        managed = False
        db_table = 'semesters'
        
class Batches(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    programs = models.ForeignKey('Programs', models.DO_NOTHING, db_column='Programs_ID')  # Field name made lowercase.
    current_level = models.CharField(db_column='Current_Level', max_length=45, blank=True, null=True)  # Field name made lowercase.
    is_active = models.BooleanField(db_column='is_active', default=True)

    class Meta:
        managed = False
        db_table = 'batches'
        
class Programs(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    level = models.IntegerField(db_column='Level')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'programs'
        
class Subjects(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=45)  # Field name made lowercase.
    total_credit = models.IntegerField(db_column='Total_credit', blank=True, null=True)  # Field name made lowercase.
    theory_credit = models.IntegerField(db_column='Theory_credit', blank=True, null=True)  # Field name made lowercase.
    practical_credit = models.IntegerField(db_column='Practical_credit', blank=True, null=True)  # Field name made lowercase.
    level = models.IntegerField(db_column='Level')  # Field name made lowercase.
    programs = models.ForeignKey(Programs, models.DO_NOTHING, db_column='Programs_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'subjects'
        
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

    class Meta:
        managed = False
        db_table = 'courses_batches'

class Results(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    grade = models.CharField(db_column='Grade', max_length=20)  # Field name made lowercase.
    courses = models.ForeignKey(Courses, models.DO_NOTHING, db_column='Courses_ID')  # Field name made lowercase.
    students = models.ForeignKey('Students', models.DO_NOTHING, db_column='Students_ID')  # Field name made lowercase.
    parent_id = models.CharField(db_column='Parent_ID', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'results'
        
class Students(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    index_no = models.CharField(db_column='Index_No', max_length=45, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    batches = models.ForeignKey(Batches, models.DO_NOTHING, db_column='batches_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'students'
        
