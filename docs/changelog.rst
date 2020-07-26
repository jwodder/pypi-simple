.. currentmodule:: pypi_simple

Changelog
=========

v0.7.0 (in development)
-----------------------
- Drop support for Python 2.7, Python 3.4, and Python 3.5
- `DistributionPackage.has_sig` is now `None` if the package repository does
  not report this information
- Added type annotations
- Moved documentation from README file to a Read the Docs site
- Gave `PyPISimple` a `~PyPISimple.get_project_page()` method that returns a
  `ProjectPage` instance with a ``packages: List[DistributionPackage]``
  attribute plus other attributes for repository metadata
- Gave `PyPISimple` a `~PyPISimple.stream_project_names()` method for
  retrieving project names from a repository using a streaming request
- New utility functions:

  - `parse_repo_links()` — Parses an HTML page, returns a pair of repository
    metadata and a list of `Link` objects
  - `parse_repo_project_page()` — Parses a project page, returns a
    `ProjectPage` instance
  - `parse_repo_project_reponse()` — Parses a `requests.Response` object
    containing a project page, returns a `ProjectPage` instance
  - `parse_links_stream()` — Parses an HTML page as stream of `bytes` or `str`
    and returns a generator of `Link` objects
  - `parse_links_stream_response()` — Parses a streaming `requests.Response`
    object containing an HTML page and returns a generator of `Link` objects


v0.6.0 (2020-03-01)
-------------------
- Support Python 3.8
- `DistributionPackage.sig_url` is now always non-`None`, as Warehouse does not
  report proper values for `~DistributionPackage.has_sig`

v0.5.0 (2019-05-12)
-------------------
- The `PyPISimple` constructor now takes an optional ``session`` argument which
  can be used to specify a `requests.Session` object with more complicated
  configuration than just authentication
- Support for PEP 592; `DistributionPackage` now has a
  `~DistributionPackage.yanked` attribute

v0.4.0 (2018-09-06)
-------------------
- Publicly (i.e., in the README) document the utility functions
- Gave `PyPISimple` an ``auth`` parameter for specifying login/authentication
  details

v0.3.0 (2018-09-03)
-------------------
- When fetching the list of files for a project, the project name is now used
  to resolve ambiguous filenames.
- The filename parser now requires all filenames to be all-ASCII (except for
  wheels).

v0.2.0 (2018-09-01)
-------------------
- The filename parser now rejects invalid project names, blatantly invalid
  versions, and non-ASCII digits.
- RPM packages are now recognized.

v0.1.0 (2018-08-31)
-------------------
Initial release