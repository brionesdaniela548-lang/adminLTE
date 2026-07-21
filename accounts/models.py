from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    SECURITY_QUESTIONS = [
        (
            "mascota",
            "¿Cuál era el nombre de tu primera mascota?",
        ),
        (
            "ciudad",
            "¿En qué ciudad naciste?",
        ),
        (
            "escuela",
            "¿Cuál era el nombre de tu primera escuela?",
        ),
        (
            "amigo",
            "¿Cuál era el nombre de tu mejor amigo de la infancia?",
        ),
        (
            "comida",
            "¿Cuál es tu comida favorita?",
        ),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    foto = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
        verbose_name="Foto de perfil",
    )

    pregunta_seguridad = models.CharField(
        max_length=50,
        choices=SECURITY_QUESTIONS,
        blank=True,
        default="",
        verbose_name="Pregunta de seguridad",
    )

    respuesta_seguridad = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Respuesta de seguridad",
    )

    def __str__(self):
        return self.user.username