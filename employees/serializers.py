from rest_framework import serializers

from employees.models import Employee, Profession


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Employee
        fields = ('url', Employee.EMAIL, Employee.LAST_NAME, Employee.NAME, Employee.PROFESSION)
        'url',
        extra_kwargs = {
            'url': {'lookup_field': Employee.EMAIL},
        }


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('url', Profession.NAME, Profession.DESCRIPTION)
        # extra_kwargs = {
        #     'url': {'lookup_field': Profession.PK},
        # }
