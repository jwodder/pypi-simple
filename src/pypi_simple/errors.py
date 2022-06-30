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
    Raised by `PyPISimple.download_package()` with ``verify=True`` when the
    given package does not have any digests with known algorithms
    """

    pass


class DigestMismatchError(ValueError):
    """
    Raised by `PyPISimple.download_package()` with ``verify=True`` when the
    digest of the downloaded file does not match the expected value
    """

    def __init__(
        self, algorithm: str, expected_digest: str, actual_digest: str
    ) -> None:
        #: The name of the digest algorithm used
        self.algorithm = algorithm
        #: The expected digest
        self.expected_digest = expected_digest
        #: The digest of the file that was actually received
        self.actual_digest = actual_digest

    def __str__(self) -> str:
        return (
            f"{self.algorithm} digest of downloaded file is"
            f" {self.actual_digest!r} instead of expected {self.expected_digest!r}"
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
