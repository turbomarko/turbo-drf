# Turbo DRF

[![Build Status](https://img.shields.io/github/workflow/status/turbomarko/turbo-drf/CI/master)](https://github.com/turbomarko/turbo-drf/actions?query=workflow%3ACI)
[![Documentation Status](https://readthedocs.org/projects/turbo-drf/badge/?version=latest)](https://turbo-drf.readthedocs.io/en/latest/?badge=latest)
[![Updates](https://pyup.io/repos/github/turbomarko/turbo-drf/shield.svg)](https://pyup.io/repos/github/turbomarko/turbo-drf/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Powered by [Cookiecutter](https://github.com/cookiecutter/cookiecutter), Turbo DRF is a framework for jumpstarting production-ready Django Rest Framework projects quickly.

* Documentation: <https://turbo-drf.readthedocs.io/en/latest/>
* See [Troubleshooting](https://turbo-drf.readthedocs.io/en/latest/troubleshooting.html) for common errors and obstacles
* If you have problems with Turbo DRF, please open [issues](https://github.com/turbomarko/turbo-drf/issues/new) don't send emails to the maintainers.

## Features

-   For Django 3.2
-   Works with Python 3.9
-   Renders Django Rest Framework projects with 100% starting test coverage
-   [12-Factor](http://12factor.net/) based settings via [django-environ](https://github.com/joke2k/django-environ)
-   Secure by default. We believe in SSL.
-   Optimized development and production settings
-   Registration via [django-allauth](https://github.com/pennersr/django-allauth)
-   Comes with custom user model ready to go
-   Optional basic ASGI setup for Websockets
-   Optional custom static build using Gulp and livereload
-   Send emails via [Anymail](https://github.com/anymail/django-anymail) (using [Mailgun](http://www.mailgun.com/) by default or Amazon SES if AWS is selected cloud provider, but switchable)
-   Media storage using Amazon S3 or Google Cloud Storage
-   Docker support using [docker-compose](https://github.com/docker/compose) for development and production (using [Traefik](https://traefik.io/) with [LetsEncrypt](https://letsencrypt.org/) support)
-   [Procfile](https://devcenter.heroku.com/articles/procfile) for deploying to Heroku
-   Instructions for deploying to [PythonAnywhere](https://www.pythonanywhere.com/)
-   Run tests with unittest or pytest
-   Customizable PostgreSQL version
-   Default integration with [pre-commit](https://github.com/pre-commit/pre-commit) for identifying simple issues before submission to code review


## Optional Integrations

*These features can be enabled during initial project setup.*

-   Serve static files from Amazon S3, Google Cloud Storage or [Whitenoise](https://whitenoise.readthedocs.io/)
-   Configuration for [Celery](http://www.celeryproject.org/) and [Flower](https://github.com/mher/flower) (the latter in Docker setup only)
-   Integration with [MailHog](https://github.com/mailhog/MailHog) for local email testing
-   Integration with [Sentry](https://sentry.io/welcome/) for error logging

## Constraints

-   Only maintained 3rd party libraries are used.
-   Uses PostgreSQL everywhere (10.19 - 14.1)
-   Environment variables for configuration (This won't work with Apache/mod_wsgi).


### PyUp

<p align="center">
  <a href="https://pyup.io/"><img src="https://pyup.io/static/images/logo.png"></a>
</p>

PyUp brings you automated security and dependency updates used by Google and other organizations. Free for open source projects!

## Usage

Let's pretend you want to create a Django project called "redditclone". Rather than using `startproject`
and then editing the results to include your name, email, and various configuration issues that always get forgotten until the worst possible moment, get [cookiecutter](https://github.com/cookiecutter/cookiecutter) to do all the work.

First, get Cookiecutter. Trust me, it's awesome:

    $ pip install "cookiecutter>=1.7.0"

Now run it against this repo::

    $ cookiecutter https://github.com/turbomarko/turbo-drf

You'll be prompted for some values. Provide them, then a Django project will be created for you.

**Warning**: After this point, change 'Mark Hoffman', 'turbomarko', etc to your own information.

Answer the prompts with your own desired [options](http://turbo-drf.readthedocs.io/en/latest/project-generation-options.html). For example::

    project_name [Project Name]: Reddit Clone
    project_slug [reddit_clone]: reddit
    author_name [Mark Hoffman]: Mark Hoffman
    email [you@example.com]: 7urbo.marko@gmail.com
    description [Behold My Awesome Project!]: A reddit clone.
    domain_name [example.com]: myreddit.com
    version [0.1.0]: 0.0.1
    timezone [UTC]: America/Los_Angeles
    use_whitenoise [n]: n
    use_celery [n]: y
    use_mailhog [n]: n
    use_sentry [n]: y
    use_heroku [n]: y
    Select postgresql_version:
    1 - 14.1
    2 - 13.5
    3 - 12.9
    4 - 11.14
    5 - 10.19
    Choose from 1, 2, 3, 4, 5 [1]: 1
    Choose from 1, 2 [1]: 1
    Select cloud_provider:
    1 - AWS
    2 - GCP
    3 - None
    Choose from 1, 2, 3 [1]: 1
    Select open_source_license:
    1 - MIT
    2 - BSD
    3 - GPLv3
    4 - Apache Software License 2.0
    5 - Not open source
    Choose from 1, 2, 3, 4, 5 [1]: 1
    keep_local_envs_in_vcs [y]: y
    debug[n]: n

Enter the project and take a look around::

    $ cd reddit/
    $ ls

Create a git repo and push it there::

    $ git init
    $ git add .
    $ git commit -m "first awesome commit"
    $ git remote add origin git@github.com:turbomarko/redditclone.git
    $ git push -u origin master

Now take a look at your repo. Don't forget to carefully look at the generated README. Awesome, right?

For local development, see the following:

-   [Developing locally using docker](http://turbo-drf.readthedocs.io/en/latest/developing-locally-docker.html)

## Community

If you think you found a bug or want to request a feature, please open an [issue](https://github.com/turbomarko/turbo-drf/issues).

## For PyUp Users

If you are using [PyUp](https://pyup.io) to keep your dependencies updated and secure, use the code *cookiecutter* during checkout to get 15% off every month.

## "Your Stuff"

Scattered throughout the Python and HTML of this project are places marked with "your stuff". This is where third-party libraries are to be integrated with your project.

## Releases

Need a stable release? You can find them at https://github.com/turbomarko/turbo-drf/releases

### Submit a Pull Request

We accept pull requests if they're small, atomic, and make our own project development
experience better.

## Code of Conduct

Everyone interacting in the Cookiecutter project's codebases, issue trackers, chat
rooms, and mailing lists is expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).
