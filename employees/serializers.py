from rest_framework import serializers
from .models import Employee, Department

class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'employee_count']
    
    def get_employee_count(self, obj):
        return obj.employees.count()

class EmployeeSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source='department',
        write_only=True
    )
    
    class Meta:
        model = Employee
        fields = [
            'id', 
            'name', 
            'email', 
            'phone',
            'department',
            'department_id',
            'date_joined',
            'is_active'
        ]
        extra_kwargs = {
            'email': {'validators': []}  # Disable unique check during updates
        }
