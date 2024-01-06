from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass  # TODO check if anything else can come here

    def __str__(self):
        return self.username
