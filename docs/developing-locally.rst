Setting Up and Running Locally With Docker
==========================================

.. index:: Docker

.. note::

    If you're new to Docker, please be aware that some resources are cached system-wide
    and might reappear if you generate a project multiple times with the same name (e.g.
    :ref:`this issue with Postgres <docker-postgres-auth-failed>`).


Prerequisites
-------------

* Docker; if you don't have it yet, follow the `installation instructions`_;
* Docker Compose; refer to the official documentation for the `installation guide`_.
* Pre-commit; refer to the official documentation for the `pre-commit`_.
* Cookiecutter; refer to the official GitHub repository of `Cookiecutter`_

.. _`installation instructions`: https://docs.docker.com/install/#supported-platforms
.. _`installation guide`: https://docs.docker.com/compose/install/
.. _`pre-commit`: https://pre-commit.com/#install
.. _`Cookiecutter`: https://github.com/cookiecutter/cookiecutter

Before Getting Started
----------------------
.. include:: generate-project-block.rst

Build the Stack
---------------

This can take a while, especially the first time you run this particular command on your development system::

    $ docker compose -f docker-compose.local.yml build

Generally, if you want to emulate production environment use ``docker-compose.production.yml`` instead. And this is true for any other actions you might need to perform: whenever a switch is required, just do it!

Before doing any git commit, `pre-commit`_ should be installed globally on your local machine, and then::

    $ git init
    $ pre-commit install

Failing to do so will result with a bunch of CI and Linter errors that can be avoided with pre-commit.

Run the Stack
-------------

This brings up both Django and PostgreSQL. The first time it is run it might take a while to get started, but subsequent runs will occur quickly.

Open a terminal at the project root and run the following for local development::

    $ docker compose -f docker-compose.local.yml up

You can also set the environment variable ``COMPOSE_FILE`` pointing to ``docker-compose.local.yml`` like this::

    $ export COMPOSE_FILE=docker-compose.local.yml

And then run::

    $ docker compose up

To run in a detached (background) mode, just::

    $ docker compose up -d

These commands don't run the docs service. In order to run docs service you can run::

    $ docker compose -f docker-compose.docs.yml up

To run the docs with local services just use::

    $ docker compose -f docker-compose.local.yml -f docker-compose.docs.yml up

Execute Management Commands
---------------------------

As with any shell command that we wish to run in our container, this is done using the ``docker compose -f docker-compose.local.yml run --rm`` command: ::

    $ docker compose -f docker-compose.local.yml run --rm django python manage.py migrate
    $ docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser

Here, ``django`` is the target service we are executing the commands against.
Also, please note that the ``docker exec`` does not work for running management commands.


(Optionally) Designate your Docker Development Server IP
--------------------------------------------------------

When ``DEBUG`` is set to ``True``, the host is validated against ``['localhost', '127.0.0.1', '[::1]']``. This is adequate when running a ``virtualenv``. For Docker, in the ``config.settings.local``, add your host development server IP to ``INTERNAL_IPS`` or ``ALLOWED_HOSTS`` if the variable exists.

.. _envs:

Configuring the Environment
---------------------------

This is the excerpt from your project's ``docker-compose.local.yml``: ::

  # ...

  postgres:
    build:
      context: .
      dockerfile: ./compose/production/postgres/Dockerfile
    volumes:
      - {{ cookiecutter.project_slug }}_local_postgres_data:/var/lib/postgresql/data
      - {{ cookiecutter.project_slug }}_local_postgres_data_backups:/backups
    env_file:
      - ./.envs/.local/.postgres

  # ...

The most important thing for us here now is ``env_file`` section enlisting ``./.envs/.local/.postgres``. Generally, the stack's behavior is governed by a number of environment variables (`env(s)`, for short) residing in ``envs/``, for instance, this is what we generate for you: ::

    .envs
    ├── .local
    │   ├── .django
    │   └── .postgres
    └── .production
        ├── .django
        └── .postgres

By convention, for any service ``sI`` in environment ``e`` (you know ``someenv`` is an environment when there is a ``someenv.yml`` file in the project root), given ``sI`` requires configuration, a ``.envs/.e/.sI`` `service configuration` file exists.

