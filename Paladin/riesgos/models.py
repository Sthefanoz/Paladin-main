from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from activos.models import Activo


# Escala común (1-5) usada para probabilidad e impacto.
# Se mantiene coherente con la valoración CIA de los activos.
NIVEL_1_5 = [
    (1, 'Muy Bajo'),
    (2, 'Bajo'),
    (3, 'Medio'),
    (4, 'Alto'),
    (5, 'Muy Alto'),
]


class Amenaza(models.Model):
    """Catálogo de amenazas (módulo: identificación de riesgos)."""

    CATEGORIAS = [
        ('NAT', 'Natural / Desastre'),
        ('HUM', 'Error humano'),
        ('MAL', 'Ataque malicioso / Malware'),
        ('TEC', 'Fallo técnico'),
        ('ORG', 'Organizacional / Procesos'),
    ]

    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=3, choices=CATEGORIAS, default='TEC')

    class Meta:
        verbose_name = 'Amenaza'
        verbose_name_plural = 'Amenazas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Vulnerabilidad(models.Model):
    """Catálogo de vulnerabilidades (debilidades aprovechables por una amenaza)."""

    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Vulnerabilidad'
        verbose_name_plural = 'Vulnerabilidades'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Control(models.Model):
    """Control de seguridad de referencia (ISO/IEC 27002:2022)."""

    TEMAS = [
        ('ORG', 'Organizacional'),
        ('PER', 'Personas'),
        ('FIS', 'Físico'),
        ('TEC', 'Tecnológico'),
    ]

    codigo = models.CharField(max_length=20, unique=True)        # p.ej. "8.7"
    nombre = models.CharField(max_length=160)
    tema = models.CharField(max_length=3, choices=TEMAS, default='ORG')
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Control ISO 27002'
        verbose_name_plural = 'Controles ISO 27002:2022'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Riesgo(models.Model):
    """Entidad central. Cubre los módulos de identificación, valoración,
    tratamiento, riesgo residual, comunicación y monitoreo."""

    ESTRATEGIAS = [
        ('MIT', 'Mitigar'),
        ('TRA', 'Transferir'),
        ('ACE', 'Aceptar'),
        ('EVI', 'Evitar'),
    ]

    ESTADOS = [
        ('IDE', 'Identificado'),
        ('TRA', 'En tratamiento'),
        ('CON', 'Controlado'),
        ('CER', 'Cerrado'),
    ]

    # --- Identificación ---
    activo = models.ForeignKey(
        Activo, on_delete=models.CASCADE, related_name='riesgos'
    )
    amenaza = models.ForeignKey(Amenaza, on_delete=models.PROTECT)
    vulnerabilidad = models.ForeignKey(Vulnerabilidad, on_delete=models.PROTECT)
    controles_existentes = models.TextField(
        blank=True,
        help_text='Controles ya implementados antes del análisis.'
    )

    # --- Valoración del riesgo inherente (probabilidad x impacto) ---
    probabilidad = models.IntegerField(
        choices=NIVEL_1_5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    impacto = models.IntegerField(
        choices=NIVEL_1_5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    # --- Tratamiento ---
    estrategia = models.CharField(
        max_length=3, choices=ESTRATEGIAS, blank=True
    )
    controles_propuestos = models.ManyToManyField(
        Control, blank=True, related_name='riesgos'
    )
    responsable = models.CharField(max_length=120, blank=True)

    # --- Riesgo residual (tras aplicar controles) ---
    probabilidad_residual = models.IntegerField(
        choices=NIVEL_1_5, null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    impacto_residual = models.IntegerField(
        choices=NIVEL_1_5, null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    # --- Comunicación y consulta ---
    observaciones = models.TextField(
        blank=True,
        help_text='Observaciones o recomendaciones para las partes interesadas.'
    )

    # --- Monitoreo y supervisión ---
    estado = models.CharField(max_length=3, choices=ESTADOS, default='IDE')

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Riesgo'
        verbose_name_plural = 'Riesgos'
        ordering = ['-fecha_actualizacion']

    def __str__(self):
        return f'{self.activo.nombre} / {self.amenaza.nombre}'

    # ----- Cálculos -----
    @staticmethod
    def _clasificar(nivel):
        """Traduce un nivel numérico (1-25) a una categoría cualitativa."""
        if nivel is None:
            return None
        if nivel <= 4:
            return 'Bajo'
        if nivel <= 9:
            return 'Medio'
        if nivel <= 15:
            return 'Alto'
        return 'Crítico'

    @property
    def nivel_riesgo(self):
        """Riesgo inherente = probabilidad x impacto (rango 1-25)."""
        return self.probabilidad * self.impacto

    @property
    def nivel_riesgo_texto(self):
        return self._clasificar(self.nivel_riesgo)

    @property
    def riesgo_residual(self):
        """Riesgo residual = prob. residual x impacto residual (si está definido)."""
        if self.probabilidad_residual and self.impacto_residual:
            return self.probabilidad_residual * self.impacto_residual
        return None

    @property
    def riesgo_residual_texto(self):
        return self._clasificar(self.riesgo_residual)

    @property
    def reduccion(self):
        """Reducción absoluta del nivel de riesgo lograda por el tratamiento."""
        if self.riesgo_residual is not None:
            return self.nivel_riesgo - self.riesgo_residual
        return None
