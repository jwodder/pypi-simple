from packaging.version import Version
from .                 import SUPPORTED_REPOSITORY_VERSION

def check_repo_version(
    declared_version: str,
    supported_version: str = SUPPORTED_REPOSITORY_VERSION,
) -> None:
    """
    Raise an `UnsupportedRepoVersionError` if ``declared_version`` has a
    greater major version component than ``supported_version``
    """
    declared = Version(declared_version)
    supported = Version(supported_version)
    if (declared.epoch, declared.major) > (supported.epoch, supported.major):
        raise UnsupportedRepoVersionError(declared_version, supported_version)


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
