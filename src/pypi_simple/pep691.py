from __future__ import annotations
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field, HttpUrl, StrictBool, field_validator
from .enums import ProjectStatus


def shishkebab(s: str) -> str:
    return s.replace("_", "-")


class Meta(BaseModel, alias_generator=shishkebab, populate_by_name=True):
    api_version: str
    last_serial: str | None = Field(None, alias="_last-serial")

    @field_validator("last_serial", mode="before")
    @classmethod
    def _strify_serial_int(cls, value: Any) -> Any:
        if isinstance(value, int):
            return str(value)
        else:
            return value


class ProjectMeta(Meta):
    tracks: list[str] = Field(default_factory=list)


class StatusData(BaseModel):
    status: ProjectStatus | None = None
    reason: str | None = None


class File(BaseModel, alias_generator=shishkebab, populate_by_name=True):
    filename: str
    url: str
    hashes: dict[str, str]
    requires_python: str | None = None
    core_metadata: StrictBool | dict[str, str] | None = None
    gpg_sig: StrictBool | None = None
    yanked: StrictBool | str = False
    size: int | None = None
    upload_time: datetime | None = None
    provenance: HttpUrl | None = None

    @property
    def is_yanked(self) -> bool:
        if isinstance(self.yanked, str):
            return True
        else:
            return self.yanked

    @property
    def yanked_reason(self) -> str | None:
        if isinstance(self.yanked, str):
            return self.yanked
        else:
            return None

    @property
    def has_metadata(self) -> bool | None:
        if isinstance(self.core_metadata, dict):
            return True
        else:
            return self.core_metadata

    @property
    def metadata_digests(self) -> dict[str, str] | None:
        if isinstance(self.core_metadata, dict):
            return self.core_metadata
        elif self.core_metadata is True:
            return {}
        else:
            return None


class Project(BaseModel, alias_generator=shishkebab, populate_by_name=True):
    name: str
    files: list[File]
    meta: ProjectMeta
    alternate_locations: list[str] = Field(default_factory=list)
    project_status: StatusData = Field(default_factory=StatusData)
    versions: list[str] | None = None


class ProjectItem(BaseModel):
    name: str


class ProjectList(BaseModel):
    projects: list[ProjectItem]
    meta: Meta
