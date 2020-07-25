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

    classes
    functions
    changelog

``pypi-simple`` is a client library for the Python Simple Repository API as
specified in :pep:`503` and updated by :pep:`592`.  With it, you can query `the
Python Package Index (PyPI) <https://pypi.org>`_ and other `pip
<https://pip.pypa.io>`_-compatible repositories for a list of their available
projects and lists of each project's available package files.  The library also
allows you to query package files for their project version, package type, file
digests, ``requires_python`` string, and PGP signature URL.


Installation
============
``pypi-simple`` requires Python 3.6 or higher.  Just use `pip
<https://pip.pypa.io>`_ for Python 3 (You have pip, right?) to install
``pypi-simple`` and its dependencies::

    python3 -m pip install pypi-simple


Example
========

::

    >>> from pypi_simple import PyPISimple
    >>> client = PyPISimple()
    >>> packages = client.get_project_files('requests')
    >>> packages[0]
    DistributionPackage(filename='requests-0.2.0.tar.gz', url='https://files.pythonhosted.org/packages/ba/bb/dfa0141a32d773c47e4dede1a617c59a23b74dd302e449cf85413fc96bc4/requests-0.2.0.tar.gz#sha256=813202ace4d9301a3c00740c700e012fb9f3f8c73ddcfe02ab558a8df6f175fd', project='requests', version='0.2.0', package_type='sdist', requires_python=None, has_sig=None, yanked=None)
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


Indices and tables
==================
* :ref:`genindex`
* :ref:`search`
