"""
Architecture-as-Code Data Models

This module defines the core data structures for representing enterprise architecture
decisions, patterns, policies, and designs in a machine-readable format.

Models follow the AaC Maturity Model from Level 3 (STRUCTURED) onwards.
"""

from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator


# ============================================================================
# ENUMERATIONS
# ============================================================================

class ComplianceFramework(str, Enum):
    """Supported regulatory compliance frameworks."""
    MIFID_II = "MiFID II"
    DORA = "DORA"
    GDPR = "GDPR"
    SOX = "SOX"
    PCI_DSS = "PCI DSS"
    HIPAA = "HIPAA"
    CUSTOM = "Custom"


class DecisionStatus(str, Enum):
    """Architecture decision lifecycle status."""
    DRAFT = "Draft"
    PROPOSED = "Proposed"
    APPROVED = "Approved"
    ACTIVE = "Active"
    SUPERSEDED = "Superseded"
    DEPRECATED = "Deprecated"


class PolicySeverity(str, Enum):
    """Policy violation severity levels."""
    CRITICAL = "Critical"      # Must fix immediately
    HIGH = "High"              # Should fix soon
    MEDIUM = "Medium"          # Address in next cycle
    LOW = "Low"                # Nice to have
    INFO = "Info"              # For awareness


class ValidationStatus(str, Enum):
    """Validation check outcomes."""
    PASS = "Pass"
    FAIL = "Fail"
    WARN = "Warn"
    SKIPPED = "Skipped"


# ============================================================================
# BUSINESS & CAPABILITY MODELS
# ============================================================================

class BusinessCapability(BaseModel):
    """
    Represents a business capability - a functional unit of the business.
    
    Example:
        - Loan Origination
        - Risk Management
        - Customer Onboarding
    """
    id: str = Field(..., description="Unique identifier (e.g., BC-LOAN-001)")
    name: str = Field(..., description="Business capability name")
    description: str = Field(..., description="Detailed description of the capability")
    owner: str = Field(..., description="Owner/Business stakeholder")
    applications: List[str] = Field(default_factory=list, description="Associated applications")
    criticality: Literal["Critical", "High", "Medium", "Low"] = Field(
        default="Medium", description="Business criticality level"
    )
    sla_availability: float = Field(default=99.5, description="SLA availability percentage")
    sla_rpo_minutes: int = Field(default=60, description="Recovery Point Objective in minutes")
    sla_rto_minutes: int = Field(default=15, description="Recovery Time Objective in minutes")


class ApplicationNode(BaseModel):
    """
    Represents an application in the application landscape.
    
    Example:
        - Core Banking System
        - Risk Analytics Platform
        - Customer Portal
    """
    id: str = Field(..., description="Unique application ID")
    name: str = Field(..., description="Application name")
    description: str = Field(..., description="Application purpose and scope")
    owner: str = Field(..., description="Application owner/team")
    technology_stack: List[str] = Field(default_factory=list, description="Tech stack components")
    deployment_topology: str = Field(
        default="monolith", 
        description="Monolith, microservices, serverless, etc."
    )
    data_classification: str = Field(
        default="confidential",
        description="Data sensitivity: public, internal, confidential, restricted"
    )
    criticality: Literal["Critical", "High", "Medium", "Low"] = "Medium"
    cloud_provider: Optional[str] = Field(default=None, description="AWS, Azure, GCP, OnPrem")
    containers: bool = Field(default=False, description="Uses containerization")
    managed_by: Optional[str] = Field(default=None, description="Team/Platform managing it")


# ============================================================================
# ARCHITECTURE DECISION RECORD (ADR)
# ============================================================================

class ArchitectureDecision(BaseModel):
    """
    Architecture Decision Record (ADR) - captures architectural decisions
    following Michael Nygard's ADR format enhanced with governance.
    
    Reference: https://adr.github.io/
    """
    id: str = Field(..., description="ADR ID (e.g., ADR-001)")
    title: str = Field(..., description="Decision title")
    status: DecisionStatus = Field(default=DecisionStatus.DRAFT)
    date: datetime = Field(default_factory=datetime.now, description="Decision date")
    context: str = Field(..., description="The issue/context requiring the decision")
    decision: str = Field(..., description="What decision was made and why")
    consequences: str = Field(..., description="Positive and negative consequences")
    alternatives: List[str] = Field(default_factory=list, description="Alternative options considered")
    compliance_implications: Optional[str] = Field(
        default=None, description="Regulatory/compliance impact"
    )
    cost_impact: Optional[str] = Field(default=None, description="Financial impact estimation")
    decision_maker: str = Field(..., description="Who made this decision")
    stakeholders: List[str] = Field(default_factory=list, description="Affected stakeholders")
    related_decisions: List[str] = Field(default_factory=list, description="References to related ADRs")
    supersedes: Optional[str] = Field(default=None, description="Which ADR this supersedes (if any)")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")


