from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.test import APITestCase

from employees import views
from employees import models
from employees.models import Employee
from employees.scripts.create_professions import create_professions


def create_test_employees(professions):
    employees = [Employee(name='test',
                          last_name='test',
                          email='test1@test.test',
                          profession=professions[0]),
                 Employee(name='test',
                          last_name='test',
                          email='test2@test.test',
                          profession=professions[1])]

    for employee in employees:
        employee.save()

    return employees


class TestApiRoot(APITestCase):
    def setUp(self):
        User.objects.create_superuser(username='test', password='test', email='test@test.test')
        self.client.login(username='test', password='test')

    def test_api_root_should_return_root_when_get(self):
        # given
        url = reverse(views.api_root.__name__)
        # when
        response = self.client.get(url)
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_root_should_point_to_models_when_get(self):
        # given
        url = reverse(views.api_root.__name__)
        root_response = self.client.get(url)
        # when
        response_employee_list = self.client.get(root_response.data[models.Employee.list_name])
        response_profession_list = self.client.get(root_response.data[models.Profession.list_name])
        # then
        self.assertEqual(response_employee_list.status_code, status.HTTP_200_OK)
        self.assertEqual(response_profession_list.status_code, status.HTTP_200_OK)


class TestProfessionList(APITestCase):
    def setUp(self):
        create_professions()
        User.objects.create_superuser(username='test', password='test', email='test@test.test')
        self.client.login(username='test', password='test')

    def test_profession_list_view_should_list_all_professions_when_get(self):
        # given
        url = reverse(views.ProfessionList.rev_name)
        # when
        response = self.client.get(url)
        all_professions = set(choice[0] for choice in models.Profession.CHOICES)
        ret_professions = set(profession[models.Profession.NAME] for profession in response.data)
        # then
        self.assertEqual(all_professions, ret_professions)

    def test_profession_list_view_should_return_403_when_not_authenticated(self):
        # given
        url = reverse(views.ProfessionList.rev_name)
        # when
        self.client.logout()
        response = self.client.get(url)
        # then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestProfessionDetail(APITestCase):
    def setUp(self):
        self.professions = create_professions()
        User.objects.create_superuser(username='test', password='test', email='test@test.test')
        self.client.login(username='test', password='test')

    def test_profession_detail_view_should_return_profession_when_get(self):
        # given
        url = reverse(views.ProfessionDetail.rev_name, kwargs={'pk': '1'})
        # when
        response = self.client.get(url)
        response.data.pop('url')
        model_to_dict(self.professions[0]).pop('id')
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profession_detail_view_should_return_403_when_not_authenticated(self):
        # given
        url = reverse(views.ProfessionDetail.rev_name, kwargs={'pk': '1'})
        # when
        self.client.logout()
        response = self.client.get(url)
        # then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestEmployeeListView(APITestCase):
    def setUp(self):
        self.professions = create_professions()
        User.objects.create_superuser(username='test', password='test', email='test@test.test')
        self.client.login(username='test', password='test')

    def test_employees_list_view_should_list_all_employees_when_get(self):
        # given
        employees = create_test_employees(self.professions)

        url = reverse(views.EmployeeList.rev_name)
        # when
        response = self.client.get(url)
        # then
        # all_professions = set(choice[0] for choice in models.Profession.CHOICES)
        ret_employees = [employee_data[models.Employee.NAME] for employee_data in response.data]
        # then
        self.assertEqual(ret_employees, [employee.name for employee in employees])

    def test_employees_list_view_should_save_employee_when_post_valid_data(self):
        # given
        url = reverse(views.ProfessionList.rev_name)
        profession_response = self.client.get(url)
        profession_url = profession_response.data[0]['url']

        employee_data = {
            Employee.NAME: 'test',
            Employee.LAST_NAME: 'test',
            Employee.EMAIL: 'test@test.test',
            Employee.PROFESSION: profession_url
        }

        url = reverse(views.EmployeeList.rev_name)
        # when
        response = self.client.post(url, employee_data)
        employee_url = response.data['url']
        employee_response = self.client.get(employee_url)
        # then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        employee_response.data.pop('url')
        self.assertEqual(employee_response.data, employee_data)

    def test_employees_list_view_should_not_save_employee_when_post_malformed_email(self):
        # given
        url = reverse(views.ProfessionList.rev_name)
        profession_response = self.client.get(url)
        profession_url = profession_response.data[0]['url']

        employee_data = {
            Employee.NAME: 'test',
            Employee.LAST_NAME: 'test',
            Employee.EMAIL: 'testtest.test',  # not an email
            Employee.PROFESSION: profession_url
        }

        url = reverse(views.EmployeeList.rev_name)
        # when
        response = self.client.post(url, employee_data)
        # then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employees_list_view_should_not_save_employee_when_post_malformed_profession_url(self):
        # given
        employee_data = {
            Employee.NAME: 'test',
            Employee.LAST_NAME: 'test',
            Employee.EMAIL: 'testtest.test',  # not an email
            Employee.PROFESSION: 'test/test'
        }

        url = reverse(views.EmployeeList.rev_name)
        # when
        response = self.client.post(url, employee_data)
        # then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employees_list_view_should_return_employees_filtered_when_proper_filter_and_value_given(self):
        # given
        employees = create_test_employees(self.professions)
        url = reverse(views.EmployeeList.rev_name)
        # when
        response = self.client.get(url, {'filter': 'email', 'value': '1'})
        # then
        self.assertEqual(model_to_dict(employees[0])[Employee.EMAIL], dict(response.data[0])[Employee.EMAIL])

    def test_employees_list_view_should_return_400_when_filter_not_in_query_params(self):
        # given
        create_test_employees(self.professions)
        url = reverse(views.EmployeeList.rev_name)
        # when
        response = self.client.get(url, {'value': '1'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employees_list_view_should_return_400_when_filter_type_not_in_model_fields(self):
        # given
        create_test_employees(self.professions)
        url = reverse(views.EmployeeList.rev_name)
        # when
        response = self.client.get(url, {'filter': 'test', 'value': '1'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employees_list_view_should_return_403_when_not_authenticated(self):
        # given
        url = reverse(views.EmployeeList.rev_name)
        # when
        self.client.logout()
        response = self.client.get(url)
        # then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestEmployeeDetail(APITestCase):
    def setUp(self):
        User.objects.create_superuser(username='test', password='test', email='test@test.test')
        self.client.login(username='test', password='test')
        professions = create_professions()
        self.employees = create_test_employees(professions)

    def test_employee_detail_view_should_return_employee_when_get(self):
        # given
        url = reverse(views.EmployeeDetail.rev_name, kwargs={'email': self.employees[0].email})
        # when
        response = self.client.get(url)
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_detail_view_should_remove_employee_when_delete(self):
        # given
        url = reverse(views.EmployeeDetail.rev_name, kwargs={'email': self.employees[0].email})
        # when
        response = self.client.delete(url)
        # then
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_employee_detail_view_should_update_employee_when_put_name_and_last_name(self):
        # given
        url = reverse(views.EmployeeDetail.rev_name, kwargs={'email': self.employees[0].email})
        # when
        response = self.client.put(url, data={Employee.NAME: 'change_name',
                                              Employee.LAST_NAME: 'change_last'})
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url)
        self.assertEqual(response.data[Employee.NAME], 'change_name')
        self.assertEqual(response.data[Employee.LAST_NAME], 'change_last')

    def test_employee_detail_view_should_not_update_employee_when_put_email(self):
        # given
        url = reverse(views.EmployeeDetail.rev_name, kwargs={'email': self.employees[0].email})
        # when
        response = self.client.put(url, data={Employee.EMAIL: 'change@change.change'})
        # then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employees_detail_view_should_return_403_when_not_authenticated(self):
        # given
        url = reverse(views.EmployeeDetail.rev_name, kwargs={'email': self.employees[0].email})
        # when
        self.client.logout()
        response = self.client.get(url)
        # then
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)