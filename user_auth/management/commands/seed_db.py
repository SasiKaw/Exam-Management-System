from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from user_auth.models import *
from django.db import connection
import datetime
from django.utils.timezone import make_aware

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database seeding...')
        
        try:
            # Create data in order
            self.create_groups()
            self.create_users()
            self.create_user_groups()
            self.create_programs()
            self.create_batches()
            self.create_semesters()
            self.create_subjects()
            self.create_courses()
            self.create_courses_batches()
            self.create_students()
            self.create_courses_student()
            self.create_criterias()
            self.create_students_criterias()
            self.create_results()
            
            self.stdout.write(self.style.SUCCESS('Successfully seeded database'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding database: {str(e)}'))
            raise e

    def create_groups(self):
        """Create user groups"""
        groups_data = [
            {'id': 3, 'name': 'Student'},
            {'id': 4, 'name': 'Lecturer'},
            {'id': 5, 'name': 'HOD'},
            {'id': 6, 'name': 'BOE'}
        ]
        
        for group in groups_data:
            Group.objects.create(**group)

    def create_users(self):
        """Create all users"""
        users_data = [
            {
                'id': 13,
                'username': 'Admin',
                'password': 'pbkdf2_sha256$720000$scdH9t0qXKqCVrdL5sONh1$Ib3wAWpL/DK10abFx1nLvRq2ypMKWzZkXnTClcxQ/7w=',
                'is_superuser': True,
                'email': 'admin@gmail.com',
                'is_staff': True,
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2024-12-17 17:08:06.388245', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 15,
                'username': 'Avishka',
                'password': 'pbkdf2_sha256$720000$tr5Unh01kU33kpkpqQ5rYO$s+klkJgpZ/m1zOtAQbY5DMzwvj3XPACPvfG3cy3KqPM=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2024-12-18 03:09:30.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 16,
                'username': 'Sasindu',
                'password': 'pbkdf2_sha256$720000$Uri242lDEGhTMHCnrzeHdC$+wsdVc07jvSbAYUOUUAE9x2WAercmSr+5o2m0oSZ09k=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2024-12-18 03:15:32.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 18,
                'username': 'Janith',
                'password': 'pbkdf2_sha256$720000$Iaao8BpFgJmCtQkm5sIKge$gqYemrWac75sLtrRrfYu1MP57qvKykYrQ+kedVlupK8=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2024-12-18 15:44:40.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 22,
                'username': 'Bashini',
                'password': 'pbkdf2_sha256$720000$y7RmNM86Owx0QDAjaV6g5h$XFiflvrrNRl3pbPfH2sVDKoq2HRCeuW8IPQahT8Oh18=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2024-12-19 03:41:10.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 23,
                'username': 'Roshini',
                'password': 'pbkdf2_sha256$720000$e7rgNOFBv7QG5tjmdaDQUq$ad6nz3bTvT9A6tV1iK9Z6wcsLWH6MbBkzQVPt+VXIZQ=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2025-02-11 04:07:21.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
        ]
        
        for user_data in users_data:
            User.objects.create(**user_data)

    def create_user_groups(self):
        """Assign users to groups"""
        assignments = [
            {'user_id': 15, 'group_id': 3},  # Avishka -> Student
            {'user_id': 16, 'group_id': 3},  # Sasindu -> Student
            {'user_id': 18, 'group_id': 4},  # Janith -> Lecturer
            {'user_id': 22, 'group_id': 5},  # Bashini -> HOD
            {'user_id': 23, 'group_id': 6},  # Roshini -> BOE
        ]
        
        for assignment in assignments:
            user = User.objects.get(id=assignment['user_id'])
            group = Group.objects.get(id=assignment['group_id'])
            user.groups.add(group)

    def create_programs(self):
        """Create programs"""
        programs_data = [
            {'id': 1, 'name': 'BSc(Hons) Software Engineering', 'level': 8},
            {'id': 2, 'name': 'BSc(Hons) in Computing (IS)', 'level': 8}
        ]
        
        for prog_data in programs_data:
            Programs.objects.create(**prog_data)

    def create_batches(self):
        """Create batches with correct current levels"""
        batches_data = [
            # SE Batches
            {'id': 1, 'name': 'SE01', 'programs_id': 1, 'current_level': '4', 'is_active': 1},
            {'id': 2, 'name': 'SE02', 'programs_id': 1, 'current_level': '3', 'is_active': 1},
            {'id': 3, 'name': 'SE03', 'programs_id': 1, 'current_level': '2', 'is_active': 1},
            {'id': 4, 'name': 'SE04', 'programs_id': 1, 'current_level': '2', 'is_active': 1},
            {'id': 5, 'name': 'SE05', 'programs_id': 1, 'current_level': '1', 'is_active': 1},
            
            # UOG Batches
            {'id': 6, 'name': 'UOG01', 'programs_id': 2, 'current_level': '6', 'is_active': 1},
            {'id': 7, 'name': 'UOG02', 'programs_id': 2, 'current_level': '5', 'is_active': 1},
            {'id': 8, 'name': 'UOG03', 'programs_id': 2, 'current_level': '5', 'is_active': 1},
            {'id': 9, 'name': 'UOG04', 'programs_id': 2, 'current_level': '4', 'is_active': 1},
            {'id': 10, 'name': 'UOG07', 'programs_id': 2, 'current_level': '4', 'is_active': 1},
            {'id': 11, 'name': 'UOG08', 'programs_id': 2, 'current_level': '3', 'is_active': 1},
            {'id': 12, 'name': 'UOG09', 'programs_id': 2, 'current_level': '3', 'is_active': 1},
            {'id': 13, 'name': 'UOG10', 'programs_id': 2, 'current_level': '2', 'is_active': 1},
            {'id': 14, 'name': 'UOG11', 'programs_id': 2, 'current_level': '2', 'is_active': 1}
        ]
        
        for batch_data in batches_data:
            Batches.objects.create(**batch_data)

    def create_semesters(self):
        """Create semesters with actual academic calendar dates"""
        semesters_data = [
            {
                'id': 1,
                'start_date': '2023-04-01',  # First semester (Year 1 Semester 1)
                'end_date': '2023-10-31',
                'status': 1
            },
            {
                'id': 2,
                'start_date': '2023-11-01',  # Second semester (Year 1 Semester 2)
                'end_date': '2024-04-30',
                'status': 1
            },
            {
                'id': 3,
                'start_date': '2024-05-01',  # Third semester (Year 2 Semester 1)
                'end_date': '2024-10-31',
                'status': 1
            },
            {
                'id': 4,
                'start_date': '2024-11-01',  # Current semester (Year 2 Semester 2)
                'end_date': '2025-03-31',
                'status': 0
            }
        ]
        
        for semester_data in semesters_data:
            Semesters.objects.create(**semester_data)

    # Update in create_subjects():
    def create_subjects(self):
        """Create subjects according to curriculum"""
        subjects_data = [
             # Year 1 Semester 1 (Already have these)
            {'id': 1, 'name': 'Japanese Language Level I', 'code': 'PRF110120', 'total_credit': 2, 'theory_credit': 2, 'practical_credit': 0, 'level': 1, 'programs_id': 1, 'ca': 30, 'fe': 70},
            {'id': 2, 'name': 'Computer Fundamentals', 'code': 'CMP110130', 'total_credit': 3, 'theory_credit': 2, 'practical_credit': 1, 'level': 1, 'programs_id': 1, 'ca': 40, 'fe': 60},
            {'id': 3, 'name': 'Programming Fundamentals', 'code': 'CMP110240', 'total_credit': 4, 'theory_credit': 2, 'practical_credit': 2, 'level': 1, 'programs_id': 1, 'ca': 50, 'fe': 50},
            {'id': 4, 'name': 'Technical Writing', 'code': 'PRF110220', 'total_credit': 2, 'theory_credit': 2, 'practical_credit': 0, 'level': 1, 'programs_id': 1, 'ca': 60, 'fe': 40},
            {'id': 5, 'name': 'Mathematics I for SE', 'code': 'FND110120', 'total_credit': 2, 'theory_credit': 2, 'practical_credit': 0, 'level': 1, 'programs_id': 1, 'ca': 30, 'fe': 70},

            # Year 1 Semester 2 (Already have these)
            {'id': 6, 'name': 'Japanese Language Level II', 'code': 'PRF120120', 'total_credit': 2, 'theory_credit': 2, 'practical_credit': 0, 'level': 2, 'programs_id': 1, 'ca': 30, 'fe': 70},
            {'id': 7, 'name': 'Database Systems', 'code': 'MAA120130', 'total_credit': 3, 'theory_credit': 2, 'practical_credit': 1, 'level': 2, 'programs_id': 1, 'ca': 40, 'fe': 60},
            {'id': 8, 'name': 'Web Programming', 'code': 'CMP120230', 'total_credit': 3, 'theory_credit': 1, 'practical_credit': 2, 'level': 2, 'programs_id': 1, 'ca': 50, 'fe': 50},
            {'id': 9, 'name': 'Mathematics II for SE', 'code': 'FND120120', 'total_credit': 2, 'theory_credit': 2, 'practical_credit': 0, 'level': 2, 'programs_id': 1, 'ca': 30, 'fe': 70},

            # Year 2 Semester 1 (Already have these)
            {'id': 10, 'name': 'Data Structures and Algorithms', 'code': 'CMP210130', 'total_credit': 3, 'theory_credit': 2, 'practical_credit': 1, 'level': 3, 'programs_id': 1, 'ca': 40, 'fe': 60},
            {'id': 11, 'name': 'Software Architecture and Design', 'code': 'PRO210130', 'total_credit': 3, 'theory_credit': 2, 'practical_credit': 1, 'level': 3, 'programs_id': 1, 'ca': 50, 'fe': 50},
            {'id': 12, 'name': 'Visual Application Programming', 'code': 'CMP210230', 'total_credit': 3, 'theory_credit': 1, 'practical_credit': 2, 'level': 3, 'programs_id': 1, 'ca': 50, 'fe': 50},
            {'id': 13, 'name': 'Mathematics III for SE', 'code': 'FND210130', 'total_credit': 3, 'theory_credit': 3, 'practical_credit': 0, 'level': 3, 'programs_id': 1, 'ca': 30, 'fe': 70},

            # Year 2 Semester 2 (Current Semester)
            {'id': 14, 'name': 'Japanese Language Level IV', 'code': 'PRF220120', 'total_credit': 2, 'theory_credit': 2, 'practical_credit': 0, 'level': 4, 'programs_id': 1, 'ca': 30, 'fe': 70},
            {'id': 15, 'name': 'Advanced Database Systems', 'code': 'MAA220130', 'total_credit': 3, 'theory_credit': 2, 'practical_credit': 1, 'level': 4, 'programs_id': 1, 'ca': 40, 'fe': 60},
            {'id': 16, 'name': 'Computer Architecture', 'code': 'DES220130', 'total_credit': 3, 'theory_credit': 2, 'practical_credit': 1, 'level': 4, 'programs_id': 1, 'ca': 40, 'fe': 60},
            {'id': 17, 'name': 'Statistics I for SE', 'code': 'FND220120', 'total_credit': 2, 'theory_credit': 2, 'practical_credit': 0, 'level': 4, 'programs_id': 1, 'ca': 30, 'fe': 70},
            # Year 3 Semester 1 (5th Semester)
            {'id': 18, 'name': 'Operating Systems', 'code': 'CMP310130', 'total_credit': 3, 'theory_credit': 2, 'practical_credit': 1, 'level': 5, 'programs_id': 1, 'ca': 40, 'fe': 60},
            {'id': 19, 'name': 'Software Testing and Quality Assurance', 'code': 'VAV310130', 'total_credit': 3, 'theory_credit': 2, 'practical_credit': 1, 'level': 5, 'programs_id': 1, 'ca': 50, 'fe': 50},
            {'id': 20, 'name': 'Professional Practice and Work Based Learning', 'code': 'PRF310220', 'total_credit': 2, 'theory_credit': 2, 'practical_credit': 0, 'level': 5, 'programs_id': 1, 'ca': 60, 'fe': 40},
            {'id': 21, 'name': 'Statistics II for SE', 'code': 'FND310130', 'total_credit': 3, 'theory_credit': 2, 'practical_credit': 1, 'level': 5, 'programs_id': 1, 'ca': 30, 'fe': 70},
            {'id': 22, 'name': 'Enterprise Application Development', 'code': 'CMP310230', 'total_credit': 3, 'theory_credit': 1, 'practical_credit': 2, 'level': 5, 'programs_id': 1, 'ca': 50, 'fe': 50},
            {'id': 23, 'name': 'Mobile Application Development', 'code': 'CMP310330', 'total_credit': 3, 'theory_credit': 1, 'practical_credit': 2, 'level': 5, 'programs_id': 1, 'ca': 50, 'fe': 50},

            # Year 3 Semester 2 (6th Semester)
            {'id': 24, 'name': 'Physics and Digital Electronics', 'code': 'FND310230', 'total_credit': 3, 'theory_credit': 2, 'practical_credit': 1, 'level': 6, 'programs_id': 1, 'ca': 30, 'fe': 70},
            {'id': 25, 'name': 'Software Evolution', 'code': 'PRO320130', 'total_credit': 3, 'theory_credit': 2, 'practical_credit': 1, 'level': 6, 'programs_id': 1, 'ca': 40, 'fe': 60},
            {'id': 26, 'name': 'Industrial Training', 'code': 'PRF320190', 'total_credit': 9, 'theory_credit': 0, 'practical_credit': 9, 'level': 6, 'programs_id': 1, 'ca': 100, 'fe': 0},
            {'id': 27, 'name': 'Japanese way of doing business', 'code': 'PRF320220', 'total_credit': 2, 'theory_credit': 2, 'practical_credit': 0, 'level': 6, 'programs_id': 1, 'ca': 60, 'fe': 40},
            {'id': 28, 'name': 'Business Management and Regulatory Studies', 'code': 'PRF320330', 'total_credit': 3, 'theory_credit': 3, 'practical_credit': 0, 'level': 6, 'programs_id': 1, 'ca': 50, 'fe': 50},

            # Year 4 Semester 1 (7th Semester)
            {'id': 29, 'name': 'Japanese Language Level VI', 'code': 'PRF410120', 'total_credit': 2, 'theory_credit': 2, 'practical_credit': 0, 'level': 7, 'programs_id': 1, 'ca': 30, 'fe': 70},
            {'id': 30, 'name': 'Research Methodology', 'code': 'PRF410130', 'total_credit': 3, 'theory_credit': 3, 'practical_credit': 0, 'level': 7, 'programs_id': 1, 'ca': 60, 'fe': 40},
            {'id': 31, 'name': 'Software Measurement Metrics', 'code': 'PRO410230', 'total_credit': 3, 'theory_credit': 2, 'practical_credit': 1, 'level': 7, 'programs_id': 1, 'ca': 50, 'fe': 50},
            {'id': 32, 'name': 'Final Year Software Engineering Research Project Part I', 'code': 'PRO430130', 'total_credit': 3, 'theory_credit': 0, 'practical_credit': 3, 'level': 7, 'programs_id': 1, 'ca': 100, 'fe': 0},

            # Year 4 Semester 2 (8th Semester)
            {'id': 33, 'name': 'Japanese Language Level VII', 'code': 'PRF420120', 'total_credit': 2, 'theory_credit': 2, 'practical_credit': 0, 'level': 8, 'programs_id': 1, 'ca': 30, 'fe': 70},
            {'id': 34, 'name': 'Final Year Software Engineering Research Project Part II', 'code': 'PRO430150', 'total_credit': 5, 'theory_credit': 0, 'practical_credit': 5, 'level': 8, 'programs_id': 1, 'ca': 100, 'fe': 0},
            {'id': 35, 'name': 'Human Computer Interaction and UX Engineering', 'code': 'DES420130', 'total_credit': 3, 'theory_credit': 2, 'practical_credit': 1, 'level': 8, 'programs_id': 1, 'ca': 50, 'fe': 50},
            {'id': 36, 'name': 'Software Safety and Reliability', 'code': 'QUA420130', 'total_credit': 3, 'theory_credit': 2, 'practical_credit': 1, 'level': 8, 'programs_id': 1, 'ca': 40, 'fe': 60}
        ]
        for subj_data in subjects_data:
            Subjects.objects.create(**subj_data)

    def create_courses(self):
        """Create courses for completed semesters"""
        courses_data = [
            # First Semester Courses
            {'id': 1, 'semesters_id': 1, 'subjects_id': 1},  # Japanese Language I
            {'id': 2, 'semesters_id': 1, 'subjects_id': 2},  # Computer Fundamentals
            {'id': 3, 'semesters_id': 1, 'subjects_id': 3},  # Programming Fundamentals
            {'id': 4, 'semesters_id': 1, 'subjects_id': 4},  # Technical Writing
            {'id': 5, 'semesters_id': 1, 'subjects_id': 5},  # Mathematics I
            
            # Second Semester Courses
            {'id': 6, 'semesters_id': 2, 'subjects_id': 6},  # Japanese Language II
            {'id': 7, 'semesters_id': 2, 'subjects_id': 7},  # Database Systems
            {'id': 8, 'semesters_id': 2, 'subjects_id': 8},  # Web Programming
            {'id': 9, 'semesters_id': 2, 'subjects_id': 9},  # Mathematics II
            
            # Third Semester Courses
            {'id': 10, 'semesters_id': 3, 'subjects_id': 10},  # Data Structures
            {'id': 11, 'semesters_id': 3, 'subjects_id': 11},  # Software Architecture
            {'id': 12, 'semesters_id': 3, 'subjects_id': 12},  # Visual Programming
            {'id': 13, 'semesters_id': 3, 'subjects_id': 13},  # Mathematics III

            # Fourth Semester (Current)
            {'id': 14, 'semesters_id': 4, 'subjects_id': 14},  # Japanese IV
            {'id': 15, 'semesters_id': 4, 'subjects_id': 15},  # Advanced Database
            {'id': 16, 'semesters_id': 4, 'subjects_id': 16},  # Computer Architecture
            {'id': 17, 'semesters_id': 4, 'subjects_id': 17},  # Statistics I
        ]
        
        for course_data in courses_data:
            Courses.objects.create(**course_data)

    def create_courses_batches(self):
        """Create course-batch associations for SE01"""
        cb_data = [
            # First Semester
            {'id': 1, 'courses_id': 1, 'batches_id': 1, 'status': 1},  # Japanese I - Completed
            {'id': 2, 'courses_id': 2, 'batches_id': 1, 'status': 1},  # Computer Fundamentals - Completed
            {'id': 3, 'courses_id': 3, 'batches_id': 1, 'status': 1},  # Programming Fundamentals - Completed
            {'id': 4, 'courses_id': 4, 'batches_id': 1, 'status': 1},  # Technical Writing - Completed
            {'id': 5, 'courses_id': 5, 'batches_id': 1, 'status': 1},  # Mathematics I - Completed
            
            # Second Semester
            {'id': 6, 'courses_id': 6, 'batches_id': 1, 'status': 1},  # Japanese II - Completed
            {'id': 7, 'courses_id': 7, 'batches_id': 1, 'status': 1},  # Database Systems - Completed
            {'id': 8, 'courses_id': 8, 'batches_id': 1, 'status': 1},  # Web Programming - Completed
            {'id': 9, 'courses_id': 9, 'batches_id': 1, 'status': 1},  # Mathematics II - Completed
            
            # Third Semester
            {'id': 10, 'courses_id': 10, 'batches_id': 1, 'status': 1},  # Data Structures - Completed
            {'id': 11, 'courses_id': 11, 'batches_id': 1, 'status': 1},  # Software Architecture - Completed
            {'id': 12, 'courses_id': 12, 'batches_id': 1, 'status': 1},  # Visual Programming - Completed
            {'id': 13, 'courses_id': 13, 'batches_id': 1, 'status': 1},  # Mathematics III - Completed

             # Fourth Semester (Current - status: 0)
            {'id': 14, 'courses_id': 14, 'batches_id': 1, 'status': 0},  # Japanese IV
            {'id': 15, 'courses_id': 15, 'batches_id': 1, 'status': 0},  # Advanced Database
            {'id': 16, 'courses_id': 16, 'batches_id': 1, 'status': 0},  # Computer Architecture
            {'id': 17, 'courses_id': 17, 'batches_id': 1, 'status': 0},  # Statistics I

        ]
        
        for cb in cb_data:
            CoursesBatches.objects.create(**cb)

    def create_students(self):
        """Create student records"""
        students_data = [
            {'id': 1, 'index_no': 'UGC0122033', 'name': 'Avishka Udara', 'auth_user_id': 15, 'batches_id': 1},
            {'id': 2, 'index_no': 'UGC0122030', 'name': 'Sasindu Jayawardana', 'auth_user_id': 16, 'batches_id': 1},
        ]
        
        for student_data in students_data:
            Students.objects.create(**student_data)
    
    def create_courses_student(self):
        """Create course enrollments with final marks for Sasindu"""
        enrollments_data = [
            # First Semester
            {'enroll_id': 1, 'marks': 14.67, 'students_id': 2, 'courses_id': 1, 'level': 1},  # Japanese I
            {'enroll_id': 2, 'marks': 88.2, 'students_id': 2, 'courses_id': 2, 'level': 1},  # Computer Fundamentals
            {'enroll_id': 3, 'marks': 86.4, 'students_id': 2, 'courses_id': 3, 'level': 1},  # Programming Fundamentals
            {'enroll_id': 4, 'marks': 90.0, 'students_id': 2, 'courses_id': 4, 'level': 1},  # Technical Writing
            {'enroll_id': 5, 'marks': 82.5, 'students_id': 2, 'courses_id': 5, 'level': 1},  # Mathematics I
            
            # Second Semester
            {'enroll_id': 6, 'marks': 84.8, 'students_id': 2, 'courses_id': 6, 'level': 2},  # Japanese II
            {'enroll_id': 7, 'marks': 86.2, 'students_id': 2, 'courses_id': 7, 'level': 2},  # Database Systems
            {'enroll_id': 8, 'marks': 88.5, 'students_id': 2, 'courses_id': 8, 'level': 2},  # Web Programming
            {'enroll_id': 9, 'marks': 83.0, 'students_id': 2, 'courses_id': 9, 'level': 2},  # Mathematics II
            
            # Third Semester
            {'enroll_id': 10, 'marks': 85.5, 'students_id': 2, 'courses_id': 10, 'level': 3},  # Data Structures
            {'enroll_id': 11, 'marks': 87.2, 'students_id': 2, 'courses_id': 11, 'level': 3},  # Data StructuresSoftware Architecture
            {'enroll_id': 12, 'marks': 89.0, 'students_id': 2, 'courses_id': 12, 'level': 3},  # Data StructuresVisual Programming
            {'enroll_id': 13, 'marks': 84.5, 'students_id': 2, 'courses_id': 13, 'level': 3},  # Data StructuresMathematics III
            {'enroll_id': 14, 'marks': 80.67, 'students_id': 2, 'courses_id': 1, 'level': 3}, 
        ]
        
        for enroll_data in enrollments_data:
            CoursesStudent.objects.create(**enroll_data)

    def create_criterias(self):
        """Create comprehensive assessment criteria for all completed courses"""
        criteria_data = [
            # Japanese Language Level I (30:70 ratio)
            {'id': 1, 'nature': 'Quiz', 'type': 'CA', 'name': 'Mid-Term Test', 'weights': 60, 'courses_id': 1, 'max_mark': 100},
            {'id': 2, 'nature': 'Quiz', 'type': 'CA', 'name': 'Oral Presentation', 'weights': 40, 'courses_id': 1, 'max_mark': 100},
            {'id': 3, 'nature': 'MCQ', 'type': 'FE', 'name': 'Final Written', 'weights': 70, 'courses_id': 1, 'max_mark': 100},
            {'id': 4, 'nature': 'Essay', 'type': 'FE', 'name': 'Final Oral', 'weights': 30, 'courses_id': 1, 'max_mark': 100},

            # Computer Fundamentals (40:60 ratio)
            {'id': 5, 'nature': 'Quiz', 'type': 'CA', 'name': 'Theory Quiz', 'weights': 50, 'courses_id': 2, 'max_mark': 100},
            {'id': 6, 'nature': 'Quiz', 'type': 'CA', 'name': 'Lab Assessment', 'weights': 50, 'courses_id': 2, 'max_mark': 100},
            {'id': 7, 'nature': 'MCQ', 'type': 'FE', 'name': 'Final Theory', 'weights': 35, 'courses_id': 2, 'max_mark': 100},
            {'id': 8, 'nature': 'Essay', 'type': 'FE', 'name': 'Final Practical', 'weights': 65, 'courses_id': 2, 'max_mark': 100},

            # Programming Fundamentals (50:50 ratio)
            {'id': 9, 'nature': 'Quiz', 'type': 'CA', 'name': 'Programming Quiz', 'weights': 25, 'courses_id': 3, 'max_mark': 100},
            {'id': 10, 'nature': 'Quiz', 'type': 'CA', 'name': 'Programming Assignment', 'weights': 50, 'courses_id': 3, 'max_mark': 100},
            {'id': 11, 'nature': 'Quiz', 'type': 'CA', 'name': 'Mini Project', 'weights': 25, 'courses_id': 3, 'max_mark': 100},
            {'id': 12, 'nature': 'MCQ', 'type': 'FE', 'name': 'Final Theory', 'weights': 50, 'courses_id': 3, 'max_mark': 100},
            {'id': 13, 'nature': 'Essay', 'type': 'FE', 'name': 'Final Practical', 'weights': 50, 'courses_id': 3, 'max_mark': 100},

            # Technical Writing (60:40 ratio)
            {'id': 14, 'nature': 'Quiz', 'type': 'CA', 'name': 'Writing Assignment 1', 'weights': 50, 'courses_id': 4, 'max_mark': 100},
            {'id': 15, 'nature': 'Quiz', 'type': 'CA', 'name': 'Documentation Project', 'weights': 25, 'courses_id': 4, 'max_mark': 100},
            {'id': 16, 'nature': 'Quiz', 'type': 'CA', 'name': 'Oral Presentation', 'weights': 25, 'courses_id': 4, 'max_mark': 100},
            {'id': 17, 'nature': 'MCQ', 'type': 'FE', 'name': 'Final Assessment', 'weights': 100, 'courses_id': 4, 'max_mark': 100},

            # Mathematics I for SE (30:70 ratio)
            {'id': 18, 'nature': 'Quiz', 'type': 'CA', 'name': 'Math Quiz 1', 'weights': 55, 'courses_id': 5, 'max_mark': 100},
            {'id': 19, 'nature': 'Quiz', 'type': 'CA', 'name': 'Problem Sets', 'weights': 45, 'courses_id': 5, 'max_mark': 100},
            {'id': 20, 'nature': 'MCQ', 'type': 'FE', 'name': 'Final Exam', 'weights': 100, 'courses_id': 5, 'max_mark': 100},

            # Japanese Language Level II (30:70 ratio)
            {'id': 21, 'nature': 'Quiz', 'type': 'CA', 'name': 'Mid-Term Test', 'weights': 45, 'courses_id': 6, 'max_mark': 100},
            {'id': 22, 'nature': 'Quiz', 'type': 'CA', 'name': 'Oral Presentation', 'weights': 55, 'courses_id': 6, 'max_mark': 100},
            {'id': 23, 'nature': 'MCQ', 'type': 'FE', 'name': 'Final Written', 'weights': 40, 'courses_id': 6, 'max_mark': 100},
            {'id': 24, 'nature': 'Essay', 'type': 'FE', 'name': 'Final Oral', 'weights': 60, 'courses_id': 6, 'max_mark': 100},

            # Database Systems (40:60 ratio)
            {'id': 25, 'nature': 'Quiz', 'type': 'CA', 'name': 'Theory Quiz', 'weights': 75, 'courses_id': 7, 'max_mark': 100},
            {'id': 26, 'nature': 'Quiz', 'type': 'CA', 'name': 'Database Project', 'weights': 25, 'courses_id': 7, 'max_mark': 100},
            {'id': 27, 'nature': 'MCQ', 'type': 'FE', 'name': 'Final Theory', 'weights': 55, 'courses_id': 7, 'max_mark': 100},
            {'id': 28, 'nature': 'Essay', 'type': 'FE', 'name': 'Final Practical', 'weights': 45, 'courses_id': 7, 'max_mark': 100},

            # Web Programming (50:50 ratio)
            {'id': 29, 'nature': 'Quiz', 'type': 'CA', 'name': 'Coding Quiz', 'weights': 25, 'courses_id': 8, 'max_mark': 100},
            {'id': 30, 'nature': 'Quiz', 'type': 'CA', 'name': 'Web Project', 'weights': 25, 'courses_id': 8, 'max_mark': 100},
            {'id': 31, 'nature': 'Quiz', 'type': 'CA', 'name': 'Implementation Task', 'weights': 50, 'courses_id': 8, 'max_mark': 100},
            {'id': 32, 'nature': 'MCQ', 'type': 'FE', 'name': 'Final Theory', 'weights': 75, 'courses_id': 8, 'max_mark': 100},
            {'id': 33, 'nature': 'Essay', 'type': 'FE', 'name': 'Final Practical', 'weights': 25, 'courses_id': 8, 'max_mark': 100},

            # Mathematics II for SE (30:70 ratio)
            {'id': 34, 'nature': 'Quiz', 'type': 'CA', 'name': 'Math Quiz', 'weights': 45, 'courses_id': 9, 'max_mark': 100},
            {'id': 35, 'nature': 'Quiz', 'type': 'CA', 'name': 'Problem Sets', 'weights': 55, 'courses_id': 9, 'max_mark': 100},
            {'id': 36, 'nature': 'MCQ', 'type': 'FE', 'name': 'Final Exam', 'weights': 100, 'courses_id': 9, 'max_mark': 100},

            # Data Structures and Algorithms (40:60 ratio)
            {'id': 37, 'nature': 'Quiz', 'type': 'CA', 'name': 'Theory Quiz', 'weights': 45, 'courses_id': 10, 'max_mark': 100},
            {'id': 38, 'nature': 'Quiz', 'type': 'CA', 'name': 'Implementation Project', 'weights': 55, 'courses_id': 10, 'max_mark': 100},
            {'id': 39, 'nature': 'MCQ', 'type': 'FE', 'name': 'Final Theory', 'weights': 35, 'courses_id': 10, 'max_mark': 100},
            {'id': 40, 'nature': 'Essay', 'type': 'FE', 'name': 'Final Practical', 'weights': 65, 'courses_id': 10, 'max_mark': 100},

            # Software Architecture and Design (50:50 ratio)
            {'id': 41, 'nature': 'Quiz', 'type': 'CA', 'name': 'Architecture Quiz', 'weights': 25, 'courses_id': 11, 'max_mark': 100},
            {'id': 42, 'nature': 'Quiz', 'type': 'CA', 'name': 'Design Project', 'weights': 25, 'courses_id': 11, 'max_mark': 100},
            {'id': 43, 'nature': 'Quiz', 'type': 'CA', 'name': 'Case Study', 'weights': 50, 'courses_id': 11, 'max_mark': 100},
            {'id': 44, 'nature': 'MCQ', 'type': 'FE', 'name': 'Final Theory', 'weights': 30, 'courses_id': 11, 'max_mark': 100},
            {'id': 45, 'nature': 'Essay', 'type': 'FE', 'name': 'Final Design Implementation', 'weights': 70, 'courses_id': 11, 'max_mark': 100},

            # Visual Application Programming (50:50 ratio)
            {'id': 46, 'nature': 'Quiz', 'type': 'CA', 'name': 'Programming Quiz', 'weights': 25, 'courses_id': 12, 'max_mark': 100},
            {'id': 47, 'nature': 'Quiz', 'type': 'CA', 'name': 'GUI Project', 'weights': 25, 'courses_id': 12, 'max_mark': 100},
            {'id': 48, 'nature': 'Quiz', 'type': 'CA', 'name': 'Implementation Task', 'weights': 50, 'courses_id': 12, 'max_mark': 100},
            {'id': 49, 'nature': 'MCQ', 'type': 'FE', 'name': 'Final Theory', 'weights': 75, 'courses_id': 12, 'max_mark': 100},
            {'id': 50, 'nature': 'Essay', 'type': 'FE', 'name': 'Final Practical', 'weights': 25, 'courses_id': 12, 'max_mark': 100},

            # Mathematics III for SE (30:70 ratio)
            {'id': 51, 'nature': 'Quiz', 'type': 'CA', 'name': 'Math Quiz', 'weights': 55, 'courses_id': 13, 'max_mark': 100},
            {'id': 52, 'nature': 'Quiz', 'type': 'CA', 'name': 'Problem Sets', 'weights': 45, 'courses_id': 13, 'max_mark': 100},
            {'id': 53, 'nature': 'MCQ', 'type': 'FE', 'name': 'Final Exam', 'weights': 100, 'courses_id': 13, 'max_mark': 100},

             # statistic I for SE (30:70 ratio)
            {'id': 54, 'nature': 'Quiz', 'type': 'CA', 'name': 'CA 1', 'weights': 25, 'courses_id': 17, 'max_mark': 100},
            {'id': 55, 'nature': 'Quiz', 'type': 'CA', 'name': 'CA 2', 'weights': 75, 'courses_id': 17, 'max_mark': 100},
            {'id': 56, 'nature': 'MCQ', 'type': 'FE', 'name': 'Final Theory', 'weights': 30, 'courses_id': 17, 'max_mark': 100},
            {'id': 57, 'nature': 'Essay', 'type': 'FE', 'name': 'Final Quiz', 'weights': 70, 'courses_id': 17, 'max_mark': 100},

        ]
        
        for crit_data in criteria_data:
            Criterias.objects.create(**crit_data)

    def create_students_criterias(self):
        """Create comprehensive assessment marks for Sasindu across all completed courses"""
        sc_data = [
            # Japanese Language Level I
            {'id': 1, 'students_id': 2, 'criterias_id': 1, 'mark': '10'},   # Mid-Term Test
            {'id': 2, 'students_id': 2, 'criterias_id': 2, 'mark': '18'},   # Oral Presentation
            {'id': 3, 'students_id': 2, 'criterias_id': 3, 'mark': '15'},   # Final Written
            {'id': 4, 'students_id': 2, 'criterias_id': 4, 'mark': '16'},   # Final Oral

            # Computer Fundamentals
            {'id': 5, 'students_id': 2, 'criterias_id': 5, 'mark': '90'},   # Theory Quiz
            {'id': 6, 'students_id': 2, 'criterias_id': 6, 'mark': '87'},   # Lab Assessment
            {'id': 7, 'students_id': 2, 'criterias_id': 7, 'mark': '88'},   # Final Theory
            {'id': 8, 'students_id': 2, 'criterias_id': 8, 'mark': '89'},   # Final Practical

            # Programming Fundamentals
            {'id': 9, 'students_id': 2, 'criterias_id': 9, 'mark': '88'},   # Programming Quiz
            {'id': 10, 'students_id': 2, 'criterias_id': 10, 'mark': '92'}, # Programming Assignment
            {'id': 11, 'students_id': 2, 'criterias_id': 11, 'mark': '89'}, # Mini Project
            {'id': 12, 'students_id': 2, 'criterias_id': 12, 'mark': '85'}, # Final Theory
            {'id': 13, 'students_id': 2, 'criterias_id': 13, 'mark': '88'}, # Final Practical

            # Technical Writing
            {'id': 14, 'students_id': 2, 'criterias_id': 14, 'mark': '92'}, # Writing Assignment 1
            {'id': 15, 'students_id': 2, 'criterias_id': 15, 'mark': '90'}, # Documentation Project
            {'id': 16, 'students_id': 2, 'criterias_id': 16, 'mark': '88'}, # Oral Presentation
            {'id': 17, 'students_id': 2, 'criterias_id': 17, 'mark': '89'}, # Final Assessment

            # Mathematics I for SE
            {'id': 18, 'students_id': 2, 'criterias_id': 18, 'mark': '84'}, # Math Quiz 1
            {'id': 19, 'students_id': 2, 'criterias_id': 19, 'mark': '82'}, # Problem Sets
            {'id': 20, 'students_id': 2, 'criterias_id': 20, 'mark': '83'}, # Final Exam

            # Japanese Language Level II
            {'id': 21, 'students_id': 2, 'criterias_id': 21, 'mark': '86'}, # Mid-Term Test
            {'id': 22, 'students_id': 2, 'criterias_id': 22, 'mark': '85'}, # Oral Presentation
            {'id': 23, 'students_id': 2, 'criterias_id': 23, 'mark': '84'}, # Final Written
            {'id': 24, 'students_id': 2, 'criterias_id': 24, 'mark': '85'}, # Final Oral

            # Database Systems
            {'id': 25, 'students_id': 2, 'criterias_id': 25, 'mark': '85'}, # Theory Quiz
            {'id': 26, 'students_id': 2, 'criterias_id': 26, 'mark': '90'}, # Database Project
            {'id': 27, 'students_id': 2, 'criterias_id': 27, 'mark': '86'}, # Final Theory
            {'id': 28, 'students_id': 2, 'criterias_id': 28, 'mark': '88'}, # Final Practical

            # Web Programming
            {'id': 29, 'students_id': 2, 'criterias_id': 29, 'mark': '90'}, # Coding Quiz
            {'id': 30, 'students_id': 2, 'criterias_id': 30, 'mark': '89'}, # Web Project
            {'id': 31, 'students_id': 2, 'criterias_id': 31, 'mark': '88'}, # Implementation Task
            {'id': 32, 'students_id': 2, 'criterias_id': 32, 'mark': '87'}, # Final Theory
            {'id': 33, 'students_id': 2, 'criterias_id': 33, 'mark': '89'}, # Final Practical

            # Mathematics II for SE
            {'id': 34, 'students_id': 2, 'criterias_id': 34, 'mark': '84'}, # Math Quiz
            {'id': 35, 'students_id': 2, 'criterias_id': 35, 'mark': '83'}, # Problem Sets
            {'id': 36, 'students_id': 2, 'criterias_id': 36, 'mark': '82'}, # Final Exam

            # Data Structures and Algorithms
            {'id': 37, 'students_id': 2, 'criterias_id': 37, 'mark': '87'}, # Theory Quiz
            {'id': 38, 'students_id': 2, 'criterias_id': 38, 'mark': '85'}, # Implementation Project
            {'id': 39, 'students_id': 2, 'criterias_id': 39, 'mark': '86'}, # Final Theory
            {'id': 40, 'students_id': 2, 'criterias_id': 40, 'mark': '84'}, # Final Practical

            # Software Architecture and Design
            {'id': 41, 'students_id': 2, 'criterias_id': 41, 'mark': '88'}, # Architecture Quiz
            {'id': 42, 'students_id': 2, 'criterias_id': 42, 'mark': '89'}, # Design Project
            {'id': 43, 'students_id': 2, 'criterias_id': 43, 'mark': '86'}, # Case Study
            {'id': 44, 'students_id': 2, 'criterias_id': 44, 'mark': '87'}, # Final Theory
            {'id': 45, 'students_id': 2, 'criterias_id': 45, 'mark': '88'}, # Final Design Implementation

            # Visual Application Programming
            {'id': 46, 'students_id': 2, 'criterias_id': 46, 'mark': '90'}, # Programming Quiz
            {'id': 47, 'students_id': 2, 'criterias_id': 47, 'mark': '89'}, # GUI Project
            {'id': 48, 'students_id': 2, 'criterias_id': 48, 'mark': '88'}, # Implementation Task
            {'id': 49, 'students_id': 2, 'criterias_id': 49, 'mark': '89'}, # Final Theory
            {'id': 50, 'students_id': 2, 'criterias_id': 50, 'mark': '90'}, # Final Practical

            # Mathematics III for SE
            {'id': 51, 'students_id': 2, 'criterias_id': 51, 'mark': '85'}, # Math Quiz
            {'id': 52, 'students_id': 2, 'criterias_id': 52, 'mark': '84'}, # Problem Sets
            {'id': 53, 'students_id': 2, 'criterias_id': 53, 'mark': '85'}, # Final Exam
        ]
        
        for sc in sc_data:
            StudentsCriterias.objects.create(**sc)

    def create_results(self):
        """Create final results with grades for Sasindu"""
        results_data = [
            # First Semester
            {'id': 1, 'grade': 'E', 's_grade': 'E', 'courses_id': 1, 'students_id': 2},  # Japanese I
            {'id': 2, 'grade': 'A', 's_grade': 'A', 'courses_id': 2, 'students_id': 2},  # Computer Fundamentals
            {'id': 3, 'grade': 'A', 's_grade': 'A', 'courses_id': 3, 'students_id': 2},  # Programming Fundamentals
            {'id': 4, 'grade': 'A+', 's_grade': 'A+', 'courses_id': 4, 'students_id': 2},  # Technical Writing
            {'id': 5, 'grade': 'A-', 's_grade': 'A-', 'courses_id': 5, 'students_id': 2},  # Mathematics I
            
            # Second Semester
            {'id': 6, 'grade': 'A', 's_grade': 'A', 'courses_id': 6, 'students_id': 2},  # Japanese II
            {'id': 7, 'grade': 'A', 's_grade': 'A', 'courses_id': 7, 'students_id': 2},  # Database Systems
            {'id': 8, 'grade': 'A', 's_grade': 'A', 'courses_id': 8, 'students_id': 2},  # Web Programming
            {'id': 9, 'grade': 'A-', 's_grade': 'A-', 'courses_id': 9, 'students_id': 2},  # Mathematics II
            
            # Third Semester
            {'id': 10, 'grade': 'A', 's_grade': 'A', 'courses_id': 10, 'students_id': 2},  # Data Structures
            {'id': 11, 'grade': 'A', 's_grade': 'A', 'courses_id': 11, 'students_id': 2},  # Software Architecture
            {'id': 12, 'grade': 'A', 's_grade': 'A', 'courses_id': 12, 'students_id': 2},  # Visual Programming
            {'id': 13, 'grade': 'A', 's_grade': 'A', 'courses_id': 13, 'students_id': 2},  # Mathematics III
            {'id': 14, 'grade': 'C', 's_grade': 'C', 'courses_id': 1, 'students_id': 2},  # Japanese I
        ]
        
        for result_data in results_data:
            Results.objects.create(**result_data)

