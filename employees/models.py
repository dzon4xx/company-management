from django.db import models


class classproperty:
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


class ModelNames:

    @classproperty
    def name(cls):
        return cls.__name__.lower()

    @classproperty
    def list_name(cls):
        return cls.__name__.lower() + 's'


class Profession(models.Model, ModelNames):

    DEV = 'dev'
    TEST = 'test'
    ADM = 'adm'

    CHOICES = ((DEV, 'Developer'),
               (TEST, 'Tester'),
               (ADM, 'Administrator'))

    name = models.CharField(max_length=20, choices=CHOICES)
    description = models.TextField()

    PK = 'pk'
    NAME = 'name'
    DESCRIPTION = 'description'


class Employee(models.Model, ModelNames):
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    profession = models.ForeignKey(Profession)

    NAME = 'name'
    LAST_NAME = 'last_name'
    EMAIL = 'email'
    PROFESSION = 'profession'

    def __str__(self):
        return 'email: {}'.format(self.email)
