from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, StrictBool, field_validator


def shishkebab(s: str) -> str:
    return s.replace("_", "-")


class Meta(BaseModel, alias_generator=shishkebab, populate_by_name=True):
    api_version: str
    last_serial: Optional[str] = Field(None, alias="_last-serial")

    @field_validator("last_serial", mode="before")
    @classmethod
    def _strify_serial_int(cls, value: Any) -> Any:
        if isinstance(value, int):
            return str(value)
        else:
            return value


class ProjectMeta(Meta):
    tracks: List[str] = Field(default_factory=list)
    alternate_locations: List[str] = Field(default_factory=list)


class File(BaseModel, alias_generator=shishkebab, populate_by_name=True):
    filename: str
    url: str
    hashes: Dict[str, str]
    requires_python: Optional[str] = None
    core_metadata: Union[StrictBool, Dict[str, str], None] = None
    gpg_sig: Optional[StrictBool] = None
    yanked: Union[StrictBool, str] = False
    size: Optional[int] = None
    upload_time: Optional[datetime] = None
    provenance: Optional[str] = None

    @property
    def is_yanked(self) -> bool:
        if isinstance(self.yanked, str):
            return True
        else:
            return self.yanked

    @property
    def yanked_reason(self) -> Optional[str]:
        if isinstance(self.yanked, str):
            return self.yanked
        else:
            return None

    @property
    def has_metadata(self) -> Optional[bool]:
        if isinstance(self.core_metadata, dict):
            return True
        else:
            return self.core_metadata

    @property
    def metadata_digests(self) -> Optional[dict[str, str]]:
        if isinstance(self.core_metadata, dict):
            return self.core_metadata
        elif self.core_metadata is True:
            return {}
        else:
            return None


class Project(BaseModel):
    name: str
    files: List[File]
    meta: ProjectMeta
    versions: Optional[List[str]] = None


class ProjectItem(BaseModel):
    name: str


class ProjectList(BaseModel):
    projects: List[ProjectItem]
    meta: Meta
