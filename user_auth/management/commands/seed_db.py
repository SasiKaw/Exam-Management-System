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
            {'id': 5, 'name': 'HOD'}
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
                'id': 20,
                'username': 'Oneli',
                'password': 'pbkdf2_sha256$720000$838svvdGEAmfc64DfyWxAC$uI5gEsPkhz/3MFyCA6ecKZS57OEvoMyxNb0PDiGRAaw=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2024-12-18 15:50:51.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 22,
                'username': 'Bashini',
                'password': 'pbkdf2_sha256$720000$y7RmNM86Owx0QDAjaV6g5h$XFiflvrrNRl3pbPfH2sVDKoq2HRCeuW8IPQahT8Oh18=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2024-12-19 03:41:10.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 27,
                'username': 'Akindu',
                'password': 'pbkdf2_sha256$720000$M1ugtUWb0ArpiYvyxGUxSZ$Y55UqPGC8yTtety808AeiRPuUFzuvzyYHxn2fn5BPhc=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2024-12-19 11:32:52.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 34,
                'username': 'Piyumi',
                'password': 'pbkdf2_sha256$720000$orvt0vI4zmZqkKKQ0i5Z29$rVsJMJNNxlAVcMTOnIlLL+cn47xMHzYOUz4xOFKLXYk=',
                'is_active': False,
                'date_joined': make_aware(datetime.datetime.strptime('2024-12-19 20:15:34.848084', '%Y-%m-%d %H:%M:%S.%f'))
            }
        ]
        
        for user_data in users_data:
            User.objects.create(**user_data)

    def create_user_groups(self):
        """Assign users to groups"""
        assignments = [
            {'user_id': 15, 'group_id': 3},  # Avishka -> Student
            {'user_id': 16, 'group_id': 3},  # Sasindu -> Student
            {'user_id': 18, 'group_id': 4},  # Janith -> Lecturer
            {'user_id': 20, 'group_id': 3},  # Oneli -> Student
            {'user_id': 22, 'group_id': 5},  # Bashini -> HOD
            {'user_id': 27, 'group_id': 3},  # Akindu -> Student
            {'user_id': 34, 'group_id': 3},  # Piyumi -> Student
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
        """Create batches"""
        batches_data = [
            {'id': 1, 'name': 'SE01', 'programs_id': 1, 'current_level': '4', 'is_active': 1},
            {'id': 2, 'name': 'SE02', 'programs_id': 1, 'current_level': '3', 'is_active': 1},
            {'id': 3, 'name': 'SE03', 'programs_id': 1, 'current_level': '2', 'is_active': 1},
            {'id': 4, 'name': 'SE04', 'programs_id': 1, 'current_level': '2', 'is_active': 1},
            {'id': 5, 'name': 'SE05', 'programs_id': 1, 'current_level': '4', 'is_active': 1},
            {'id': 9, 'name': 'UOG01', 'programs_id': 2, 'current_level': '8', 'is_active': 1},
            {'id': 10, 'name': 'UOG02', 'programs_id': 2, 'current_level': '7', 'is_active': 1},
            {'id': 11, 'name': 'UOG03', 'programs_id': 2, 'current_level': '7', 'is_active': 1},
            {'id': 12, 'name': 'UOG04', 'programs_id': 2, 'current_level': '9', 'is_active': 1},
            {'id': 13, 'name': 'UOG05', 'programs_id': 2, 'current_level': '10', 'is_active': 1},
            {'id': 14, 'name': 'UOG06', 'programs_id': 2, 'current_level': '10', 'is_active': 1},
            {'id': 15, 'name': 'UOG07', 'programs_id': 2, 'current_level': '10', 'is_active': 1},
            {'id': 16, 'name': 'UOG08', 'programs_id': 2, 'current_level': '10', 'is_active': 1},
            {'id': 17, 'name': 'UOG09', 'programs_id': 2, 'current_level': '11', 'is_active': 1},
            {'id': 18, 'name': 'UOG10', 'programs_id': 2, 'current_level': '11', 'is_active': 1},
            {'id': 19, 'name': 'UOG11', 'programs_id': 2, 'current_level': '11', 'is_active': 1}
        ]
        
        for batch_data in batches_data:
            Batches.objects.create(**batch_data)

    def create_semesters(self):
        """Create semesters"""
        Semesters.objects.create(
            id=1,
            start_date='2025-03-01',
            end_date='2025-06-14'
        )

    def create_subjects(self):
        """Create subjects"""
        subjects_data = [
            {'id': 1, 'name': 'Programming Fundamentals', 'code': 'PF001', 'total_credit': 3, 'theory_credit': 1, 'practical_credit': 2, 'level': 1, 'programs_id': 1, 'ca': 50, 'fe': 50},
            {'id': 2, 'name': 'Database Systems', 'code': 'DBS01', 'total_credit': 3, 'theory_credit': 2, 'practical_credit': 1, 'level': 1, 'programs_id': 1, 'ca': 30, 'fe': 70},
            {'id': 3, 'name': 'Web Development', 'code': 'WD001', 'total_credit': 2, 'theory_credit': 1, 'practical_credit': 1, 'level': 2, 'programs_id': 1, 'ca': 40, 'fe': 60},
            {'id': 4, 'name': 'Software Architecture', 'code': 'SA001', 'total_credit': 2, 'theory_credit': 1, 'practical_credit': 1, 'level': 2, 'programs_id': 1, 'ca': 50, 'fe': 50},
            {'id': 5, 'name': 'Advanced Programming', 'code': 'AP001', 'total_credit': 3, 'theory_credit': 1, 'practical_credit': 2, 'level': 3, 'programs_id': 1, 'ca': 40, 'fe': 60},
            {'id': 6, 'name': 'Software Project Management', 'code': 'SP001', 'total_credit': 2, 'theory_credit': 1, 'practical_credit': 1, 'level': 3, 'programs_id': 1, 'ca': 50, 'fe': 50},
            {'id': 7, 'name': 'Mathematics', 'code': 'M001', 'total_credit': 2, 'theory_credit': 1, 'practical_credit': 1, 'level': 4, 'programs_id': 1, 'ca': 30, 'fe': 70},
            {'id': 8, 'name': 'Physics', 'code': 'P001', 'total_credit': 3, 'theory_credit': 1, 'practical_credit': 2, 'level': 4, 'programs_id': 1, 'ca': 40, 'fe': 60},
            {'id': 9, 'name': 'Web Programming', 'code': 'WP001', 'total_credit': 3, 'theory_credit': 1, 'practical_credit': 2, 'level': 4, 'programs_id': 1, 'ca': 50, 'fe': 50},
            {'id': 10, 'name': 'IoT', 'code': 'IOT001', 'total_credit': 3, 'theory_credit': 1, 'practical_credit': 2, 'level': 3, 'programs_id': 2, 'ca': 40, 'fe': 60},
            {'id': 11, 'name': 'Cyber Security', 'code': 'CYS0001', 'total_credit': 3, 'theory_credit': 1, 'practical_credit': 2, 'level': 3, 'programs_id': 2, 'ca': 30, 'fe': 70}
        ]
        
        for subj_data in subjects_data:
            Subjects.objects.create(**subj_data)

    def create_courses(self):
        """Create courses"""
        courses_data = [
            {'id': 1, 'semesters_id': 1, 'subjects_id': 7},
            {'id': 2, 'semesters_id': 1, 'subjects_id': 8},
            {'id': 3, 'semesters_id': 1, 'subjects_id': 9}
        ]
        
        for course_data in courses_data:
            Courses.objects.create(**course_data)

    def create_courses_batches(self):
        """Create course-batch associations"""
        cb_data = [
            {'id': 1, 'courses_id': 1, 'batches_id': 1, 'status': 0},
            {'id': 2, 'courses_id': 2, 'batches_id': 1, 'status': 0},
            {'id': 3, 'courses_id': 3, 'batches_id': 1, 'status': 0}
        ]
        
        for cb in cb_data:
            CoursesBatches.objects.create(**cb)

    def create_students(self):
        """Create student records"""
        students_data = [
            {'id': 1, 'index_no': 'UGC0122033', 'name': 'Avishka Udara', 'auth_user_id': 15, 'batches_id': 1},
            {'id': 2, 'index_no': 'UGC0122030', 'name': 'Sasindu Jayawardana', 'auth_user_id': 16, 'batches_id': 1},
            {'id': 3, 'index_no': 'UGC0122034', 'name': 'Oneli Jayodha', 'auth_user_id': 20, 'batches_id': 1},
            {'id': 4, 'index_no': 'UGC0122035', 'name': 'Sehan Rajapaksha', 'auth_user_id': 21, 'batches_id': 1},
            {'id': 5, 'index_no': 'UGC0122036', 'name': 'Akindu Venul', 'auth_user_id': 27, 'batches_id': 1},
            {'id': 6, 'index_no': 'UGC0122037', 'name': 'Piyumi Natasha', 'auth_user_id': 34, 'batches_id': 1}
        ]
        
        for student_data in students_data:
            Students.objects.create(**student_data)
    
    def create_courses_student(self):
        """Create course enrollments"""
        enrollments_data = [
            {'enroll_id': 1, 'marks': 79, 'students_id': 1, 'courses_id': 1},
            {'enroll_id': 2, 'marks': 85, 'students_id': 2, 'courses_id': 1},
            {'enroll_id': 3, 'marks': 77, 'students_id': 3, 'courses_id': 1},
            {'enroll_id': 4, 'marks': 91, 'students_id': 4, 'courses_id': 1},
            {'enroll_id': 5, 'marks': 90, 'students_id': 5, 'courses_id': 1},
            {'enroll_id': 6, 'marks': 82, 'students_id': 6, 'courses_id': 1}
        ]
        
        for enroll_data in enrollments_data:
            CoursesStudent.objects.create(**enroll_data)

    def create_criterias(self):
        """Create assessment criteria"""
        criteria_data = [
            {'id': 1, 'nature': 'In class', 'type': 'CA', 'name': 'CA 1', 'weights': 40, 'courses_id': 1, 'max_mark': 100},
            {'id': 2, 'nature': 'In class', 'type': 'CA', 'name': 'CA 2', 'weights': 60, 'courses_id': 1, 'max_mark': 100},
            {'id': 3, 'nature': 'Essay', 'type': 'FE', 'name': 'Q 1', 'weights': 20, 'courses_id': 1, 'max_mark': 100},
            {'id': 4, 'nature': 'Essay', 'type': 'FE', 'name': 'Q 2', 'weights': 20, 'courses_id': 1, 'max_mark': 100},
            {'id': 5, 'nature': 'Essay', 'type': 'FE', 'name': 'Q 3', 'weights': 20, 'courses_id': 1, 'max_mark': 100},
            {'id': 6, 'nature': 'Essay', 'type': 'FE', 'name': 'Q 4', 'weights': 20, 'courses_id': 1, 'max_mark': 100},
            {'id': 7, 'nature': 'Essay', 'type': 'FE', 'name': 'Q 5', 'weights': 20, 'courses_id': 1, 'max_mark': 100},

        ]
        
        for crit_data in criteria_data:
            Criterias.objects.create(**crit_data)

    def create_students_criterias(self):
        """Create student criteria records"""
        sc_data = [
            {'id': 1, 'students_id': 1, 'criterias_id': 1, 'mark': '85'},
            {'id': 2, 'students_id': 1, 'criterias_id': 2, 'mark': '90'},
            {'id': 3, 'students_id': 1, 'criterias_id': 3, 'mark': '75'},
            {'id': 4, 'students_id': 1, 'criterias_id': 4, 'mark': '80'},
            {'id': 5, 'students_id': 1, 'criterias_id': 5, 'mark': '70'},
            {'id': 6, 'students_id': 1, 'criterias_id': 6, 'mark': '65'},
            {'id': 7, 'students_id': 1, 'criterias_id': 7, 'mark': '88'},
            {'id': 8, 'students_id': 2, 'criterias_id': 1, 'mark': '78'},
            {'id': 9, 'students_id': 2, 'criterias_id': 2, 'mark': '82'},
            {'id': 10, 'students_id': 2, 'criterias_id': 3, 'mark': '88'},
            {'id': 11, 'students_id': 2, 'criterias_id': 4, 'mark': '92'},
            {'id': 12, 'students_id': 2, 'criterias_id': 5, 'mark': '85'},
            {'id': 13, 'students_id': 2, 'criterias_id': 6, 'mark': '80'},
            {'id': 14, 'students_id': 2, 'criterias_id': 7, 'mark': '90'},
            {'id': 15, 'students_id': 3, 'criterias_id': 1, 'mark': '65'},
            {'id': 16, 'students_id': 3, 'criterias_id': 2, 'mark': '70'},
            {'id': 17, 'students_id': 3, 'criterias_id': 3, 'mark': '85'},
            {'id': 18, 'students_id': 3, 'criterias_id': 4, 'mark': '88'},
            {'id': 19, 'students_id': 3, 'criterias_id': 5, 'mark': '90'},
            {'id': 20, 'students_id': 3, 'criterias_id': 6, 'mark': '80'},
            {'id': 21, 'students_id': 3, 'criterias_id': 7, 'mark': '75'},
            {'id': 22, 'students_id': 4, 'criterias_id': 1, 'mark': '95'},
            {'id': 23, 'students_id': 4, 'criterias_id': 2, 'mark': '85'},
            {'id': 24, 'students_id': 4, 'criterias_id': 3, 'mark': '80'},
            {'id': 25, 'students_id': 4, 'criterias_id': 4, 'mark': '85'},
            {'id': 26, 'students_id': 4, 'criterias_id': 5, 'mark': '75'},
            {'id': 27, 'students_id': 4, 'criterias_id': 6, 'mark': '90'},
            {'id': 28, 'students_id': 4, 'criterias_id': 7, 'mark': '88'},
            {'id': 29, 'students_id': 5, 'criterias_id': 1, 'mark': '88'},
            {'id': 30, 'students_id': 5, 'criterias_id': 2, 'mark': '92'},
            {'id': 31, 'students_id': 5, 'criterias_id': 3, 'mark': '87'},
            {'id': 32, 'students_id': 5, 'criterias_id': 4, 'mark': '90'},
            {'id': 33, 'students_id': 5, 'criterias_id': 5, 'mark': '84'},
            {'id': 34, 'students_id': 5, 'criterias_id': 6, 'mark': '89'},
            {'id': 35, 'students_id': 5, 'criterias_id': 7, 'mark': '91'},
            {'id': 36, 'students_id': 6, 'criterias_id': 1, 'mark': '76'},
            {'id': 37, 'students_id': 6, 'criterias_id': 2, 'mark': '82'},
            {'id': 38, 'students_id': 6, 'criterias_id': 3, 'mark': '88'},
            {'id': 39, 'students_id': 6, 'criterias_id': 4, 'mark': '84'},
            {'id': 40, 'students_id': 6, 'criterias_id': 5, 'mark': '83'},
            {'id': 41, 'students_id': 6, 'criterias_id': 6, 'mark': '87'},
            {'id': 42, 'students_id': 6, 'criterias_id': 7, 'mark': '89'}
        ]
        
        for sc in sc_data:
            StudentsCriterias.objects.create(**sc)

    def create_results(self):
        """Create results"""
        results_data = [
            {'id': 1, 'grade': 'A+', 's_grade': 'B+', 'courses_id': 1, 'students_id': 1},
            {'id': 2, 'grade': 'A', 's_grade': 'A', 'courses_id': 1, 'students_id': 2},
            {'id': 3, 'grade': 'B', 's_grade': 'B', 'courses_id': 1, 'students_id': 3},
            {'id': 4, 'grade': 'A+', 's_grade': 'A+', 'courses_id': 1, 'students_id': 4},
            {'id': 5, 'grade': 'A+', 's_grade': 'A+', 'courses_id': 1, 'students_id': 5},
            {'id': 6, 'grade': 'B+', 's_grade': 'B+', 'courses_id': 1, 'students_id': 6}
        ]
        
        for result_data in results_data:
            Results.objects.create(**result_data)

