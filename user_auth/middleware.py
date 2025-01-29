from django.core.management import call_command
from django.conf import settings
import atexit
from django.db import connection

class DatabaseSeedingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        if settings.DEBUG:  # Only in development
            try:
                # Create tables first
                print("Creating tables...")
                call_command('create_tables')
                
                # Clean up existing data
                self.cleanup()
                
                # Seed fresh data
                print("Seeding database...")
                call_command('seed_db')
                
                # Register cleanup for server shutdown
                atexit.register(self.cleanup)
            except Exception as e:
                print(f"Error initializing database: {str(e)}")

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def cleanup(self):
        print("Cleaning up database...")
        with connection.cursor() as cursor:
            try:
                cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
                
                # Delete data but keep table structure
                tables = [
                    'results',
                    'students_criterias',
                    'criterias',
                    'courses_student',
                    'courses_batches',
                    'courses_lecturer',
                    'courses',
                    'students',
                    'subjects',
                    'batches',
                    'semesters',
                    'programs',
                    'auth_user_groups',
                    'auth_user_user_permissions',
                    'auth_group_permissions',
                    'auth_user',
                    'auth_group'
                ]
                
                for table in tables:
                    try:
                        cursor.execute(f'DELETE FROM {table};')
                        cursor.execute(f'ALTER TABLE {table} AUTO_INCREMENT = 1;')
                    except Exception as e:
                        print(f"Error cleaning table {table}: {str(e)}")
                
                cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
            except Exception as e:
                print(f"Error during cleanup: {str(e)}")