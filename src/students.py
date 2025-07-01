import os
import random
from faker import Faker
from jinja2 import Template
import uuid

# Inicializar Faker
faker = Faker('es_ES')

# Template Jinja
TEMPLATE = """
REPORTE DE CALIFICACIONES DEL ALUMNO

Nombre del alumno: {{ alumno.nombre }}
ID del alumno: {{ alumno.id }}

{% for registro in alumno.registros %}
Escuela: {{ registro.escuela }}
Fecha: {{ registro.fecha }}

Materias:
{% for materia in registro.materias %}
  - {{ materia.nombre }}: {{ materia.calificacion }} {% if materia.comentarios %}({{ materia.comentarios }}){% endif %}
{% endfor %}

{% endfor %}
"""

# Lista de materias de ejemplo
MATERIAS = ["Matemáticas", "Ciencias", "Lengua", "Historia", "Arte", "Educación Física"]

# Generador de datos para un alumno
def generar_alumno():
    alumno = {
        "nombre": faker.name(),
        "id": faker.unique.random_int(min=0, max=30000),
        "registros": []
    }

    # Número aleatorio de registros académicos
    for _ in range(1):
        registro = {
            "escuela": faker.company(),
            "fecha": faker.date(),
            "materias": []
        }

        # Materias aleatorias por registro
        for materia in random.sample(MATERIAS, k=random.randint(3, 6)):
            registro["materias"].append({
                "nombre": materia,
                "calificacion": random.randint(5, 10),
                "comentarios": faker.sentence() if random.random() < 0.4 else ""
            })

        alumno["registros"].append(registro)

    return alumno

# Función principal para generar N reportes


def generar_reportes(n, carpeta_destino="./src/students_report"):
    template = Template(TEMPLATE)

    for i in range(n):
        alumno = generar_alumno()
        contenido = template.render(alumno=alumno)
        uuid_ = str(uuid.uuid4())
        filename = f"{carpeta_destino}/{uuid_}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(contenido)

    print(f"{n} reportes generados en la carpeta '{carpeta_destino}'.")


# Ejecutar
if __name__ == "__main__":
    print("Generando reportes")
    generar_reportes(10000)  # Cambia el número según lo que necesites
