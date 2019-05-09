.. image:: http://www.repostatus.org/badges/latest/active.svg
    :target: http://www.repostatus.org/#active
    :alt: Project Status: Active — The project has reached a stable, usable
          state and is being actively developed.

.. image:: https://travis-ci.org/jwodder/pypi-simple.svg?branch=master
    :target: https://travis-ci.org/jwodder/pypi-simple

.. image:: https://codecov.io/gh/jwodder/pypi-simple/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/pypi-simple

.. image:: https://img.shields.io/pypi/pyversions/pypi-simple.svg
    :target: https://pypi.org/project/pypi-simple/

.. image:: https://img.shields.io/github/license/jwodder/pypi-simple.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
    :target: https://saythanks.io/to/jwodder

`GitHub <https://github.com/jwodder/pypi-simple>`_
| `PyPI <https://pypi.org/project/pypi-simple/>`_
| `Issues <https://github.com/jwodder/pypi-simple/issues>`_
| `Changelog <https://github.com/jwodder/pypi-simple/blob/master/CHANGELOG.md>`_

``pypi-simple`` is a client library for the Python Simple Repository API as
specified in `PEP 503 <https://www.python.org/dev/peps/pep-0503/>`_ and updated
by `PEP 592 <https://www.python.org/dev/peps/pep-0592/>`_.  With it, you can
query `the Python Package Index (PyPI) <https://pypi.org>`_ and other `pip
<https://pip.pypa.io>`_-compatible repositories for a list of their available
projects and lists of each project's available package files.  The library also
allows you to query package files for their project version, package type, file
digests, ``requires_python`` string, and PGP signature URL.


Installation
============
Just use `pip <https://pip.pypa.io>`_ (You have pip, right?) to install
``pypi-simple`` and its dependencies::

    pip install pypi-simple


Example
=======

::

    >>> from pypi_simple import PyPISimple
    >>> client = PyPISimple()
    >>> packages = client.get_project_files('requests')
    >>> packages[0]
    DistributionPackage(filename='requests-0.2.0.tar.gz', url='https://files.pythonhosted.org/packages/ba/bb/dfa0141a32d773c47e4dede1a617c59a23b74dd302e449cf85413fc96bc4/requests-0.2.0.tar.gz#sha256=813202ace4d9301a3c00740c700e012fb9f3f8c73ddcfe02ab558a8df6f175fd', project='requests', version='0.2.0', package_type='sdist', requires_python=None, has_sig=False, yanked=None)
    >>> packages[0].filename
    'requests-0.2.0.tar.gz'
    >>> packages[0].url
    'https://files.pythonhosted.org/packages/ba/bb/dfa0141a32d773c47e4dede1a617c59a23b74dd302e449cf85413fc96bc4/requests-0.2.0.tar.gz#sha256=813202ace4d9301a3c00740c700e012fb9f3f8c73ddcfe02ab558a8df6f175fd'
    >>> packages[0].project
    'requests'
    >>> packages[0].version
    '0.2.0'
    >>> packages[0].package_type
    'sdist'
    >>> packages[0].get_digests()
    {'sha256': '813202ace4d9301a3c00740c700e012fb9f3f8c73ddcfe02ab558a8df6f175fd'}


API
===

``PyPISimple``
--------------

A client for fetching package information from a Python simple package
repository

``PyPISimple(endpoint=pypi_simple.PYPI_SIMPLE_ENDPOINT, auth=None, session=None)``
   Create a new ``PyPISimple`` object for querying the simple API instance at
   ``endpoint``.  The endpoint defaults to PyPI's simple API at
   <https://pypi.org/simple/>.

   If necessary, login/authentication details for the repository can be
   specified by setting the ``auth`` parameter to either a ``(username,
   password)`` pair or `another authentication object accepted by requests
   <http://docs.python-requests.org/en/master/user/authentication/>`_.

   If more complicated session configuration is desired (e.g., setting up
   caching), the user must create & configure a ``requests.Session`` object
   appropriately and pass it to the constructor as the ``session`` parameter.

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
   - ``'rpm'``
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

``yanked``
   If the package file has been "yanked" from the package repository (meaning
   that it should only be installed when that specific version is requested),
   this attribute will be a string giving the reason why it was yanked;
   otherwise, it is `None`.

``get_digests()``
   Extracts the hash digests from the package file's URL and returns a `dict`
   mapping hash algorithm names to hex-encoded digest strings


Utility Functions
-----------------

``parse_simple_index(html, base_url=None, from_encoding=None)``
   Parse a simple repository's index page and return a generator of ``(project
   name, project URL)`` pairs.  ``html`` is a `str` or `bytes` value to parse.
   ``base_url`` is an optional URL (usually the URL of the page being parsed)
   to join to the front of the URLs returned.  ``from_encoding`` is an optional
   hint to Beautiful Soup as to the encoding of ``html``.

``parse_project_page(html, base_url=None, from_encoding=None, project_hint=None)``
   Parse a project page from a simple repository and return a list of
   ``DistributionPackage`` objects.  ``html`` is a `str` or `bytes` value to
   parse.  ``base_url`` is an optional URL (usually the URL of the page being
   parsed) to join to the front of the URLs returned.  ``from_encoding`` is an
   optional hint to Beautiful Soup as to the encoding of ``html``.
   ``project_hint`` is the name of the project whose page is being parsed; it
   is used to disambiguate the parsing of certain filenames.

``parse_links(html, base_url=None, from_encoding=None)``
   Parse an HTML page and return a generator of links, where each link is
   represented as a triple of link text, link URL, and a `dict` of link tag
   attributes (including the unmodified ``href`` attribute).  Link text has all
   leading & trailing whitespace removed.  Keys in the attributes `dict` are
   converted to lowercase.

   ``html`` is a `str` or `bytes` value to parse.  ``base_url`` is an optional
   URL (usually the URL of the page being parsed) to join to the front of the
   URLs returned.  ``from_encoding`` is an optional hint to Beautiful Soup as
   to the encoding of ``html``.

``parse_filename(filename, project_hint=None)``
   Given the filename of a distribution package, returns a triple of the
   project name, project version, and package type.  The name and version are
   spelled the same as they appear in the filename; no normalization is
   performed.

   The package type may be any of the following strings:

   - ``'dumb'``
   - ``'egg'``
   - ``'msi'``
   - ``'rpm'``
   - ``'sdist'``
   - ``'wheel'``
   - ``'wininst'``

   If the filename cannot be parsed, ``(None, None, None)`` is returned.

   Note that some filenames (e.g., ``1-2-3.tar.gz``) may be ambiguous as
   to which part is the project name and which is the version.  In order to
   resolve the ambiguity, the expected value for the project name (*modulo*
   normalization) can be supplied as the ``project_name`` argument to the
   function.  If the filename can be parsed with the given string in the role
   of the project name, the results of that parse will be returned; otherwise,
   the function will fall back to breaking the project & version apart at an
   unspecified point.
