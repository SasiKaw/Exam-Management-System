from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Reset database by dropping all tables and re-creating them'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Disable foreign key checks
            cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
            
            # Get list of all tables
            cursor.execute("SHOW TABLES")
            tables = [record[0] for record in cursor.fetchall()]
            
            # Drop each table
            for table in tables:
                self.stdout.write(f'Dropping table {table}...')
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
            
            # Re-enable foreign key checks
            cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
            
        self.stdout.write(self.style.SUCCESS('Successfully reset database'))