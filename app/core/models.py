from typing import Any, Literal, Optional

from pydantic import BaseModel, Field

Sha256Pattern = r"^sha256:[0-9a-f]{64}$"
CatLevel = Literal['CAT1','CAT2','CAT3','CAT4','CAT5']

class ToolEnvelope(BaseModel):
    tool_name: str
    run_id: str | None = None
    actor: str | None = None
    arguments: dict[str, Any]

class ArtifactRef(BaseModel):
    uri: str
    sha256: str = Field(pattern=Sha256Pattern)

class ReleaseInfo(BaseModel):
    project: str
    platform: str
    system: str
    delivery: str
    cat_level: CatLevel
    status: str
    revision: str
    date: str

class IdentificationInfo(BaseModel):
    cplace_id: str
    zf_part_number_summary: str
    oem_part_number_summary: str
    system_ptc_project_id: str
    system_ptc_alm_delivery_id: str

class SoftwarePart(BaseModel):
    name: str
    ptc_integrity_id: str
    software_version_zf: str
    software_version_customer: Optional[str] = None
    configuration_path: Optional[str] = None
    to_whom: Optional[str] = None

class ReasonForRelease(BaseModel):
    clarity_project_id: Optional[str] = None
    reason_description: str
    former_delivery_id: Optional[str] = None
    replacement_delivery_id: Optional[str] = None
    system_changes: str

class ReleaseDocument(BaseModel):
    title: str
    revision: Optional[str] = None
    status: Optional[str] = None
    archive: Optional[str] = None

class TestSummaryReport(ReleaseDocument):
    aggregated_test_result: Literal['Passed','Failed']

class SafetyCase(ReleaseDocument):
    required_for_cat5: bool = False

class ReleaseDocumentation(BaseModel):
    software_release_document: Optional[ReleaseDocument] = None
    test_summary_report: Optional[TestSummaryReport] = None
    impact_analysis: Optional[ReleaseDocument] = None
    safety_case: Optional[SafetyCase] = None

class KnownIssues(BaseModel):
    issues_found: bool
    driver_information: Optional[str] = None

class GenerationOptions(BaseModel):
    validate_after_render: bool = True
    emit_receipt: bool = True
    allow_warnings: bool = True

class CreateReleaseSheetRequest(BaseModel):
    actor: str
    template_ref: ArtifactRef
    release: ReleaseInfo
    identification: IdentificationInfo
    software: list[SoftwarePart]
    reason_for_release: ReasonForRelease
    release_documentation: ReleaseDocumentation
    known_issues: KnownIssues
    generation_options: GenerationOptions = GenerationOptions()

class GenerateReleaseSheetToolRequest(BaseModel):
    document_id: str
    system: str
    cat_level: CatLevel
    fields: dict[str, Any]

class ValidateReleaseSheetToolRequest(BaseModel):
    artifact_id: str
    validation_profile: Literal['system_release_sheet','system_release_sheet_cat5']

class WriteReceiptToolRequest(BaseModel):
    event_type: str
    actor: str
    artifact_id: str
    sha256: str = Field(pattern=Sha256Pattern)
    metadata: dict[str, Any] = {}

class FetchArtifactToolRequest(BaseModel):
    artifact_id: str

class ResolveReplayToolRequest(BaseModel):
    run_id: str
    adapter_version: str
