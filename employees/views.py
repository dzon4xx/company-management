from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from employees import APP_NAME
from employees.models import Employee, Profession
from employees.serializers import EmployeeSerializer, ProfessionSerializer

import re


class EmployeeList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        employees = Employee.objects.all()
        if request.query_params:
            try:
                filter_type = request.query_params['filter']
                try:
                    getattr(Employee, filter_type)
                except AttributeError:
                    return Response('Employee has no field {}'.format(filter_type), status.HTTP_400_BAD_REQUEST)
            except KeyError:
                return Response('Filter not found in query string', status.HTTP_400_BAD_REQUEST)
            else:
                filter_value = request.query_params.get('value', '')
                column_name = Employee.__name__.lower()
                table_name = APP_NAME
                employees = Employee.objects\
                    .raw('select * from {}_{} where {} like "%{}%";'
                    .format(table_name, column_name, filter_type, filter_value))

        serializer = EmployeeSerializer(employees, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EmployeeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetail(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, email, format=None):
        employee = get_object_or_404(Employee, email=email)
        serializer = EmployeeSerializer(employee, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, email, format=None):
        employee = get_object_or_404(Employee, email=email)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, email, format=None):
        employee = get_object_or_404(Employee, email=email)
        serializer = EmployeeSerializer(data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            if Employee.EMAIL in request.data:
                return Response('can\'t change email', status=status.HTTP_400_BAD_REQUEST)
            employee.__dict__.update(request.data)
            employee.save()
            return Response(request.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfessionList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        professions = Profession.objects.all()
        serializer = ProfessionSerializer(professions, many=True, context={'request': request})
        return Response(serializer.data)


class ProfessionDetail(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        profession = Profession.objects.get(pk=pk)
        serializer = ProfessionSerializer(profession, context={'request': request})
        return Response(serializer.data)


@api_view()
def api_root(request, format=None):
    return Response({Employee.list_name: reverse(EmployeeList.rev_name, request=request, format=format),
                     Profession.list_name: reverse(ProfessionList.rev_name, request=request, format=format)})


# monkey patch classes
for cls in [ProfessionDetail, ProfessionList, EmployeeDetail, EmployeeList]:
    cls.rev_name = re.sub('([A-Z][a-z0-9]+)', r'\1-', cls.__name__).rstrip('-').lower()