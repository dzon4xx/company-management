import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company_management.settings") #copy from manage.py
os.environ["DJANGO_SETTINGS_MODULE"] = "company_management.settings"
import django
django.setup()

from employees.models import Employee, Profession
import random


def random_number(min, max, numbers=set()):
    number = random.randint(min, max)
    if number in numbers:
        while number in numbers:
            number = random.randint(min, max)
    numbers.add(number)
    return number


names = ['john', 'test', 'user', 'bot', 'someguy']
last_names = ['Doe', 'Kowalski', 'Smith', 'White']
hosts = ['gmail.com', 'yahoo.com', 'wp.pl', 'o2.pl']

professions = list(Profession.objects.all())

for i in range(20):

    name = random.choice(names)
    last_name = random.choice(last_names)
    email = '@'.join([name + str(random_number(0, 300)), random.choice(hosts)])

    e = Employee(name=name,
                 last_name=last_name,
                 email=email,
                 profession=random.choice(professions))
    # print(name, last_name, email)
    e.save()


