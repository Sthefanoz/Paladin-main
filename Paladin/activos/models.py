from django.db import models

class Activo(models.Model):

    NIVEL_CIA = [
        (1, 'Muy Bajo'),
        (2, 'Bajo'),
        (3, 'Medio'),
        (4, 'Alto'),
        (5, 'Muy Alto'),
    ]

    TIPOS_ACTIVO = [
        ('HW', 'Hardware'),
        ('SW', 'Software'),
        ('INF', 'Información'),
        ('SER', 'Servicio'),
        ('PER', 'Personal'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    tipo = models.CharField(
        max_length=10,
        choices=TIPOS_ACTIVO
    )

    confidencialidad = models.IntegerField(
        choices=NIVEL_CIA
    )

    integridad = models.IntegerField(
        choices=NIVEL_CIA
    )

    disponibilidad = models.IntegerField(
        choices=NIVEL_CIA
    )

    @property
    def valor_total(self):
        return (
            self.confidencialidad +
            self.integridad +
            self.disponibilidad
        )