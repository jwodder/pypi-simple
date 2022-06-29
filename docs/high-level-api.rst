.. currentmodule:: pypi_simple

High-Level API
==============
.. autoclass:: PyPISimple
.. autoclass:: IndexPage()
.. autoclass:: ProjectPage()
.. autoclass:: DistributionPackage()

Constants
---------
.. autodata:: PYPI_SIMPLE_ENDPOINT
.. autodata:: SUPPORTED_REPOSITORY_VERSION

Progress Trackers
-----------------
.. autoclass:: ProgressTracker()
    :special-members: __enter__, __exit__
.. autofunction:: tqdm_progress_factory

Exceptions
----------
.. autoexception:: DigestMismatchError()
    :show-inheritance:
.. autoexception:: NoDigestsError()
    :show-inheritance:
.. autoexception:: UnsupportedContentTypeError()
    :show-inheritance:
.. autoexception:: UnsupportedRepoVersionError()
.. autoexception:: UnexpectedRepoVersionWarning()
    :show-inheritance:
