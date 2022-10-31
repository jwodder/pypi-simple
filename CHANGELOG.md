v1.0.0 (2022-10-31)
-------------------
- Removed deprecated functionality:
    - `DistributionPackage.get_digests()`
    - `PyPISimple.get_projects()`
    - `PyPISimple.get_project_files()`
    - `parse_simple_index()`
    - `parse_project_page()`
    - `parse_links()`
- Drop support for Python 3.6
- Support Python 3.11
- `IndexPage`, `ProjectPage`, `DistributionPackage`, and `Link` have been
  changed from NamedTuples to dataclasses
- Replaced `DistributionPackage.yanked` with separate `is_yanked` and
  `yanked_reason` attributes
- `parse_filename()` now raises an `UnparsableFilenameError` on unparsable
  filenames instead of returning a triple of `None`s
- `PyPISimple.get_project_page()` now raises a `NoSuchProjectError` on 404
  responses instead of returning `None`
- The functions for parsing data into `IndexPage` and `ProjectPage` instances
  have been replaced with classmethods:
    - `parse_repo_index_page()` → `IndexPage.from_html()`
    - `parse_repo_index_json()` → `IndexPage.from_json_data()`
    - `parse_repo_index_response()` → `IndexPage.from_response()`
    - `parse_repo_links()` → `RepositoryPage.from_html()`
    - `parse_repo_project_page()` → `ProjectPage.from_html()`
    - `parse_repo_project_json()` → `ProjectPage.from_json_data()`
    - `parse_repo_project_response()` → `ProjectPage.from_response()`
- Add a `RepositoryPage` class for representing the return value of
  `parse_repo_links()` (now called `RepositoryPage.from_html()`)
- Renamed `DistributionPackage.from_pep691_details()` to `from_json_data()`
- `PyPISimple.stream_project_names()` now accepts JSON responses
- Use pydantic internally to parse JSON responses
- Added constants for passing to `PyPISimple` and its methods in order to
  specify the `Accept` header to send

v0.10.0 (2022-06-30)
--------------------
- Support Python 3.10
- Support PEP 691
    - Send "Accept" headers in requests (except for `stream_project_names()`)
      listing both the new JSON format and the old HTML format
    - `parse_repo_project_response()` and `parse_repo_index_response()` now
      support both the JSON and HTML formats
    - Add `parse_repo_index_json()` and `parse_repo_project_json()` functions
    - Gave `DistributionPackage` a `from_pep691_details()` classmethod
    - `DistributionPackage.has_metadata` will now be `None` if not specified by
      a JSON response
    - `DistributionPackage.metadata_url` is now always non-`None`
- Gave `DistributionPackage` a `digests` attribute
    - The `get_digests()` method of `DistributionPackage` is now deprecated;
      use `digests` instead
    - Digest fragments are now removed from `DistributionPackage.url` when
      parsing HTML responses
- Warn on encountering a repository version with a greater minor version than
  expected
- Gave `PyPISimple` a `download_package()` method

v0.9.0 (2021-08-26)
-------------------
- Support PEP 658 by adding `has_metadata`, `metadata_url`, and
  `metadata_digests` attributes to `DistributionPackage`

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