Consider the aforementioned ``.envs/.local/.postgres``: ::

    # PostgreSQL
    # ------------------------------------------------------------------------------
    POSTGRES_HOST=postgres
    POSTGRES_DB=<your project slug>
    POSTGRES_USER=XgOWtQtJecsAbaIyslwGvFvPawftNaqO
    POSTGRES_PASSWORD=jSljDz4whHuwO3aJIgVBrqEml5Ycbghorep4uVJ4xjDYQu0LfuTZdctj7y0YcCLu

The three envs we are presented with here are ``POSTGRES_DB``, ``POSTGRES_USER``, and ``POSTGRES_PASSWORD`` (by the way, their values have also been generated for you). You might have figured out already where these definitions will end up; it's all the same with ``django`` service container envs.

One final touch: should you ever need to merge ``.envs/.production/*`` in a single ``.env`` run the ``merge_production_dotenvs_in_dotenv.py``: ::

    $ python merge_production_dotenvs_in_dotenv.py

The ``.env`` file will then be created, with all your production envs residing beside each other.


Tips & Tricks
-------------

Activate a Docker Machine
~~~~~~~~~~~~~~~~~~~~~~~~~

This tells our computer that all future commands are specifically for the dev1 machine. Using the ``eval`` command we can switch machines as needed.::

    $ eval "$(docker-machine env dev1)"

Add 3rd party python packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To install a new 3rd party python package, you cannot use ``pip install <package_name>``, that would only add the package to the container. The container is ephemeral, so that new library won't be persisted if you run another container. Instead, you should modify the Docker image:
You have to modify the relevant requirement file: base, local or production by adding: ::

    <package_name>==<package_version>

To get this change picked up, you'll need to rebuild the image(s) and restart the running container: ::

    docker compose -f docker-compose.local.yml build
    docker compose -f docker-compose.local.yml up

Debugging
~~~~~~~~~

ipdb
"""""

If you are using the following within your code to debug: ::

    import ipdb; ipdb.set_trace()

Then you may need to run the following for it to work as desired: ::

    $ docker compose -f docker-compose.local.yml run --rm --service-ports django


django-debug-toolbar
""""""""""""""""""""

In order for ``django-debug-toolbar`` to work designate your Docker Machine IP with ``INTERNAL_IPS`` in ``local.py``.


docker
""""""

The ``container_name`` from the yml file can be used to check on containers with docker commands, for example: ::

    $ docker logs <project_slug>_local_celeryworker
    $ docker top <project_slug>_local_celeryworker

Notice that the ``container_name`` is generated dynamically using your project slug as a prefix

Mailpit
~~~~~~~

When developing locally you can go with Mailpit_ for email testing provided ``use_mailpit`` was set to ``y`` on setup. To proceed,

#. make sure ``<project_slug>_local_mailpit`` container is up and running;

#. open up ``http://127.0.0.1:8025``.

.. _Mailpit: https://github.com/axllent/mailpit/

.. _`CeleryTasks`:

Celery tasks in local development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When using docker, the task scheduler will be used by default.

If you need tasks to be executed on the main thread during development set ``CELERY_TASK_ALWAYS_EAGER = True`` in ``config/settings/local.py``.

Possible uses could be for testing, or ease of profiling with DJDT.

.. _`CeleryFlower`:

Celery Flower
~~~~~~~~~~~~~

`Flower`_ is a "real-time monitor and web admin for Celery distributed task queue".

Prerequisites:

* ``use_celery`` was set to ``y`` on project initialization.

By default, it's enabled both in local and production environments (``docker-compose.local.yml`` and ``docker-compose.production.yml`` Docker Compose configs, respectively) through a ``flower`` service. For added security, ``flower`` requires its clients to provide authentication credentials specified as the corresponding environments' ``.envs/.local/.django`` and ``.envs/.production/.django`` ``CELERY_FLOWER_USER`` and ``CELERY_FLOWER_PASSWORD`` environment variables. Check out ``localhost:5555`` and see for yourself.

.. _`Flower`: https://github.com/mher/flower

(Optionally) Developing locally with HTTPS
------------------------------------------

Nginx
~~~~~

If you want to add some sort of social authentication with a OAuth provider such as Facebook, securing your communication to the local development environment will be necessary. These providers usually require that you use an HTTPS URL for the OAuth redirect URL for the Facebook login to work appropriately.

Here is a link to an article on `how to add HTTPS using Nginx`_ to your local docker installation. This also includes how to serve files from the ``media`` location, in the event that you are want to serve user-uploaded content.

.. _`how to add HTTPS using Nginx`: https://afroshok.com/cookiecutter-https
