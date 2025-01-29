from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Create all database tables'

    def handle(self, *args, **options):
        # Get the path to the SQL file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sql_file_path = os.path.join(current_dir, 'create_tables.sql')

        # Read the SQL file
        with open(sql_file_path, 'r') as f:
            sql_statements = f.read()

        # Execute the SQL
        with connection.cursor() as cursor:
            # Split the SQL statements and execute them one by one
            for statement in sql_statements.split(';'):
                if statement.strip():
                    self.stdout.write(f'Executing: {statement[:100]}...')
                    cursor.execute(statement)

        self.stdout.write(self.style.SUCCESS('Successfully created all tables'))