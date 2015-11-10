Pyuploadcare-Sqlalchemy
=======================

.. image:: https://img.shields.io/pypi/v/pyuploadcare-sqlalchemy.svg
    :target: https://pypi.python.org/pypi/pyuploadcare-sqlalchemy
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/uploadcare/pyuploadcare-sqlalchemy.svg?branch=master
    :target: https://travis-ci.org/uploadcare/pyuploadcare-sqlalchemy
    :alt: Build status

Custom fields types for SqlAlchemy which integrated with Uploadcare service.

Installation
------------

.. code:: bash

    $ pip install pyuploadcare-sqlalchemy

Usage
-----

This package similar to ``pyuploadcare.dj`` but for ``Sqlalchemy`` instead of Django's ORM. It stores Uploadcare CDN links on database's side and builds a object of ``File`` (or ``FileGroup``) on python's side (e.g you can easily use it in yours templates).

Fields types:

* ``FileType``
* ``FileGroupType``
* ``ImageType`` - Provides syntax sugar when working with images - ``effects`` - you can set default effects according by `CDN API <https://uploadcare.com/documentation/cdn/#image-operations>`_ which will be applied to uploaded image.

Also for getting started you can look at this `simplest example <https://github.com/uploadcare/pyuploadcare-sqlalchemy/tree/master/example>`_.

For install it use a command:

.. code:: bash

    $ make run_example


Contributing
------------

1. Fork the ``pyuploadcare-sqlalchemy`` repo on GitHub.
2. Clone your fork locally:

.. code:: bash

    $ git clone git@github.com:your_name_here/pyuploadcare-sqlalchemy.git

3. Install your local copy into a virtualenv. Assuming you have ``virtualenvwrapper`` installed, this is how you set up your fork for local development:

.. code:: bash

    $ mkvirtualenv pyuploadcare-sqlalchemy
    $ cd pyuploadcare-sqlalchemy/
    $ python setup.py develop

4. Create a branch for local development:

.. code:: bash

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the tests, including testing other Python versions with tox:

.. code:: bash

    $ pip install tox
    $ tox

6. Commit your changes and push your branch to GitHub:

.. code:: bash

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.
