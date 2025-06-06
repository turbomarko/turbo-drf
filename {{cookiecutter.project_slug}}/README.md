# {{cookiecutter.project_name}}

{{ cookiecutter.description }}

[![Built with Turbo DRF](https://img.shields.io/badge/built%20with-Turbo%20DRF-ff69b4.svg?logo=cookiecutter)](https://github.com/turbomarko/turbo-drf/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

{%- if cookiecutter.open_source_license != "Not open source" %}

License: {{cookiecutter.open_source_license}}
{%- endif %}

## Settings

Moved to [settings](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html).

## Basic Commands

### Creating apps

To create a **new app**, run the following command from inside the project root::

    $ docker compose -f local.yml run --rm django python manage.py startapp --template=./template_app myappname

After creating the app, move it to the **api** folder.
You can add the new app to the project by extending the LOCAL_APPS list in the base settings file with the value **api.myappname**.

These templates can be customized to suit the project needs. (see [startapp](https://docs.djangoproject.com/en/dev/ref/django-admin/#startapp))

### Setting Up Your Superuser

To create a **superuser account**, use this command:

    $ docker compose -f local.yml run --rm django python manage.py createsuperuser

### Type checks

Running type checks with mypy:

    $ docker compose -f local.yml run --rm django mypy api

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ docker compose -f local.yml run --rm django coverage run -m pytest
    $ docker compose -f local.yml run --rm django coverage html

#### Running tests with pytest

    $ docker compose -f local.yml run --rm django pytest
{%- if cookiecutter.use_celery == "y" %}

### Celery

This app comes with Celery. The docker compose command will automatically run a celery worker for you.

To run a celery worker:

```bash
cd {{cookiecutter.project_slug}}
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd {{cookiecutter.project_slug}}
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd {{cookiecutter.project_slug}}
celery -A config.celery_app worker -B -l info
```

{%- endif %}
{%- if cookiecutter.use_mailpit == "y" %}

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [Mailpit](https://github.com/axllent/mailpit) with a web interface is available as docker container.

Container mailpit will start automatically when you will run all docker containers.
Please check [cookiecutter-django Docker documentation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally.html) for more details how to start all containers.

With Mailpit running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`
{%- endif %}
{%- if cookiecutter.use_sentry == "y" %}

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.
{%- endif %}

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](https://cookiecutter-django.readthedocs.io/en/latest/3-deployment/deployment-with-docker.html).