# ============================================================================
# TECHNOLOGY & STANDARDS
# ============================================================================

class TechnologyStandard(BaseModel):
    """
    Represents an approved technology standard for enterprise architecture.
    
    Example:
        - Java 11+ for microservices
        - PostgreSQL 13+ for relational data
        - Kubernetes 1.26+ for orchestration
    """
    id: str = Field(..., description="Standard ID")
    category: str = Field(..., description="Category (Database, Language, Framework, etc.)")
    technology_name: str = Field(..., description="Official technology name")
    versions: List[str] = Field(..., description="Approved versions")
    use_case: str = Field(..., description="When to use this technology")
    restrictions: Optional[str] = Field(default=None, description="Restrictions or limitations")
    compliance_implications: List[ComplianceFramework] = Field(
        default_factory=list, description="Relevant compliance frameworks"
    )
    adoption_status: Literal["Approved", "Trial", "Deprecated", "Prohibited"] = "Approved"
    owner: str = Field(..., description="Technology owner/steward")


class CloudPattern(BaseModel):
    """
    Represents an approved cloud architecture pattern.
    
    Examples:
        - Strangler Fig Pattern for migration
        - Event Sourcing for audit
        - CQRS for complex domains
        - Multi-region deployment
    """
    id: str = Field(..., description="Pattern ID")
    name: str = Field(..., description="Pattern name")
    description: str = Field(..., description="Pattern description and use cases")
    when_to_use: str = Field(..., description="Situations where this pattern applies")
    benefits: List[str] = Field(default_factory=list, description="Pattern benefits")
    tradeoffs: List[str] = Field(default_factory=list, description="Tradeoffs and considerations")
    technology_stack: List[str] = Field(default_factory=list, description="Recommended technologies")
    cloud_providers: List[str] = Field(default_factory=list, description="Applicable providers")
    estimated_cost_multiplier: float = Field(default=1.0, description="Cost relative to basic deployment")
    complexity_level: Literal["Low", "Medium", "High", "Expert"] = "Medium"


# ============================================================================
# POLICY & GOVERNANCE
# ============================================================================

class PolicyRule(BaseModel):
    """
    A single policy rule that can be validated against architecture decisions.
    
    Example:
        - "All databases must be encrypted at rest"
        - "Public APIs require API Gateway"
        - "Production workloads require multi-region deployment"
    """
    id: str = Field(..., description="Policy rule ID")
    name: str = Field(..., description="Policy name")
    description: str = Field(..., description="What this policy enforces")
    frameworks: List[ComplianceFramework] = Field(
        default_factory=list, description="Compliance frameworks this addresses"
    )
    severity: PolicySeverity = Field(default=PolicySeverity.MEDIUM)
    condition: str = Field(..., description="Rule condition (in pseudo-code or logic)")
    remediation: str = Field(..., description="How to fix violations of this rule")
    enabled: bool = Field(default=True)
    owner: str = Field(..., description="Policy owner")
    created_date: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)


class PolicyValidation(BaseModel):
    """
    Result of validating an architecture against a specific policy.
    """
    policy_id: str = Field(..., description="ID of the validated policy")
    policy_name: str = Field(..., description="Name of the validated policy")
    status: ValidationStatus = Field(..., description="Validation result")
    severity: PolicySeverity = Field(..., description="Policy severity level")
    message: str = Field(..., description="Validation message")
    remediation_steps: Optional[List[str]] = Field(default=None)
    affected_components: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)


# ============================================================================
# ARCHITECTURE DESIGN
# ============================================================================

