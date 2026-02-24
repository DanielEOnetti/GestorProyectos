# Gestor de Proyectos con Roles - Django

Aplicación para colaborar en proyectos con roles definidos (Admin, Lector), gestión de tareas y chat en tiempo real.

## Funcionalidades
* **Roles:** Sistema de permisos granular (Admin edita, Lector solo ve).
* **Dashboard:** Vista general con barra de progreso visual.
* **Tareas:** Asignación y marcado de completado (solo con permiso).
* **Chat:** Mensajería interna por proyecto.

## Instalación

1. Clonar el repositorio.
2. Crear entorno virtual y activarlo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # O venv\Scripts\activate en Windows

3. Instalar dependencias
    pip install -r requirements.txt

4. Aplicar migraciones
    python manage.py migrate

5. (Opcional) Cargar datos de prueba
    python manage.py loaddata datos_iniciales.json

6. Si no cargargaste los datos, crear un superusuario
    python manage.py createsuperuser

7. Ejecutar servidor
    python manage.py runserver

Usuarios de Prueba (si cargaste datos)
Admin: Dani / (1234dani)

Usuario: Pepe / (pepe1234)