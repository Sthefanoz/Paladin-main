from django.db import migrations


# Ejemplos de CVE asociados a vulnerabilidades ya cargadas.
CVES = {
    'Software desactualizado / sin parches': 'CVE-2021-44228',
    'Configuración por defecto en servidores': 'CVE-2020-1472',
    'Falta de cifrado de datos sensibles': 'CVE-2014-0160',
}


def cargar(apps, schema_editor):
    Vulnerabilidad = apps.get_model('riesgos', 'Vulnerabilidad')
    for nombre, cve in CVES.items():
        Vulnerabilidad.objects.filter(nombre=nombre).update(cve=cve)


def borrar(apps, schema_editor):
    Vulnerabilidad = apps.get_model('riesgos', 'Vulnerabilidad')
    Vulnerabilidad.objects.filter(nombre__in=CVES.keys()).update(cve='')


class Migration(migrations.Migration):

    dependencies = [
        ('riesgos', '0003_riesgo_fecha_control_riesgo_fecha_tratamiento_and_more'),
    ]

    operations = [
        migrations.RunPython(cargar, borrar),
    ]
