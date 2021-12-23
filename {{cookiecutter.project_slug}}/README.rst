{{cookiecutter.project_name}}
{{ '=' * cookiecutter.project_name|length }}

{{cookiecutter.description}}

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/turbomarko/turbo-drf/
     :alt: Built with Turbo DRF
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style
{%- if cookiecutter.open_source_license != "Not open source" %}

:License: {{cookiecutter.open_source_license}}
{%- endif %}

Settings
--------

Moved to settings_.

.. _settings: http://turbo-drf.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Creating apps
^^^^^^^^^^^^^

* To create a **simple app**, run the following command from inside the project root::

    $ docker-compose -f local.yml run --rm django python manage.py startapp --template=../template_apps/simple myappname

* To create a **composite app** with an additional service layer, use the following command::

    $ docker-compose -f local.yml run --rm django python manage.py startapp --template=../template_apps/composite myappname

After creating the app, move it to the {{ cookiecutter.project_slug }} folder.
You can add the new app to the project by extending the LOCAL_APPS list in the base settings file with the value {{ cookiecutter.project_slug }}.myappname.

These templates can be customized to suit the project needs. (see `startapp`_)

.. _startapp: https://docs.djangoproject.com/en/dev/ref/django-admin/#startapp

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ docker-compose -f local.yml run --rm django python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ docker-compose -f local.yml run --rm django mypy {{cookiecutter.project_slug}}

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ docker-compose -f local.yml run --rm django coverage run -m pytest
    $ docker-compose -f local.yml run --rm django coverage html
    $ docker-compose -f local.yml run --rm django open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ docker-compose -f local.yml run --rm django pytest
{%- if cookiecutter.use_celery == "y" %}

Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd {{cookiecutter.project_slug}}
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.

{%- endif %}
{%- if cookiecutter.use_mailhog == "y" %}

Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server `MailHog`_ with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check `turbo-drf Docker documentation`_ for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to ``http://127.0.0.1:8025``

.. _mailhog: https://github.com/mailhog/MailHog
{%- endif %}
{%- if cookiecutter.use_sentry == "y" %}

Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at  https://sentry.io/signup/?code=cookiecutter  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.
{%- endif %}

Deployment
----------

The following details how to deploy this application.
{%- if cookiecutter.use_heroku.lower() == "y" %}

Heroku
^^^^^^

See detailed `turbo-drf Heroku documentation`_.

.. _`turbo-drf Heroku documentation`: http://turbo-drf.readthedocs.io/en/latest/deployment-on-heroku.html
{%- endif %}

Docker
^^^^^^

See detailed `turbo-drf Docker documentation`_.

.. _`turbo-drf Docker documentation`: http://turbo-drf.readthedocs.io/en/latest/deployment-with-docker.html
