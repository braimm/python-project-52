# from django.db import models
from django.contrib.auth.models import User

# Переопределяем метод __str__ у встроенной модели User
User.__str__ = lambda self: \
    f"{self.first_name} \
        {self.last_name}".strip() or self.username
