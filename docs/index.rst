.. module:: pypi_simple

=======================================================
pypi-simple — PyPI Simple Repository API client library
=======================================================

`GitHub <https://github.com/jwodder/pypi-simple>`_
| `PyPI <https://pypi.org/project/pypi-simple/>`_
| `Documentation <https://pypi-simple.readthedocs.io>`_
| `Issues <https://github.com/jwodder/pypi-simple/issues>`_
| :doc:`Changelog <changelog>`

.. toctree::
    :hidden:

    api
    changelog

``pypi-simple`` is a client library for the Python Simple Repository API as
specified in :pep:`503` and updated by :pep:`592`, :pep:`629`, :pep:`658`, and
:pep:`691`.  With it, you can query `the Python Package Index (PyPI)
<https://pypi.org>`_ and other `pip <https://pip.pypa.io>`_-compatible
repositories for a list of their available projects and lists of each project's
available package files.  The library also allows you to download package files
and query them for their project version, package type, file digests,
``requires_python`` string, PGP signature URL, and metadata URL.

Installation
============
``pypi-simple`` requires Python 3.7 or higher.  Just use `pip
<https://pip.pypa.io>`_ for Python 3 (You have pip, right?) to install
``pypi-simple`` and its dependencies::

    python3 -m pip install pypi-simple

``pypi-simple`` can optionally make use of tqdm_.  To install it alongside
``pypi-simple``, specify the ``tqdm`` extra::

    python3 -m pip install "pypi-simple[tqdm]"

.. _tqdm: https://tqdm.github.io


Example
=======

Get information about a package:

>>> from pypi_simple import PyPISimple
>>> with PyPISimple() as client:
...     requests_page = client.get_project_page('requests')
>>> pkg = requests_page.packages[0]
>>> pkg.filename
'requests-0.2.0.tar.gz'
>>> pkg.url
'https://files.pythonhosted.org/packages/ba/bb/dfa0141a32d773c47e4dede1a617c59a23b74dd302e449cf85413fc96bc4/requests-0.2.0.tar.gz'
>>> pkg.project
'requests'
>>> pkg.version
'0.2.0'
>>> pkg.package_type
'sdist'
>>> pkg.digests
{'sha256': '813202ace4d9301a3c00740c700e012fb9f3f8c73ddcfe02ab558a8df6f175fd'}

Download a package with a tqdm progress bar:

.. code:: python

    from pypi_simple import PyPISimple, tqdm_progress_factory

    with PyPISimple() as client:
        page = client.get_project_page("pypi-simple")
        pkg = page.packages[-1]
        client.download_package(
            pkg, path=pkg.filename, progress=tqdm_progress_factory(),
        )


Indices and tables
==================
* :ref:`genindex`
* :ref:`search`
