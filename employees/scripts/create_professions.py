
def create_professions():
    from employees.models import Profession
    professions = [Profession(name=Profession.DEV,
                              description="Developer position. Is responsible for writing code"),
                   Profession(name=Profession.ADM,
                              description="Administrator position. Is responsible for local network"),
                   Profession(name=Profession.TEST,
                              description="Tester position. Is responsible for testing company products")
                   ]

    for profession in professions:
        profession.save()

    return professions


if __name__ == '__main__':
    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company_management.settings")  # copy from manage.py
    os.environ["DJANGO_SETTINGS_MODULE"] = "company_management.settings"
    import django

    django.setup()
    create_professions()
