from django.contrib.auth.models import User
from django.test import TestCase


class SimpleContentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='user1',
            is_staff=True,
            is_superuser=True
        )
        self.user.set_password('passW0rdForUser1#')
