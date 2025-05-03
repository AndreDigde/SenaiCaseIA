# create_superuser.py
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'regressor.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

email = os.environ.get('USER_EMAIL', 'mail@mail.com')
password = os.environ.get('USER_PASS', 'umasenha')
full_name = os.environ.get('USER_NAME', 'Um User')
phone = os.environ.get('USER_PHONE', '(00) 00000-0000')

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        username=email,
        email=email,
        password=password,
        full_name=full_name,
        phone=phone
    )
    print('First user created!')