class ArchitectureDesign(BaseModel):
    """
    Complete architecture design capturing all aspects of a solution architecture.
    This is the primary artifact produced by the AaC generator.
    """
    # Metadata
    id: str = Field(..., description="Unique architecture ID")
    name: str = Field(..., description="Architecture name/title")
    version: str = Field(default="1.0.0", description="Semantic version")
    created_date: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    status: DecisionStatus = Field(default=DecisionStatus.DRAFT)
    
    # Ownership
    architect: str = Field(..., description="Lead architect")
    stakeholders: List[str] = Field(default_factory=list, description="Interested parties")
    reviewers: List[str] = Field(default_factory=list, description="Architecture reviewers")
    approvers: List[str] = Field(default_factory=list, description="Decision approvers")
    
    # Business Context
    business_driver: str = Field(..., description="Why this architecture is needed")
    target_capabilities: List[str] = Field(default_factory=list, description="Business capabilities enabled")
    success_metrics: List[str] = Field(default_factory=list, description="How success is measured")
    estimated_budget: Optional[float] = Field(default=None, description="Budget estimate in USD")
    target_go_live: Optional[datetime] = Field(default=None, description="Target launch date")
    
    # Architecture Components
    business_capabilities: List[BusinessCapability] = Field(
        default_factory=list, description="Business capabilities"
    )
    applications: List[ApplicationNode] = Field(default_factory=list, description="Applications")
    technologies: List[TechnologyStandard] = Field(default_factory=list, description="Technology standards used")
    patterns: List[CloudPattern] = Field(default_factory=list, description="Design patterns applied")
    decisions: List[ArchitectureDecision] = Field(default_factory=list, description="Key decisions")
    
    # Non-Functional Requirements
    availability_target: float = Field(default=99.9, description="Target availability %")
    rto_minutes: int = Field(default=15, description="Recovery Time Objective")
    rpo_minutes: int = Field(default=60, description="Recovery Point Objective")
    max_latency_ms: int = Field(default=200, description="Maximum acceptable latency")
    estimated_users: int = Field(default=1000, description="Expected concurrent users")
    
    # Compliance & Security
    compliance_frameworks: List[ComplianceFramework] = Field(
        default_factory=list, description="Applicable frameworks"
    )
    data_residency: Optional[str] = Field(default=None, description="Data residency requirements")
    encryption_required: bool = Field(default=True, description="Encryption at rest required")
    encryption_in_transit: bool = Field(default=True, description="Encryption in transit required")
    multi_region_required: bool = Field(default=False, description="Multi-region deployment required")
    
    # Validation & Governance
    policy_validations: List[PolicyValidation] = Field(
        default_factory=list, description="Policy validation results"
    )
    compliance_score: float = Field(default=0.0, description="Compliance percentage (0-100)")
    
    # Artifacts
    diagram_url: Optional[str] = Field(default=None, description="Architecture diagram URL")
    iac_repository: Optional[str] = Field(default=None, description="Git repository for IaC")
    documentation_url: Optional[str] = Field(default=None, description="Full documentation link")


class ArchitectureDrift(BaseModel):
    """
    Represents deviation between approved architecture and runtime state.
    """
    id: str = Field(..., description="Drift detection ID")
    design_id: str = Field(..., description="Reference architecture ID")
    component: str = Field(..., description="Component with drift")
    expected: str = Field(..., description="Expected state per architecture")
    actual: str = Field(..., description="Actual runtime state")
    severity: PolicySeverity = Field(default=PolicySeverity.MEDIUM)
    detected_at: datetime = Field(default_factory=datetime.now)
    remediation_plan: Optional[str] = Field(default=None, description="How to fix the drift")


# ============================================================================
# MATURITY MODEL
# ============================================================================

class MaturityAssessment(BaseModel):
    """
    Assessment of architecture-as-code maturity across the organization.
    """
    assessment_date: datetime = Field(default_factory=datetime.now)
    current_level: int = Field(..., ge=1, le=7, description="Current maturity level (1-7)")
    target_level: int = Field(..., ge=1, le=7, description="Target maturity level")
    
    # Level details
    level_1_documented: bool = Field(default=False, description="PowerPoint/Visio docs")
    level_2_versioned: bool = Field(default=False, description="Git + ADR repo")
    level_3_structured: bool = Field(default=False, description="Machine-readable models")
    level_4_policy_driven: bool = Field(default=False, description="Policy-as-Code validation")
    level_5_automated: bool = Field(default=False, description="Architecture CI/CD")
    level_6_agentic: bool = Field(default=False, description="AI-driven review")
    level_7_autonomous: bool = Field(default=False, description="Continuous reconciliation")
    
    # Assessment details
    strengths: List[str] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)
    improvement_roadmap: List[str] = Field(default_factory=list)
    estimated_effort_months: int = Field(default=6)


# ============================================================================
# GENERATION OUTPUT
# ============================================================================

class GeneratedArtifact(BaseModel):
    """
    Output artifact generated from architecture design.
    """
    type: Literal["ADR", "Terraform", "Helm", "OpenAPI", "Diagram", "Document"] = "ADR"
    name: str = Field(..., description="Artifact name/filename")
    content: str = Field(..., description="Generated content")
    language: str = Field(default="markdown", description="Content language/format")
    generated_at: datetime = Field(default_factory=datetime.now)
    source_design: str = Field(..., description="Source architecture design ID")
    validated: bool = Field(default=False, description="Has this been validated")


if __name__ == "__main__":
    # Example usage
    capability = BusinessCapability(
        id="BC-LOAN-001",
        name="Loan Origination",
        description="End-to-end loan origination process",
        owner="John Doe",
        criticality="Critical",
        sla_availability=99.99
    )
    print(capability.model_dump_json(indent=2))
