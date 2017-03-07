import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "company_management.settings") #copy from manage.py
os.environ["DJANGO_SETTINGS_MODULE"] = "company_management.settings"
import django
django.setup()

from django.contrib.auth.models import User

User.objects.create_superuser(username='test', password='test', email='test@test.test')