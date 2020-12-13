v0.8.0 (2020-12-13)
-------------------
- Support Python 3.9
- `PyPISimple` is now usable as a context manager that will close the session
  on exit

v0.7.0 (2020-10-15)
-------------------
- Drop support for Python 2.7, Python 3.4, and Python 3.5
- `DistributionPackage.has_sig` is now `None` if the package repository does
  not report this information
- Added type annotations
- Moved documentation from README file to a Read the Docs site
- Added new methods to `PyPISimple`:
    - `get_index_page()` — Returns an `IndexPage` instance with a `projects:
      List[str]` attribute plus other attributes for repository metadata
    - `get_project_page()` — Returns a `ProjectPage` instance with a `packages:
      List[DistributionPackage]` attribute plus other attributes for repository
      metadata
    - `stream_project_names()` — Retrieves project names from a repository
      using a streaming request
- New utility functions:
    - `parse_repo_links()` — Parses an HTML page and returns a pair of
      repository metadata and a list of `Link` objects
    - `parse_repo_project_page()` — Parses a project page and returns a
      `ProjectPage` instance
    - `parse_repo_project_response()` — Parses a `requests.Response` object
      containing a project page and returns a `ProjectPage` instance
    - `parse_links_stream()` — Parses an HTML page as stream of `bytes` or
      `str` and returns a generator of `Link` objects
    - `parse_links_stream_response()` — Parses a streaming `requests.Response`
      object containing an HTML page and returns a generator of `Link` objects
    - `parse_repo_index_page()` — Parses a simple repository index/root page
      and returns an `IndexPage` instance
    - `parse_repo_index_response()` — Parses a `requests.Response` object
      containing an index page and returns an `IndexPage` instance
- The following functions & methods are now deprecated and will be removed in a
  future version:
    - `PyPISimple.get_projects()`
    - `PyPISimple.get_project_files()`
    - `parse_simple_index()`
    - `parse_project_page()`
    - `parse_links()`
- Support Warehouse's ``X-PyPI-Last-Serial`` header by attaching the value to
  the objects returned by `get_index_page()` and `get_project_page()`
- Support PEP 629 by attaching the repository version to the objects returned
  by `get_index_page()` and `get_project_page()` and by raising an
  `UnsupportedRepoVersionError` when a repository with an unsupported version
  is encountered

v0.6.0 (2020-03-01)
-------------------
- Support Python 3.8
- `DistributionPackage.sig_url` is now always non-`None`, as Warehouse does not
  report proper values for `has_sig`

v0.5.0 (2019-05-12)
-------------------
- The `PyPISimple` constructor now takes an optional `session` argument which
  can be used to specify a `requests.Session` object with more complicated
  configuration than just authentication
- Support for PEP 592; `DistributionPackage` now has a `yanked` attribute

v0.4.0 (2018-09-06)
-------------------
- Publicly (i.e., in the README) document the utility functions
- Gave `PyPISimple` an `auth` parameter for specifying login/authentication
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
