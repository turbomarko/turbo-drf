Turbo DRF
===================

.. image:: https://img.shields.io/github/workflow/status/turbomarko/turbo-drf/CI/master
    :target: https://github.com/turbomarko/turbo-drf/actions?query=workflow%3ACI
    :alt: Build Status

.. image:: https://readthedocs.org/projects/turbo-drf/badge/?version=latest
    :target: https://turbo-drf.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/turbomarko/turbo-drf/shield.svg
    :target: https://pyup.io/repos/github/turbomarko/turbo-drf/
    :alt: Updates

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Code style: black

Powered by Cookiecutter_, Turbo DRF is a framework for jumpstarting
production-ready Django Rest Framework projects quickly.

* Documentation: https://turbo-drf.readthedocs.io/en/latest/
* See Troubleshooting_ for common errors and obstacles
* If you have problems with Turbo DRF, please open issues_ don't send
  emails to the maintainers.

.. _Troubleshooting: https://turbo-drf.readthedocs.io/en/latest/troubleshooting.html

.. _issues: https://github.com/turbomarko/turbo-drf/issues/new

Features
---------

* For Django 3.2
* Works with Python 3.9
* Renders Django Rest Framework projects with 100% starting test coverage
* 12-Factor_ based settings via django-environ_
* Secure by default. We believe in SSL.
* Optimized development and production settings
* Registration via django-allauth_
* Comes with custom user model ready to go
* Optional basic ASGI setup for Websockets
* Send emails via Anymail_ (using Mailgun_ by default or Amazon SES if AWS is selected cloud provider, but switchable)
* Media storage using Amazon S3 or Google Cloud Storage
* Docker support using docker-compose_ for development and production (using Traefik_ with LetsEncrypt_ support)
* Procfile_ for deploying to Heroku
* Instructions for deploying to PythonAnywhere_
* Run tests with unittest or pytest
* Customizable PostgreSQL version
* Default integration with pre-commit_ for identifying simple issues before submission to code review

Optional Integrations
---------------------

*These features can be enabled during initial project setup.*

* Serve static files from Amazon S3, Google Cloud Storage or Whitenoise_
* Configuration for Celery_ and Flower_
* Integration with MailHog_ for local email testing
* Integration with Sentry_ for error logging

.. _django-environ: https://github.com/joke2k/django-environ
.. _12-Factor: http://12factor.net/
.. _django-allauth: https://github.com/pennersr/django-allauth
.. _django-avatar: https://github.com/grantmcconnaughey/django-avatar
.. _Procfile: https://devcenter.heroku.com/articles/procfile
.. _Mailgun: http://www.mailgun.com/
.. _Whitenoise: https://whitenoise.readthedocs.io/
.. _Celery: http://www.celeryproject.org/
.. _Flower: https://github.com/mher/flower
.. _Anymail: https://github.com/anymail/django-anymail
.. _MailHog: https://github.com/mailhog/MailHog
.. _Sentry: https://sentry.io/welcome/
.. _docker-compose: https://github.com/docker/compose
.. _PythonAnywhere: https://www.pythonanywhere.com/
.. _Traefik: https://traefik.io/
.. _LetsEncrypt: https://letsencrypt.org/
.. _pre-commit: https://github.com/pre-commit/pre-commit

Constraints
-----------

* Only maintained 3rd party libraries are used.
* Uses PostgreSQL everywhere (10.19 - 14.1)
* Environment variables for configuration (This won't work with Apache/mod_wsgi).


PyUp
~~~~

.. image:: https://pyup.io/static/images/logo.png
   :name: pyup
   :align: center
   :alt: pyup
   :target: https://pyup.io/

PyUp brings you automated security and dependency updates used by Google and other organizations. Free for open source projects!

Usage
------

Let's pretend you want to create a Django project called "redditclone". Rather than using ``startproject``
and then editing the results to include your name, email, and various configuration issues that always get forgotten until the worst possible moment, get cookiecutter_ to do all the work.

First, get Cookiecutter. Trust me, it's awesome::

    $ pip install "cookiecutter>=1.7.0"

Now run it against this repo::

    $ cookiecutter https://github.com/turbomarko/turbo-drf

You'll be prompted for some values. Provide them, then a Django project will be created for you.

**Warning**: After this point, change 'Mark Hoffman', 'turbomarko', etc to your own information.

Answer the prompts with your own desired options_. For example::

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

* `Developing locally using docker`_

.. _options: http://turbo-drf.readthedocs.io/en/latest/project-generation-options.html
.. _`Developing locally using docker`: http://turbo-drf.readthedocs.io/en/latest/developing-locally-docker.html

Community
-----------

If you think you found a bug or want to request a feature, please open an issue_.

.. _`issue`: https://github.com/turbomarko/turbo-drf/issues

For Readers of Two Scoops of Django
--------------------------------------------

You may notice that some elements of this project do not exactly match what we describe in chapter 3. The reason for that is this project, amongst other things, serves as a test bed for trying out new ideas and concepts. Sometimes they work, sometimes they don't, but the end result is that it won't necessarily match precisely what is described in the book I co-authored.

For PyUp Users
--------------

If you are using `PyUp <https://pyup.io>`_ to keep your dependencies updated and secure, use the code *cookiecutter* during checkout to get 15% off every month.

"Your Stuff"
-------------

Scattered throughout the Python and HTML of this project are places marked with "your stuff". This is where third-party libraries are to be integrated with your project.

Releases
--------

Need a stable release? You can find them at https://github.com/turbomarko/turbo-drf/releases


Not Exactly What You Want?
---------------------------

This is what I want. *It might not be what you want.* Don't worry, you have options:

Fork This
~~~~~~~~~~

If you have differences in your preferred setup, I encourage you to fork this to create your own version.
Once you have your fork working, let me know and I'll add it to a '*Similar Cookiecutter Templates*' list here.
It's up to you whether or not to rename your fork.

If you do rename your fork, I encourage you to submit it to the following places:

* cookiecutter_ so it gets listed in the README as a template.
* The cookiecutter grid_ on Django Packages.

.. _cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _grid: https://www.djangopackages.com/grids/g/cookiecutters/

Submit a Pull Request
~~~~~~~~~~~~~~~~~~~~~~

We accept pull requests if they're small, atomic, and make our own project development
experience better.

Code of Conduct
---------------

Everyone interacting in the Cookiecutter project's codebases, issue trackers, chat
rooms, and mailing lists is expected to follow the `PyPA Code of Conduct`_.


.. _`PyPA Code of Conduct`: https://www.pypa.io/en/latest/code-of-conduct/
