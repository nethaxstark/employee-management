from django.core.management.base import BaseCommand
from faker import Faker
from employees.models import Department, Employee
from attendance.models import Attendance
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        fake = Faker()
        
        # Clear existing data to avoid conflicts
        Attendance.objects.all().delete()
        Employee.objects.all().delete()
        Department.objects.all().delete()
        
        # Create departments
        departments = ['HR', 'Engineering', 'Marketing', 'Sales']
        for dept in departments:
            Department.objects.get_or_create(name=dept)
        
        # Create employees
        depts = list(Department.objects.all())
        employees = []
        for _ in range(30):  # Create 30 employees
            emp = Employee.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
                phone=fake.phone_number()[:15],
                department=random.choice(depts),
                date_joined=fake.date_this_decade()
            )
            employees.append(emp)
        
        # Create attendance - FIXED VERSION
        for emp in employees:
            # Generate unique dates for each employee
            base_date = fake.date_between(start_date='-30d')
            for day_offset in range(20):  # Create 20 attendance records per employee
                try:
                    Attendance.objects.create(
                        employee=emp,
                        date=base_date + timedelta(days=day_offset),
                        status=random.choice(['present', 'absent', 'late'])
                    )
                except:
                    continue  # Skip if any duplicates slip through
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))