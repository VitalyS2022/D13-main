import datetime

from django.db import models

from django.contrib.auth.models import AbstractUser
from typing import Optional

# from message_boards.models import Advertsement


class MyUser(AbstractUser):

    MAX_NAME_LENGTH = 100

    man = "MN"
    woman = "WN"
    GENDER = [
        (man, "Мужчина"),
        (woman, "Женщина")
    ]

    id: int = models.AutoField(auto_created=True, primary_key=True, verbose_name="ID")
    username: str = models.CharField(max_length=200, blank=False, unique=True)
    email: str = models.EmailField(blank=False, db_index=True)
    full_name: str = models.CharField(max_length=MAX_NAME_LENGTH)
    birhtday: datetime.datetime = models.DateTimeField(null=True)
    gender: str = models.CharField(max_length=2, choices=GENDER, default=man)
    mailing: bool = models.BooleanField(default=False)
    is_active: bool = models.BooleanField(default=False)
    # advertsement: Advertsement = models.ForeignKey(Advertsement, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.username}"


class OneTimeCode(models.Model):
    user: Optional[MyUser] = models.OneToOneField(MyUser, null=True, on_delete=models.CASCADE)
    code: str = models.CharField(max_length=50)
