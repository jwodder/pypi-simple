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
