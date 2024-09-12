# Invera Todo Challenge

# Consideraciones
1. Use Django Rest para manejar la API, Django Filter para manejar los filtros.
2. Token based authentication por simplicidad.
3. Sqlite como base de datos por simplicidad.
4. No llegue a hacer una interfaz grafica, pero se puede testear con curl/postman/httpie/etc.

# Instalacion manual
   * `git clone git@github.com:dsocolobsky/invera-todo-challenge.git`
   * `cd invera-todo-challenge`
   * `python3 -m venv .venv`
   * `source venv/bin/activate`
   * `python3 -m pip install -r requirements.txt`
   * `python3 manage.py migrate`
   * `python3 manage.py createsuperuser --username admin --email admin@example.com`
   * `python3 manage.py runserver`
* El servidor ahora esta corriendo en `http://localhost:8000`
* Para correr los tests: `python3 manage.py test`

# Instalacion mediante Docker
* `git clone git@github.com:dsocolobsky/invera-todo-challenge.git`
* `cd invera-todo-challenge`
* `docker build -t invera-todo-app .`
* `docker run -d -p 8000:8000 invera-todo-app`
* El servidor ahora esta corriendo en `http://localhost:8000`

Para correr las migraciones y crear el superuser:
* `docker exec -it <container_id> bash`
* `python3 manage.py migrate`
* `python3 manage.py createsuperuser --username admin --email admin@example.com`

## Endpoints de la API

### Autenticación

- **Registro de usuario**
  - URL: `/register/`
  - Método: POST
  - Datos requeridos: `username`, `password`

- **Obtener token de autenticación**
  - URL: `/auth-token-create/`
  - Método: POST
  - Datos requeridos: `username`, `password`

Devuelve un objeto con el token del usuario en el campo `token`.
Este token debe ser usado como header de `Authorization` en los siguientes endpoints.
`Authorization: Bearer <token>`

### Tareas

- **Listar tareas del usuario**
  - URL: `/tasks/`
  - Método: GET
  - Autenticación: Requerida
  - Parámetros opcionales de filtrado:
    - `completed`: true/false
    - `title`: Busca en el titulo de la tarea
    - `details`: Busca en el detalle de la tarea
    - `created_at`: YYYY-MM-DD

- **Crear nueva tarea para el usuario**
  - URL: `/tasks/`
  - Método: POST
  - Autenticación: Requerida
  - Datos requeridos: `title`, `details`
  - Datos opcionales: `completed`

- **Actualizar una tarea**
  - URL: `/tasks/:task_id/`
  - Método: PATCH
  - Autenticación: Requerida
  - Datos opcionales: `title`, `details`, `completed`

- **Eliminar una tarea**
  - URL: `/tasks/:task_id/`
  - Método: DELETE
  - Autenticación: Requerida

### Administración (solo para usuario con token de admin)

- **Listar todos los usuarios**
  - URL: `/users/`
  - Método: GET
  - Autenticación: Requerida (solo admin)

- **Listar todas las tareas**
  - URL: `/all-tasks/`
  - Método: GET
  - Autenticación: Requerida (solo admin)
