class UnsupportedRepoVersionError(Exception):
    """
    Raised upon encountering a simple repository whose repository version
    (:pep:`629`) has a greater major component than the maximum supported
    repository version (`SUPPORTED_REPOSITORY_VERSION`)
    """

    def __init__(self, declared_version: str, supported_version: str) -> None:
        #: The version of the simple repository
        self.declared_version: str = declared_version
        #: The maximum repository version that we support
        self.supported_version: str = supported_version

    def __str__(self) -> str:
        return (
            f"Repository's version ({self.declared_version}) has greater major"
            f" component than supported version ({self.supported_version})"
        )


class UnexpectedRepoVersionWarning(UserWarning):
    """
    Emitted upon encountering a simple repository whose repository version
    (:pep:`629`) has a greater minor version components than the maximum
    supported repository version (`SUPPORTED_REPOSITORY_VERSION`).

    This warning can be emitted by anything that can raise
    `UnsupportedRepoVersionError`.
    """

    pass


class UnsupportedContentTypeError(ValueError):
    """
    Raised when a response from a simple repository has an unsupported
    :mailheader:`Content-Type`
    """

    def __init__(self, url: str, content_type: str) -> None:
        #: The URL that returned the response
        self.url = url
        #: The unsupported :mailheader:`Content-Type`
        self.content_type = content_type

    def __str__(self) -> str:
        return (
            f"Response from {self.url} has unsupported Content-Type"
            f" {self.content_type!r}"
        )


class NoDigestsError(ValueError):
    """
    Raised by `PyPISimple`'s download methods when passed ``verify=True`` and
    the resource being downloaded does not have any digests with known
    algorithms
    """

    def __init__(self, url: str) -> None:
        #: The URL of the resource being downloaded
        #:
        #: .. versionadded:: 1.6.0
        self.url = url

    def __str__(self) -> str:
        return f"No digests with known algorithms available for resource at {self.url}"


class DigestMismatchError(ValueError):
    """
    Raised by `PyPISimple`'s download methods when passed ``verify=True`` and
    the digest of the downloaded data does not match the expected value
    """

    def __init__(
        self, *, algorithm: str, expected_digest: str, actual_digest: str, url: str
    ) -> None:
        #: The name of the digest algorithm used
        self.algorithm = algorithm
        #: The expected digest
        self.expected_digest = expected_digest
        #: The digest of the data that was actually received
        self.actual_digest = actual_digest
        #: The URL of the resource being downloaded
        #:
        #: .. versionadded:: 1.6.0
        self.url = url

    def __str__(self) -> str:
        return (
            f"{self.algorithm} digest of {self.url} is {self.actual_digest!r}"
            f" instead of expected {self.expected_digest!r}"
        )


class UnparsableFilenameError(ValueError):
    """
    .. versionadded:: 1.0.0

    Raised when `parse_filename()` is passed an unparsable filename
    """

    def __init__(self, filename: str) -> None:
        #: The unparsable filename
        self.filename = filename

    def __str__(self) -> str:
        return f"Cannot parse package filename: {self.filename!r}"


class NoSuchProjectError(Exception):
    """
    Raised by `PyPISimple.get_project_page()` when a request for a project
    fails with a 404 error code
    """

    def __init__(self, project: str, url: str) -> None:
        #: The name of the project requested
        self.project = project
        #: The URL to which the failed request was made
        self.url = url

    def __str__(self) -> str:
        return f"No details about project {self.project!r} available at {self.url}"


class NoMetadataError(Exception):
    """
    .. versionadded:: 1.3.0

    Raised by `PyPISimple.get_package_metadata()` when a request for
    distribution metadata fails with a 404 error code
    """

    def __init__(self, filename: str, url: str) -> None:
        #: The filename of the package whose metadata was requested
        self.filename = filename
        #: The URL to which the failed request was made
        #:
        #: .. versionadded:: 1.6.0
        self.url = url

    def __str__(self) -> str:
        return f"No distribution metadata found for {self.filename} at {self.url}"


class NoProvenanceError(Exception):
    """
    .. versionadded:: 1.6.0

    Raised by `PyPISimple.get_provenance()` when a request for a
    ``.provenance`` file fails with a 404 error code
    """

    def __init__(self, filename: str, url: str) -> None:
        #: The filename of the package whose provenance was requested
        self.filename = filename
        #: The URL to which the failed request was made
        self.url = url

    def __str__(self) -> str:
        return f"No .provenance file found for {self.filename} at {self.url}"
