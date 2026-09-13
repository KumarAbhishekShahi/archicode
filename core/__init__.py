"""
Architecture-as-Code Generator - Core Module

This package contains the core functionality for the AaC generator:
- Data models (Pydantic)
- Policy validators
- Code generators
- Repository management
"""

from .models import (
    ArchitectureDesign,
    ArchitectureDecision,
    BusinessCapability,
    ApplicationNode,
    TechnologyStandard,
    CloudPattern,
    PolicyRule,
    PolicyValidation,
    ValidationStatus,
    DecisionStatus,
    ComplianceFramework,
)

from .validators import (
    PolicyValidator,
    ComplianceAssessment,
)

from .generators import (
    ADRGenerator,
    TerraformGenerator,
    ArchitectureDocumentGenerator,
    GeneratorOrchestrator,
    GeneratedArtifact,
)

__version__ = "1.0.0"
__author__ = "Architecture-as-Code Team"
__all__ = [
    # Models
    "ArchitectureDesign",
    "ArchitectureDecision",
    "BusinessCapability",
    "ApplicationNode",
    "TechnologyStandard",
    "CloudPattern",
    "PolicyRule",
    "PolicyValidation",
    "ValidationStatus",
    "DecisionStatus",
    "ComplianceFramework",
    # Validators
    "PolicyValidator",
    "ComplianceAssessment",
    # Generators
    "ADRGenerator",
    "TerraformGenerator",
    "ArchitectureDocumentGenerator",
    "GeneratorOrchestrator",
    "GeneratedArtifact",
]
