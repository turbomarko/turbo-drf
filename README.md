# Turbo DRF

[![Build Status](https://img.shields.io/actions/github/workflow/status/turbomarko/turbo-drf/ci.yml?branch=master)](https://github.com/turbomarko/turbo-drf/actions/workflows/ci.yml?query=branch%3Amaster)
[![Documentation Status](https://readthedocs.org/projects/turbo-drf/badge/?version=latest)](https://turbo-drf.readthedocs.io/en/latest/?badge=latest)
[[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/turbomarko/turbo-drf/master.svg)](https://results.pre-commit.ci/latest/github/turbomarko/turbo-drf/master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Powered by [Cookiecutter](https://github.com/cookiecutter/cookiecutter), Turbo DRF is a framework for jumpstarting production-ready Django Rest Framework projects quickly.

* Documentation: <https://turbo-drf.readthedocs.io/en/latest/>
* See [Troubleshooting](https://turbo-drf.readthedocs.io/en/latest/5-help/troubleshooting.html) for common errors and obstacles
* If you have problems with Turbo DRF, please open [issues](https://github.com/turbomarko/turbo-drf/issues/new), don't send emails to the maintainers.

## Features

- For Django 5.0
- Works with Python 3.12
- Renders Django Rest Framework projects with 100% starting test coverage
- [12-Factor](https://12factor.net) based settings via [django-environ](https://github.com/joke2k/django-environ)
- Secure by default. We believe in SSL.
- Optimized development and production settings
- Registration via [django-allauth](https://github.com/pennersr/django-allauth)
- Comes with custom user model ready to go
- Optional basic ASGI setup for Websockets
- Send emails via [Anymail](https://github.com/anymail/django-anymail) (using [Mailgun](http://www.mailgun.com/) by default or Amazon SES if AWS is selected cloud provider, but switchable)
- Media storage using Amazon S3, Google Cloud Storage or nginx
- Docker support using [docker-compose](https://github.com/docker/compose) for development and production (using [Traefik](https://traefik.io/) with [LetsEncrypt](https://letsencrypt.org/) support)
- Run tests with unittest or pytest
- Customizable PostgreSQL version
- Default integration with [pre-commit](https://github.com/pre-commit/pre-commit) for identifying simple issues before submission to code review
- Serve static files from [Whitenoise](https://whitenoise.readthedocs.io/)


## Optional Integrations

*These features can be enabled during initial project setup.*

- Configuration for [Celery](http://www.celeryproject.org/) and [Flower](https://github.com/mher/flower)
- Integration with [Mailpit](https://github.com/axllent/mailpit/) for local email testing
- Integration with [Sentry](https://sentry.io/welcome/) for error logging

## Constraints

- Only maintained 3rd party libraries are used.
- Uses PostgreSQL everywhere: 10 - 16.
- Environment variables for configuration (This won't work with Apache/mod_wsgi).


## Usage

Let's pretend you want to create a Django project called "redditclone". Rather than using `startproject`
and then editing the results to include your name, email, and various configuration issues that always get forgotten until the worst possible moment, get [cookiecutter](https://github.com/cookiecutter/cookiecutter) to do all the work.

First, get Cookiecutter. Trust me, it's awesome:

    $ pip install "cookiecutter>=1.7.0"

Now run it against this repo::

    $ cookiecutter https://github.com/turbomarko/turbo-drf

You'll be prompted for some values. Provide them, then a Django project will be created for you.

**Warning**: After this point, change 'Mark Hoffman', 'turbomarko', etc to your own information.

Answer the prompts with your own desired [options](http://turbo-drf.readthedocs.io/en/latest/1-getting-started/project-generation-options.html). For example::

    project_name [Project Name]: Reddit Clone
    project_slug [reddit_clone]: reddit
    description [Behold My Awesome Project!]: A reddit clone.
    author_name [Mark Hoffman]: Mark Hoffman
    domain_name [example.com]: myreddit.com
    email [you@example.com]: 7urbo.marko@gmail.com
    version [0.1.0]: 0.0.1
    Select open_source_license:
    1 - MIT
    2 - BSD
    3 - GPLv3
    4 - Apache Software License 2.0
    5 - Not open source
    Choose from 1, 2, 3, 4, 5 [1]: 1
    Select username_type:
    1 - username
    2 - email
    Choose from 1, 2 [1]: 1
    timezone [UTC]: America/Los_Angeles
    Select postgresql_version:
    1 - 16
    2 - 15
    3 - 14
    4 - 13
    5 - 12
    Choose from 1, 2, 3, 4, 5 [1]: 1
    Select cloud_provider:
    1 - AWS
    2 - GCP
    3 - None
    Choose from 1, 2, 3 [1]: 1
    Select mail_service:
    1 - Mailgun
    2 - Amazon SES
    3 - Mailjet
    4 - Mandrill
    5 - Postmark
    6 - Sendgrid
    7 - Brevo (formerly SendinBlue)
    8 - SparkPost
    9 - Other SMTP
    Choose from 1, 2, 3, 4, 5, 6, 7, 8, 9 [1]: 1
    use_async [n]: n
    use_celery [n]: y
    use_mailpit [n]: n
    use_sentry [n]: y
    use_whitenoise [n]: n
    Select ci_tool:
    1 - None
    2 - Travis
    3 - Gitlab
    4 - Github
    Choose from 1, 2, 3, 4 [1]: 4
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

Now take a look at your repo. Don't forget to carefully look at the generated README.

For local development, see the following:

- [Developing locally](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally.html)


## Community

If you think you found a bug or want to request a feature, please open an [issue](https://github.com/turbomarko/turbo-drf/issues).

## "Your Stuff"

Scattered throughout the Python and HTML of this project are places marked with "your stuff". This is where third-party libraries are to be integrated with your project.

## Useful articles

- [Why cookiecutter-django is Essential for Your Next Django Project](https://medium.com/@millsks/why-cookiecutter-django-is-essential-for-your-next-django-project-7d3c00cdce51) - Aug. 4, 2024
- [How to Make Your Own Django Cookiecutter Template!](https://medium.com/@FatemeFouladkar/how-to-make-your-own-django-cookiecutter-template-a753d4cbb8c2) - Aug. 10, 2023
- [Cookiecutter Django With Amazon RDS](https://haseeburrehman.com/posts/cookiecutter-django-with-amazon-rds/) - Apr, 2, 2021
- [Complete Walkthrough: Blue/Green Deployment to AWS ECS using GitHub actions](https://github.com/Andrew-Chen-Wang/cookiecutter-django-ecs-github) - June 10, 2020
- [Using cookiecutter-django with Google Cloud Storage](https://ahhda.github.io/cloud/gce/django/2019/03/12/using-django-cookiecutter-cloud-storage.html) - Mar. 12, 2019
- [cookiecutter-django with Nginx, Route 53 and ELB](https://msaizar.com/blog/cookiecutter-django-nginx-route-53-and-elb/) - Feb. 12, 2018
- [Introduction to Cookiecutter-Django](http://krzysztofzuraw.com/blog/2016/django-cookiecutter.html) - Feb. 19, 2016
- [Django and GitLab - Running Continuous Integration and tests with your FREE account](http://dezoito.github.io/2016/05/11/django-gitlab-continuous-integration-phantomjs.html) - May. 11, 2016
