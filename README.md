# django-unchained

this readme is for the django-unchained project. how to start the project and the project structure.

## how to start the project

1. clone the project

```bash
git clone https://github.com/your-username/django-unchained.git
```

2. create a virtual environment

```bash
python -m venv env
```

3. create a .env file and add the following from .env.example

4. install the dependencies

```bash
pip install -r requirements.txt
```

5. migrate the database

```bash
cd core
python manage.py makemigrations
python manage.py migrate
```

6. run the project

```bash
python manage.py runserver
```

# Here's Project Folder Structure

```bash
core/
    core/ -- django core app
    manage.py -- django manage file
    settings.py -- django settings file
    urls.py
    wsgi.py -- django wsgi file
    README.md -- this file
    .env -- django environment variables
    .gitignore -- git ignore file
    .env.example
    requirements.txt
    custom_auth/ -- custom auth app
       serializers.py -- custom auth serializers
       urls.py -- custom auth urls
       views.py -- custom auth views
       models.py -- custom auth models
    projects/ -- projects app
       models.py -- projects models
       permissions.py -- projects permissions
       serializers.py -- projects serializers
       urls.py -- projects urls
       views.py -- projects views
    README.md -- this file
    requirements.txt -- project dependencies
```
