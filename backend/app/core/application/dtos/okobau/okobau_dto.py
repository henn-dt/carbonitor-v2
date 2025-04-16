from typing import List, Optional

from pydantic import BaseModel, Field


class ComplianceResponse(BaseModel):
    name: Optional[str] = None
    uri: Optional[str] = None
    uuid: Optional[str] = None

class DataSourceResponse(BaseModel):
    uuid: Optional[str] = None
    name: Optional[str] = None

class RegAuthorityResponse(BaseModel):
    uuid: Optional[str] = None
    name: Optional[str] = None

class EPDResponse(BaseModel):
    # Mandatory fields
    uuid: str
    name: str
    classific: Optional[str] = None
    languages: Optional[List[str]] = None
    version: Optional[str] = None
    geo: Optional[str] = None
    classificId: Optional[str] = None
    classificSystem: Optional[str] = None
    type: Optional[str] = None
    refYear: Optional[int] = None
    validUntil: Optional[int] = None
    compliance: Optional[List[ComplianceResponse]] = Field(default_factory=list)
    owner: Optional[str] = None
    subType: Optional[str] = None
    dataSources: Optional[List[DataSourceResponse]] = Field(default_factory=list)
    regNo: Optional[str] = None
    regAuthority: Optional[RegAuthorityResponse] = None
    nodeid: Optional[str] = None
    dsType: Optional[str] = None

    class Config:
        from_attributes = True