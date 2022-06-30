.. currentmodule:: pypi_simple

API
===

Client
------
.. autoclass:: PyPISimple

Core Classes
------------
.. autoclass:: IndexPage()
.. autoclass:: ProjectPage()
.. autoclass:: DistributionPackage()

Progress Trackers
-----------------
.. autoclass:: ProgressTracker()
    :special-members: __enter__, __exit__
.. autofunction:: tqdm_progress_factory

Parsing Filenames
-----------------
.. autofunction:: parse_filename

Parsing Simple Repository HTML Pages
------------------------------------
.. autoclass:: RepositoryPage()
.. autoclass:: Link()

Streaming Parsers
^^^^^^^^^^^^^^^^^
.. autofunction:: parse_links_stream
.. autofunction:: parse_links_stream_response

Constants
---------
.. autodata:: PYPI_SIMPLE_ENDPOINT
.. autodata:: SUPPORTED_REPOSITORY_VERSION

Exceptions
----------
.. autoexception:: DigestMismatchError()
    :show-inheritance:
.. autoexception:: NoDigestsError()
    :show-inheritance:
.. autoexception:: NoSuchProjectError()
.. autoexception:: UnsupportedContentTypeError()
    :show-inheritance:
.. autoexception:: UnsupportedRepoVersionError()
.. autoexception:: UnexpectedRepoVersionWarning()
    :show-inheritance:
.. autoexception:: UnparsableFilenameError()
    :show-inheritance:
