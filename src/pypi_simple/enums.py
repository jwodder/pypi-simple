from enum import Enum


class ProjectStatus(str, Enum):
    """
    .. versionadded:: 1.7.0

    Enum of project status markers as defined by :pep:`792`
    """

    #: The project is active.  This is the default status for a project.
    ACTIVE = "active"

    #: The project does not expect to be updated in the future.
    ARCHIVED = "archived"

    #: The project is considered generally unsafe for use, e.g. due to malware.
    QUARANTINED = "quarantined"

    #: The project is considered obsolete, and may have been superseded by
    #: another project.
    DEPRECATED = "deprecated"

    def __str__(self) -> str:
        return self.value
