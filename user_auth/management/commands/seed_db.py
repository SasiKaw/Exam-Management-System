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
            self.create_lecturers()
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
            {
                'id': 24,
                'username': 'Oneli',
                'password': 'pbkdf2_sha256$720000$gxIRqlHE4VR4i08aM3RX3b$6LLWxZCosQjph60gE5kc8q92YkBnyHaiiOYZo72SBv4=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2025-02-12 10:20:33.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 25,
                'username': 'Dumindu',
                'password': 'pbkdf2_sha256$720000$wldEzNGp2mDZebaJJ47QGg$e6cKOZuV1Hnft3e63z1pXXW7RJKt7xBFgg5wyhd01s8=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2025-02-12 10:21:12.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 26,
                'username': 'Vindi',
                'password': 'pbkdf2_sha256$720000$J8SO5ZPmKPdUvWuEAP9pTx$sIS5T20VDokYIf7B8R6/kvvTKZ6kby9AkJxsQnYY8VY=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2025-02-12 10:21:40.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 27,
                'username': 'Suneth',
                'password': 'pbkdf2_sha256$720000$mFGRzzJQ4yQbU1eoQTvAIr$Ge62U/MU7BNnJEvIxCGQDqAnSflnxSlSf7za88isMoc=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2025-02-12 10:22:26.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 28,
                'username': 'Oshani',
                'password': 'pbkdf2_sha256$720000$J0Y0KbtVuJOKLjIwUtqhx8$wQE9hNak4EwROCjpcpF49W56e/XzhpEwN2gdVMPMP14=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2025-02-12 10:22:55.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 29,
                'username': 'Sandil',
                'password': 'pbkdf2_sha256$720000$ELdlIeeL841qIiFoEBPkg6$gijxHwsb3Jy42jpsce5KWV6jUJ1qF+SxCnO/g/cT6OE=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2025-02-12 10:23:19.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 30,
                'username': 'Pasindu',
                'password': 'pbkdf2_sha256$720000$jRf3PtF3XbN0CkuD7bPhU0$Bh4GfTIZKndR0THlI42tA4k0A8KW0G3I++bXFbDpyYY=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2025-02-12 10:24:09.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 31,
                'username': 'Mewan',
                'password': 'pbkdf2_sha256$720000$eEV55hc4DChpG3T6UVaw3O$4kkT5ot+fGgsEmHhvhkOYRoS+Rrl23/ndM3uncZPZTU=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2025-02-13 14:02:23.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 32,
                'username': 'Chobodhi',
                'password': 'pbkdf2_sha256$720000$g2Bp3ZO3j6qaxQj2AjtMfa$vlmvHYjhhzAoutrzRapqJlqfCUZzhAiN30wAI9o/sZQ=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2025-02-13 14:02:56.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 33,
                'username': 'Geethika',
                'password': 'pbkdf2_sha256$720000$ijHlXAsMb5CMnOwEfyujdD$KxmOuYD76ylIYg5wR1VVnc5dhfXIsGhbPZIQsvWIlBs=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2025-02-13 14:03:40.000000', '%Y-%m-%d %H:%M:%S.%f'))
            },
            {
                'id': 34,
                'username': 'Sudeshi',
                'password': 'pbkdf2_sha256$720000$6SMdYxVIip2Od5pjx8sKNb$5PLNLLIwUQZ5ZVdWrK48wOh8+h3g6/qEw25+MWT37RU=',
                'is_active': True,
                'date_joined': make_aware(datetime.datetime.strptime('2025-02-13 14:10:43.000000', '%Y-%m-%d %H:%M:%S.%f'))
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
            {'user_id': 22, 'group_id': 5},  # Bashini -> HOD
            {'user_id': 23, 'group_id': 6},  # Roshini -> BOE
            {'user_id': 24, 'group_id': 3},  # Oneli -> Student
            {'user_id': 25, 'group_id': 3},  # Dumindu -> Student
            {'user_id': 26, 'group_id': 3},  # Vindi -> Student
            {'user_id': 27, 'group_id': 3},  # Suneth -> Student
            {'user_id': 28, 'group_id': 3},  # Oshani -> Student
            {'user_id': 29, 'group_id': 3},  # Sandil -> Student
            {'user_id': 30, 'group_id': 3},  # Pasindu -> Student
            {'user_id': 31, 'group_id': 4},  # Mewan -> Lecturer
            {'user_id': 32, 'group_id': 4},  # Chobodhi -> Lecturer
            {'user_id': 33, 'group_id': 4},  # Geethika -> Lecturer
            {'user_id': 34, 'group_id': 4},  # Sudeshi -> Lecturer
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
            {'id': 1, 'name': 'SE01', 'programs_id': 1, 'current_level': '3', 'is_active': 1},
            {'id': 2, 'name': 'SE02', 'programs_id': 1, 'current_level': '2', 'is_active': 1},
            {'id': 3, 'name': 'SE03', 'programs_id': 1, 'current_level': '1', 'is_active': 1},
            {'id': 4, 'name': 'SE04', 'programs_id': 1, 'current_level': '1', 'is_active': 1},
            {'id': 5, 'name': 'SE05', 'programs_id': 1, 'current_level': '1', 'is_active': 1},
            
            # UOG Batches
            {'id': 6, 'name': 'UOG01', 'programs_id': 2, 'current_level': '5', 'is_active': 1},
            {'id': 7, 'name': 'UOG02', 'programs_id': 2, 'current_level': '4', 'is_active': 1},
            {'id': 8, 'name': 'UOG03', 'programs_id': 2, 'current_level': '3', 'is_active': 1},
            {'id': 9, 'name': 'UOG04', 'programs_id': 2, 'current_level': '4', 'is_active': 1},
            {'id': 10, 'name': 'UOG07', 'programs_id': 2, 'current_level': '4', 'is_active': 1},
            {'id': 11, 'name': 'UOG08', 'programs_id': 2, 'current_level': '2', 'is_active': 1},
            {'id': 12, 'name': 'UOG09', 'programs_id': 2, 'current_level': '2', 'is_active': 1},
            {'id': 13, 'name': 'UOG10', 'programs_id': 2, 'current_level': '1', 'is_active': 1},
            {'id': 14, 'name': 'UOG11', 'programs_id': 2, 'current_level': '1', 'is_active': 1}
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
            {'id': 13, 'courses_id': 13, 'batches_id': 1, 'status': 0},  # Mathematics III - Completed

            # First Semester for SE02
            {'id': 14, 'courses_id': 1, 'batches_id': 2, 'status': 1},  # Japanese I
            {'id': 15, 'courses_id': 2, 'batches_id': 2, 'status': 1},  # Computer Fundamentals
            {'id': 16, 'courses_id': 3, 'batches_id': 2, 'status': 1},  # Programming Fundamentals
            {'id': 17, 'courses_id': 4, 'batches_id': 2, 'status': 1},  # Technical Writing
            {'id': 18, 'courses_id': 5, 'batches_id': 2, 'status': 1},  # Mathematics I

            # Second Semester for SE02
            {'id': 19, 'courses_id': 6, 'batches_id': 2, 'status': 1},  # Japanese II
            {'id': 20, 'courses_id': 7, 'batches_id': 2, 'status': 1},  # Database Systems
            {'id': 21, 'courses_id': 8, 'batches_id': 2, 'status': 1},  # Web Programming
            {'id': 22, 'courses_id': 9, 'batches_id': 2, 'status': 0},  # Mathematics II

        ]
        
        for cb in cb_data:
            CoursesBatches.objects.create(**cb)

    def create_lecturers(self):
        """Create lecturer records"""
        lecturers_data = [
            {
                'name': 'Mewan Dissanayake',
                'auth_user_id': 31
            },
            {
                'name': 'Chobodhi Silva',
                'auth_user_id': 32
            },
            {
                'name': 'Geethika Fernando',
                'auth_user_id': 33
            },
            {
                'name': 'Sudeshi Perera',
                'auth_user_id': 34
            },
            {
                'name':'Janith perera',
                'auth_user_id':18
            }
        ]
        
        for lecturer_data in lecturers_data:
            Lecturers.objects.create(**lecturer_data)

    def create_students(self):
        """Create student records"""
        students_data = [
            {'id': 1, 'index_no': 'UGC0122033', 'name': 'Avishka Udara', 'auth_user_id': 15, 'batches_id': 1},
            {'id': 2, 'index_no': 'UGC0122030', 'name': 'Sasindu Jayawardana', 'auth_user_id': 16, 'batches_id': 1},
            {'id': 3, 'index_no': 'UGC0222001', 'name': 'Oneli Perera', 'auth_user_id': 24, 'batches_id': 2},
            {'id': 4, 'index_no': 'UGC0222002', 'name': 'Dumindu Silva', 'auth_user_id': 25, 'batches_id': 2},
            {'id': 5, 'index_no': 'UGC0222003', 'name': 'Vindi Fernando', 'auth_user_id': 26, 'batches_id': 2},
            {'id': 6, 'index_no': 'UGC0222004', 'name': 'Suneth Bandara', 'auth_user_id': 27, 'batches_id': 2},
            {'id': 7, 'index_no': 'UGC0222005', 'name': 'Oshani Peris', 'auth_user_id': 28, 'batches_id': 2},
            {'id': 8, 'index_no': 'UGC0222006', 'name': 'Sandil Malshan', 'auth_user_id': 29, 'batches_id': 2},
            {'id': 9, 'index_no': 'UGC0222007', 'name': 'Pasindu Akalanka', 'auth_user_id': 30, 'batches_id': 2}
        ]
        
        for student_data in students_data:
            Students.objects.create(**student_data)
    
    def create_courses_student(self):
        """Create course enrollments with final marks for Sasindu"""
        enrollments_data = [
            # First Semester-sasindu
            {'enroll_id': 1, 'marks': 14.67, 'students_id': 2, 'courses_id': 1, 'level': 1},  # Japanese I
            {'enroll_id': 2, 'marks': 88.2, 'students_id': 2, 'courses_id': 2, 'level': 1},  # Computer Fundamentals
            {'enroll_id': 3, 'marks': 86.4, 'students_id': 2, 'courses_id': 3, 'level': 1},  # Programming Fundamentals
            {'enroll_id': 4, 'marks': 90.0, 'students_id': 2, 'courses_id': 4, 'level': 1},  # Technical Writing
            {'enroll_id': 5, 'marks': 82.5, 'students_id': 2, 'courses_id': 5, 'level': 1},  # Mathematics I
            
            # Second Semester
            {'enroll_id': 6, 'marks': 84.8, 'students_id': 2, 'courses_id': 6, 'level': 2},  # Japanese II
            {'enroll_id': 7, 'marks': 86.2, 'students_id': 2, 'courses_id': 7, 'level': 2},  # Database Systems
            {'enroll_id': 8, 'marks': 88.5, 'students_id': 2, 'courses_id': 8, 'level': 2},  # Web Programming
      
            
            # Third Semester
            {'enroll_id': 10, 'marks': 85.5, 'students_id': 2, 'courses_id': 10, 'level': 3},  # Data Structures
            {'enroll_id': 11, 'marks': 87.2, 'students_id': 2, 'courses_id': 11, 'level': 3},  # Data StructuresSoftware Architecture
            {'enroll_id': 12, 'marks': 89.0, 'students_id': 2, 'courses_id': 12, 'level': 3},  # Data StructuresVisual Programming
   

            # First Semester-avishka
            {'enroll_id': 14, 'marks': 68.5, 'students_id': 1, 'courses_id': 1, 'level': 1},  # Japanese I
            {'enroll_id': 15, 'marks': 72.2, 'students_id': 1, 'courses_id': 2, 'level': 1},  # Computer Fundamentals
            {'enroll_id': 16, 'marks': 75.4, 'students_id': 1, 'courses_id': 3, 'level': 1},  # Programming Fundamentals
            {'enroll_id': 17, 'marks': 78.0, 'students_id': 1, 'courses_id': 4, 'level': 1},  # Technical Writing
            {'enroll_id': 18, 'marks': 71.5, 'students_id': 1, 'courses_id': 5, 'level': 1},  # Mathematics I

            # Second Semester 
            {'enroll_id': 19, 'marks': 74.8, 'students_id': 1, 'courses_id': 6, 'level': 2},  # Japanese II
            {'enroll_id': 20, 'marks': 76.2, 'students_id': 1, 'courses_id': 7, 'level': 2},  # Database Systems
            {'enroll_id': 21, 'marks': 77.5, 'students_id': 1, 'courses_id': 8, 'level': 2},  # Web Programming
        

            # Third Semester
            {'enroll_id': 23, 'marks': 75.5, 'students_id': 1, 'courses_id': 10, 'level': 3},  # Data Structures
            {'enroll_id': 24, 'marks': 77.2, 'students_id': 1, 'courses_id': 11, 'level': 3},  # Software Architecture
            {'enroll_id': 25, 'marks': 76.0, 'students_id': 1, 'courses_id': 12, 'level': 3},  # Visual Programming
            

             # First Semester - SE02 Students (Oneli - id: 3)
            {'enroll_id': 27, 'marks': 82.5, 'students_id': 3, 'courses_id': 1, 'level': 1},  # Japanese I
            {'enroll_id': 28, 'marks': 78.4, 'students_id': 3, 'courses_id': 2, 'level': 1},  # Computer Fundamentals
            {'enroll_id': 29, 'marks': 85.2, 'students_id': 3, 'courses_id': 3, 'level': 1},  # Programming Fundamentals
            {'enroll_id': 30, 'marks': 79.6, 'students_id': 3, 'courses_id': 4, 'level': 1},  # Technical Writing
            {'enroll_id': 31, 'marks': 76.8, 'students_id': 3, 'courses_id': 5, 'level': 1},  # Mathematics I

            # Second Semester - Oneli
            {'enroll_id': 32, 'marks': 81.2, 'students_id': 3, 'courses_id': 6, 'level': 2},  # Japanese II
            {'enroll_id': 33, 'marks': 83.5, 'students_id': 3, 'courses_id': 7, 'level': 2},  # Database Systems
            {'enroll_id': 34, 'marks': 84.7, 'students_id': 3, 'courses_id': 8, 'level': 2},  # Web Programming
        

            # First Semester - Dumindu (id: 4)
            {'enroll_id': 36, 'marks': 75.5, 'students_id': 4, 'courses_id': 1, 'level': 1},  # Japanese I
            {'enroll_id': 37, 'marks': 82.4, 'students_id': 4, 'courses_id': 2, 'level': 1},  # Computer Fundamentals
            {'enroll_id': 38, 'marks': 79.2, 'students_id': 4, 'courses_id': 3, 'level': 1},  # Programming Fundamentals
            {'enroll_id': 39, 'marks': 81.6, 'students_id': 4, 'courses_id': 4, 'level': 1},  # Technical Writing
            {'enroll_id': 40, 'marks': 73.8, 'students_id': 4, 'courses_id': 5, 'level': 1},  # Mathematics I

            # Second Semester - Dumindu
            {'enroll_id': 41, 'marks': 77.2, 'students_id': 4, 'courses_id': 6, 'level': 2},  # Japanese II
            {'enroll_id': 42, 'marks': 80.5, 'students_id': 4, 'courses_id': 7, 'level': 2},  # Database Systems
            {'enroll_id': 43, 'marks': 78.7, 'students_id': 4, 'courses_id': 8, 'level': 2},  # Web Programming
            

            # First Semester - Vindi (id: 5)
            {'enroll_id': 45, 'marks': 88.5, 'students_id': 5, 'courses_id': 1, 'level': 1},  # Japanese I
            {'enroll_id': 46, 'marks': 86.4, 'students_id': 5, 'courses_id': 2, 'level': 1},  # Computer Fundamentals
            {'enroll_id': 47, 'marks': 89.2, 'students_id': 5, 'courses_id': 3, 'level': 1},  # Programming Fundamentals
            {'enroll_id': 48, 'marks': 87.6, 'students_id': 5, 'courses_id': 4, 'level': 1},  # Technical Writing
            {'enroll_id': 49, 'marks': 85.8, 'students_id': 5, 'courses_id': 5, 'level': 1},  # Mathematics I

            # Second Semester - Vindi
            {'enroll_id': 50, 'marks': 87.2, 'students_id': 5, 'courses_id': 6, 'level': 2},  # Japanese II
            {'enroll_id': 51, 'marks': 88.5, 'students_id': 5, 'courses_id': 7, 'level': 2},  # Database Systems
            {'enroll_id': 52, 'marks': 86.7, 'students_id': 5, 'courses_id': 8, 'level': 2},  # Web Programming
         

            # First Semester - Suneth (id: 6)
            {'enroll_id': 54, 'marks': 35.5, 'students_id': 6, 'courses_id': 1, 'level': 1},  # Japanese I - Failed
            {'enroll_id': 55, 'marks': 72.4, 'students_id': 6, 'courses_id': 2, 'level': 1},  # Computer Fundamentals
            {'enroll_id': 56, 'marks': 38.2, 'students_id': 6, 'courses_id': 3, 'level': 1},  # Programming Fundamentals - Failed
            {'enroll_id': 57, 'marks': 68.6, 'students_id': 6, 'courses_id': 4, 'level': 1},  # Technical Writing
            {'enroll_id': 58, 'marks': 35.8, 'students_id': 6, 'courses_id': 5, 'level': 1},  # Mathematics I - Failed

            # Second Semester - Suneth
            {'enroll_id': 59, 'marks': 67.2, 'students_id': 6, 'courses_id': 6, 'level': 2},  # Japanese II
            {'enroll_id': 60, 'marks': 65.5, 'students_id': 6, 'courses_id': 7, 'level': 2},  # Database Systems
            {'enroll_id': 61, 'marks': 66.7, 'students_id': 6, 'courses_id': 8, 'level': 2},  # Web Programming
    

            # First Semester - Oshani (id: 7)
            {'enroll_id': 63, 'marks': 92.5, 'students_id': 7, 'courses_id': 1, 'level': 1},  # Japanese I
            {'enroll_id': 64, 'marks': 94.4, 'students_id': 7, 'courses_id': 2, 'level': 1},  # Computer Fundamentals
            {'enroll_id': 65, 'marks': 93.2, 'students_id': 7, 'courses_id': 3, 'level': 1},  # Programming Fundamentals
            {'enroll_id': 66, 'marks': 91.6, 'students_id': 7, 'courses_id': 4, 'level': 1},  # Technical Writing
            {'enroll_id': 67, 'marks': 90.8, 'students_id': 7, 'courses_id': 5, 'level': 1},  # Mathematics I

            # Second Semester - Oshani
            {'enroll_id': 68, 'marks': 93.2, 'students_id': 7, 'courses_id': 6, 'level': 2},  # Japanese II
            {'enroll_id': 69, 'marks': 92.5, 'students_id': 7, 'courses_id': 7, 'level': 2},  # Database Systems
            {'enroll_id': 70, 'marks': 94.7, 'students_id': 7, 'courses_id': 8, 'level': 2},  # Web Programming

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

        ]
        
        for crit_data in criteria_data:
            Criterias.objects.create(**crit_data)

    def create_students_criterias(self):
        """Create comprehensive assessment marks for Sasindu across all completed courses"""
        sc_data = [
            #sasindus marks
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

            # Avishka's criteria marks

            # Japanese Language Level I
            {'id': 54, 'students_id': 1, 'criterias_id': 1, 'mark': '70'},  # Mid-Term Test
            {'id': 55, 'students_id': 1, 'criterias_id': 2, 'mark': '68'},  # Oral Presentation
            {'id': 56, 'students_id': 1, 'criterias_id': 3, 'mark': '69'},  # Final Written
            {'id': 57, 'students_id': 1, 'criterias_id': 4, 'mark': '67'},  # Final Oral

            # Computer Fundamentals
            {'id': 58, 'students_id': 1, 'criterias_id': 5, 'mark': '74'},  # Theory Quiz
            {'id': 59, 'students_id': 1, 'criterias_id': 6, 'mark': '72'},  # Lab Assessment
            {'id': 60, 'students_id': 1, 'criterias_id': 7, 'mark': '71'},  # Final Theory
            {'id': 61, 'students_id': 1, 'criterias_id': 8, 'mark': '73'},  # Final Practical

            # Programming Fundamentals
            {'id': 62, 'students_id': 1, 'criterias_id': 9, 'mark': '76'},   # Programming Quiz
            {'id': 63, 'students_id': 1, 'criterias_id': 10, 'mark': '75'},  # Programming Assignment
            {'id': 64, 'students_id': 1, 'criterias_id': 11, 'mark': '77'},  # Mini Project
            {'id': 65, 'students_id': 1, 'criterias_id': 12, 'mark': '74'},  # Final Theory
            {'id': 66, 'students_id': 1, 'criterias_id': 13, 'mark': '75'},  # Final Practical

            # Technical Writing
            {'id': 67, 'students_id': 1, 'criterias_id': 14, 'mark': '79'},  # Writing Assignment 1
            {'id': 68, 'students_id': 1, 'criterias_id': 15, 'mark': '78'},  # Documentation Project
            {'id': 69, 'students_id': 1, 'criterias_id': 16, 'mark': '77'},  # Oral Presentation
            {'id': 70, 'students_id': 1, 'criterias_id': 17, 'mark': '78'},  # Final Assessment

            # Mathematics I for SE
            {'id': 71, 'students_id': 1, 'criterias_id': 18, 'mark': '72'},  # Math Quiz 1
            {'id': 72, 'students_id': 1, 'criterias_id': 19, 'mark': '71'},  # Problem Sets
            {'id': 73, 'students_id': 1, 'criterias_id': 20, 'mark': '71'},  # Final Exam

            # Japanese Language Level I - Oneli
            {'id': 74, 'students_id': 3, 'criterias_id': 1, 'mark': '84'},  # Mid-Term Test
            {'id': 75, 'students_id': 3, 'criterias_id': 2, 'mark': '81'},  # Oral Presentation
            {'id': 76, 'students_id': 3, 'criterias_id': 3, 'mark': '83'},  # Final Written
            {'id': 77, 'students_id': 3, 'criterias_id': 4, 'mark': '82'},  # Final Oral

            # Computer Fundamentals - Oneli
            {'id': 78, 'students_id': 3, 'criterias_id': 5, 'mark': '79'},  # Theory Quiz
            {'id': 79, 'students_id': 3, 'criterias_id': 6, 'mark': '78'},  # Lab Assessment
            {'id': 80, 'students_id': 3, 'criterias_id': 7, 'mark': '77'},  # Final Theory
            {'id': 81, 'students_id': 3, 'criterias_id': 8, 'mark': '80'},  # Final Practical

            # Japanese Language Level I - Dumindu
            {'id': 82, 'students_id': 4, 'criterias_id': 1, 'mark': '76'},  # Mid-Term Test
            {'id': 83, 'students_id': 4, 'criterias_id': 2, 'mark': '75'},  # Oral Presentation
            {'id': 84, 'students_id': 4, 'criterias_id': 3, 'mark': '74'},  # Final Written
            {'id': 85, 'students_id': 4, 'criterias_id': 4, 'mark': '77'},  # Final Oral

            # Computer Fundamentals - Dumindu
            {'id': 86, 'students_id': 4, 'criterias_id': 5, 'mark': '83'},  # Theory Quiz
            {'id': 87, 'students_id': 4, 'criterias_id': 6, 'mark': '82'},  # Lab Assessment
            {'id': 88, 'students_id': 4, 'criterias_id': 7, 'mark': '81'},  # Final Theory
            {'id': 89, 'students_id': 4, 'criterias_id': 8, 'mark': '84'},  # Final Practical

            # Suneth - Poor CA performance example
            {'id': 90, 'students_id': 6, 'criterias_id': 1, 'mark': '32'},  # Japanese I - Mid-Term Test
            {'id': 91, 'students_id': 6, 'criterias_id': 2, 'mark': '35'},  # Japanese I - Oral Presentation
            {'id': 92, 'students_id': 6, 'criterias_id': 3, 'mark': '38'},  # Japanese I - Final Written
            {'id': 93, 'students_id': 6, 'criterias_id': 4, 'mark': '35'},  # Japanese I - Final Oral

            # Programming Fundamentals - Suneth's failed subject
            {'id': 94, 'students_id': 6, 'criterias_id': 9, 'mark': '35'},   # Programming Quiz
            {'id': 95, 'students_id': 6, 'criterias_id': 10, 'mark': '38'},  # Programming Assignment
            {'id': 96, 'students_id': 6, 'criterias_id': 11, 'mark': '36'},  # Mini Project
            {'id': 97, 'students_id': 6, 'criterias_id': 12, 'mark': '40'},  # Final Theory
            {'id': 98, 'students_id': 6, 'criterias_id': 13, 'mark': '42'},  # Final Practical

            # Oshani - Outstanding performance example
            {'id': 99, 'students_id': 7, 'criterias_id': 1, 'mark': '93'},   # Japanese I - Mid-Term Test
            {'id': 100, 'students_id': 7, 'criterias_id': 2, 'mark': '92'},  # Japanese I - Oral Presentation
            {'id': 101, 'students_id': 7, 'criterias_id': 3, 'mark': '94'},  # Japanese I - Final Written
            {'id': 102, 'students_id': 7, 'criterias_id': 4, 'mark': '91'},  # Japanese I - Final Oral
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
            {'id': 13, 'grade': 'C-', 's_grade': 'A', 'courses_id': 13, 'students_id': 2},  # Mathematics III

            # Avishka's results
            # First Semester
            {'id': 14, 'grade': 'B', 's_grade': 'B', 'courses_id': 1, 'students_id': 1},    # Japanese I
            {'id': 15, 'grade': 'B+', 's_grade': 'B+', 'courses_id': 2, 'students_id': 1},  # Computer Fundamentals
            {'id': 16, 'grade': 'B+', 's_grade': 'B+', 'courses_id': 3, 'students_id': 1},  # Programming Fundamentals
            {'id': 17, 'grade': 'B+', 's_grade': 'B+', 'courses_id': 4, 'students_id': 1},  # Technical Writing
            {'id': 18, 'grade': 'B', 's_grade': 'B', 'courses_id': 5, 'students_id': 1},    # Mathematics I

            # Second Semester
            {'id': 19, 'grade': 'B+', 's_grade': 'B+', 'courses_id': 6, 'students_id': 1},  # Japanese II
            {'id': 20, 'grade': 'B+', 's_grade': 'B+', 'courses_id': 7, 'students_id': 1},  # Database Systems
            {'id': 21, 'grade': 'B+', 's_grade': 'B+', 'courses_id': 8, 'students_id': 1},  # Web Programming
            {'id': 22, 'grade': 'B', 's_grade': 'B', 'courses_id': 9, 'students_id': 1},    # Mathematics II

            # Third Semester
            {'id': 23, 'grade': 'B+', 's_grade': 'B+', 'courses_id': 10, 'students_id': 1}, # Data Structures
            {'id': 24, 'grade': 'B+', 's_grade': 'B+', 'courses_id': 11, 'students_id': 1}, # Software Architecture
            {'id': 25, 'grade': 'B+', 's_grade': 'B+', 'courses_id': 12, 'students_id': 1}, # Visual Programming
            {'id': 26, 'grade': 'B', 's_grade': 'B', 'courses_id': 13, 'students_id': 1},   # Mathematics III

            # First Semester - Oneli
            {'id': 27, 'grade': 'A-', 's_grade': 'A-', 'courses_id': 1, 'students_id': 3},  # Japanese I
            {'id': 28, 'grade': 'B+', 's_grade': 'B+', 'courses_id': 2, 'students_id': 3},  # Computer Fundamentals
            {'id': 29, 'grade': 'A', 's_grade': 'A', 'courses_id': 3, 'students_id': 3},    # Programming Fundamentals
            {'id': 30, 'grade': 'B+', 's_grade': 'B+', 'courses_id': 4, 'students_id': 3},  # Technical Writing
            {'id': 31, 'grade': 'B', 's_grade': 'B', 'courses_id': 5, 'students_id': 3},    # Mathematics I

            # Second Semester - Oneli
            {'id': 32, 'grade': 'A-', 's_grade': 'A-', 'courses_id': 6, 'students_id': 3},  # Japanese II
            {'id': 33, 'grade': 'A-', 's_grade': 'A-', 'courses_id': 7, 'students_id': 3},  # Database Systems
            {'id': 34, 'grade': 'A', 's_grade': 'A', 'courses_id': 8, 'students_id': 3},    # Web Programming
            {'id': 35, 'grade': 'B+', 's_grade': 'B+', 'courses_id': 9, 'students_id': 3},  # Mathematics II

            # First Semester - Dumindu
            {'id': 36, 'grade': 'B', 's_grade': 'B', 'courses_id': 1, 'students_id': 4},    # Japanese I
            {'id': 37, 'grade': 'A-', 's_grade': 'A-', 'courses_id': 2, 'students_id': 4},  # Computer Fundamentals
            {'id': 38, 'grade': 'B+', 's_grade': 'B+', 'courses_id': 3, 'students_id': 4},  # Programming Fundamentals
            {'id': 39, 'grade': 'A-', 's_grade': 'A-', 'courses_id': 4, 'students_id': 4},  # Technical Writing
            {'id': 40, 'grade': 'B', 's_grade': 'B', 'courses_id': 5, 'students_id': 4},    # Mathematics I

            # Second Semester - Dumindu
            {'id': 41, 'grade': 'B+', 's_grade': 'B+', 'courses_id': 6, 'students_id': 4},  # Japanese II
            {'id': 42, 'grade': 'A-', 's_grade': 'A-', 'courses_id': 7, 'students_id': 4},  # Database Systems
            {'id': 43, 'grade': 'B+', 's_grade': 'B+', 'courses_id': 8, 'students_id': 4},  # Web Programming
            {'id': 44, 'grade': 'B', 's_grade': 'B', 'courses_id': 9, 'students_id': 4},    # Mathematics II

            # First Semester - Vindi
            {'id': 45, 'grade': 'A', 's_grade': 'A', 'courses_id': 1, 'students_id': 5},    # Japanese I
            {'id': 46, 'grade': 'A', 's_grade': 'A', 'courses_id': 2, 'students_id': 5},    # Computer Fundamentals
            {'id': 47, 'grade': 'A', 's_grade': 'A', 'courses_id': 3, 'students_id': 5},    # Programming Fundamentals
            {'id': 48, 'grade': 'A', 's_grade': 'A', 'courses_id': 4, 'students_id': 5},    # Technical Writing
            {'id': 49, 'grade': 'A', 's_grade': 'A', 'courses_id': 5, 'students_id': 5},    # Mathematics I

            # First Semester - Suneth (with failures)
            {'id': 50, 'grade': 'F', 's_grade': 'F', 'courses_id': 1, 'students_id': 6},    # Japanese I
            {'id': 51, 'grade': 'B', 's_grade': 'B', 'courses_id': 2, 'students_id': 6},    # Computer Fundamentals
            {'id': 52, 'grade': 'F', 's_grade': 'F', 'courses_id': 3, 'students_id': 6},    # Programming Fundamentals
            {'id': 53, 'grade': 'B-', 's_grade': 'B-', 'courses_id': 4, 'students_id': 6},  # Technical Writing
            {'id': 54, 'grade': 'F', 's_grade': 'F', 'courses_id': 5, 'students_id': 6},    # Mathematics I

            # First Semester - Oshani (exceptional performance)
            {'id': 55, 'grade': 'A+', 's_grade': 'A+', 'courses_id': 1, 'students_id': 7},  # Japanese I
            {'id': 56, 'grade': 'A+', 's_grade': 'A+', 'courses_id': 2, 'students_id': 7},  # Computer Fundamentals
            {'id': 57, 'grade': 'A+', 's_grade': 'A+', 'courses_id': 3, 'students_id': 7},  # Programming Fundamentals
            {'id': 58, 'grade': 'A+', 's_grade': 'A+', 'courses_id': 4, 'students_id': 7},  # Technical Writing
            {'id': 59, 'grade': 'A+', 's_grade': 'A+', 'courses_id': 5, 'students_id': 7},  # Mathematics I
        ]
        
        for result_data in results_data:
            Results.objects.create(**result_data)

