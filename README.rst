.. image:: http://www.repostatus.org/badges/latest/wip.svg
    :target: http://www.repostatus.org/#wip
    :alt: Project Status: WIP — Initial development is in progress, but there
          has not yet been a stable, usable release suitable for the public.

.. image:: https://travis-ci.org/jwodder/pypi-simple.svg?branch=master
    :target: https://travis-ci.org/jwodder/pypi-simple

.. image:: https://codecov.io/gh/jwodder/pypi-simple/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/pypi-simple

.. image:: https://img.shields.io/github/license/jwodder/pypi-simple.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/pypi-simple>`_
| `Issues <https://github.com/jwodder/pypi-simple/issues>`_

A client library for PyPI's Simple Repository API as specified in `PEP 503
<https://www.python.org/dev/peps/pep-0503/>`_.


API
===

``PyPISimple``
--------------

A client for fetching package information from a Python simple package
repository

``PyPISimple(endpoint=pypi_simple.PYPI_SIMPLE_ENDPOINT)``
   Create a new ``PyPISimple`` object for querying the simple API instance at
   ``endpoint``.  The endpoint defaults to PyPI's simple API at
   <https://pypi.org/simple/>.

``client.get_projects()``
   Returns a generator of names of projects available in the repository.
   The names are not normalized.

   .. warning::

       PyPI's project index file is very large and takes several seconds
       to parse.  Use this method sparingly.

``client.get_project_files(project)``
   Returns a list of ``DistributionPackage`` objects representing all of the
   package files available in the repository for the given project.

   When fetching the project's information from the repository, a 404
   response is treated the same as an empty page, resulting in an empty
   list.  All other HTTP errors cause a ``requests.HTTPError`` to be raised.

``client.get_project_url(project)``
   Returns the URL for the given project's page in the repository.


``DistributionPackage``
-----------------------

Information about a versioned archived file from which a Python project release
can be installed.  ``DistributionPackage`` objects have the following
attributes and method:

``filename``
   The basename of the package file

``url``
   The URL from which the package file can be downloaded

``project``
   The name of the project (as extracted from the filename), or `None` if the
   filename cannot be parsed

``version``
   The project version (as extracted from the filename), or `None` if the
   filename cannot be parsed

``package_type``
   The type of the package, or `None` if the filename cannot be parsed.  The
   recognized package types are:

   - ``'dumb'``
   - ``'egg'``
   - ``'msi'``
   - ``'sdist'``
   - ``'wheel'``
   - ``'wininst'``

``requires_python``
   An optional version specifier string declaring the Python version(s) in
   which the package can be installed

``has_sig``
   Whether the package file is accompanied by a PGP signature file

``sig_url``
   If ``has_sig`` is true, this equals the URL of the package file's PGP
   signature file; otherwise, it equals `None`.

``get_digests()``
   Extracts the hash digests from the package file's URL and returns a `dict`
   mapping hash algorithm names to hex-encoded digest strings
