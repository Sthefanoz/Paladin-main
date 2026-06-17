from django.db import migrations


# Subconjunto representativo de controles ISO/IEC 27002:2022
# (los 4 temas: Organizacional, Personas, Físico, Tecnológico).
CONTROLES = [
    ('5.1', 'Políticas de seguridad de la información', 'ORG'),
    ('5.7', 'Inteligencia de amenazas', 'ORG'),
    ('5.9', 'Inventario de información y otros activos asociados', 'ORG'),
    ('5.10', 'Uso aceptable de la información y los activos', 'ORG'),
    ('5.15', 'Control de acceso', 'ORG'),
    ('5.23', 'Seguridad de la información en servicios en la nube', 'ORG'),
    ('5.24', 'Planificación y preparación de la gestión de incidentes', 'ORG'),
    ('5.30', 'Preparación de las TIC para la continuidad del negocio', 'ORG'),
    ('6.3', 'Concienciación, educación y formación', 'PER'),
    ('6.5', 'Responsabilidades tras la terminación del empleo', 'PER'),
    ('6.7', 'Trabajo remoto', 'PER'),
    ('7.2', 'Controles de acceso físico', 'FIS'),
    ('7.4', 'Monitoreo de la seguridad física', 'FIS'),
    ('7.10', 'Medios de almacenamiento', 'FIS'),
    ('8.1', 'Dispositivos finales de usuario', 'TEC'),
    ('8.2', 'Derechos de acceso privilegiado', 'TEC'),
    ('8.5', 'Autenticación segura', 'TEC'),
    ('8.7', 'Protección contra software malicioso (malware)', 'TEC'),
    ('8.8', 'Gestión de vulnerabilidades técnicas', 'TEC'),
    ('8.12', 'Prevención de fuga de datos', 'TEC'),
    ('8.13', 'Respaldo (backup) de la información', 'TEC'),
    ('8.15', 'Registro de eventos (logging)', 'TEC'),
    ('8.16', 'Actividades de monitoreo', 'TEC'),
    ('8.23', 'Filtrado web', 'TEC'),
    ('8.24', 'Uso de criptografía', 'TEC'),
]

AMENAZAS = [
    ('Acceso no autorizado', 'MAL'),
    ('Ransomware / Malware', 'MAL'),
    ('Phishing / Ingeniería social', 'MAL'),
    ('Error humano en la operación', 'HUM'),
    ('Fallo de hardware', 'TEC'),
    ('Corte de energía', 'TEC'),
    ('Fuga de información', 'ORG'),
    ('Desastre natural (incendio, inundación)', 'NAT'),
]

VULNERABILIDADES = [
    'Contraseñas débiles o reutilizadas',
    'Software desactualizado / sin parches',
    'Ausencia de respaldos (backups)',
    'Falta de cifrado de datos sensibles',
    'Personal sin capacitación en seguridad',
    'Configuración por defecto en servidores',
    'Ausencia de control de acceso físico',
    'Falta de plan de continuidad del negocio',
]


def cargar(apps, schema_editor):
    Control = apps.get_model('riesgos', 'Control')
    Amenaza = apps.get_model('riesgos', 'Amenaza')
    Vulnerabilidad = apps.get_model('riesgos', 'Vulnerabilidad')

    for codigo, nombre, tema in CONTROLES:
        Control.objects.get_or_create(
            codigo=codigo, defaults={'nombre': nombre, 'tema': tema}
        )
    for nombre, cat in AMENAZAS:
        Amenaza.objects.get_or_create(
            nombre=nombre, defaults={'categoria': cat}
        )
    for nombre in VULNERABILIDADES:
        Vulnerabilidad.objects.get_or_create(nombre=nombre)


def borrar(apps, schema_editor):
    apps.get_model('riesgos', 'Control').objects.all().delete()
    apps.get_model('riesgos', 'Amenaza').objects.all().delete()
    apps.get_model('riesgos', 'Vulnerabilidad').objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('riesgos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(cargar, borrar),
    ]
