from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    PREGUNTAS = [
        ("mascota", "¿Cuál fue el nombre de tu primera mascota?"),
        ("escuela", "¿Cuál fue el nombre de tu escuela primaria?"),
        ("ciudad", "¿En qué ciudad naciste?"),
        ("madre", "¿Cuál es el segundo nombre de tu madre?"),
        ("comida", "¿Cuál es tu comida favorita?"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    security_question = models.CharField(
        max_length=50,
        choices=PREGUNTAS
    )

    security_answer = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.user.username