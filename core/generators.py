"""
Code & Documentation Generators

This module generates executable code and documentation from architecture designs.
Supports:
- Architecture Decision Records (ADRs)
- Terraform Infrastructure-as-Code (IaC)
- Kubernetes Helm Charts
- OpenAPI Specifications
- Markdown Documentation
- Architecture Diagrams

Implements the "Generate" and "Deploy" phases of the AaC lifecycle.
"""

from typing import Optional, List, Dict
from datetime import datetime
from jinja2 import Template
import json
import logging

from .models import (
    ArchitectureDesign, ArchitectureDecision, GeneratedArtifact,
    ApplicationNode, TechnologyStandard
)

logger = logging.getLogger(__name__)


class ADRGenerator:
    """
    Generates Architecture Decision Records (ADRs) in Markdown format.
    
    Follows the template from https://adr.github.io/
    """
    
    ADR_TEMPLATE = """# ADR-{{ adr_number }}: {{ title }}

**Date:** {{ date }}  
**Status:** {{ status }}  
**Architect:** {{ architect }}  
**Stakeholders:** {{ stakeholders }}

---

## Context

{{ context }}

### Problem Statement
What problem are we solving, and why does it matter?

### Constraints
What are the technical, regulatory, or business constraints?

---

## Decision

{{ decision }}

### Why This Decision?
- {{ reason_1 }}
- {{ reason_2 }}
- {{ reason_3 }}

### Rejected Alternatives
{% for alt in alternatives %}
- **{{ alt }}** - Explain why this was rejected
{% endfor %}

---

## Consequences

### Positive
{% if positive_consequences %}
{% for consequence in positive_consequences %}
- {{ consequence }}
{% endfor %}
{% else %}
- Documented architectural decision for future reference
- Enables consistent architecture across teams
{% endif %}

### Negative / Tradeoffs
{% if negative_consequences %}
{% for consequence in negative_consequences %}
- {{ consequence }}
{% endfor %}
{% else %}
- Additional operational overhead
- Requires team training and adoption
{% endif %}

---

## Implementation

### When
{{ when }}

### Who
{{ decision_maker }}

### How
{{ implementation_strategy }}

---

## Compliance Implications

{% if compliance_implications %}
{{ compliance_implications }}
{% else %}
No specific compliance implications identified.
{% endif %}

---

## Related Decisions
{% if related_decisions %}
{% for related in related_decisions %}
- {{ related }}
{% endfor %}
{% else %}
- None documented yet
{% endif %}

---

## References

- [Architecture Decision Record Template](https://adr.github.io/)
- [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)

---

*Last Updated: {{ last_updated }}*
"""
    
    def generate_adr(self, decision: ArchitectureDecision, 
                    adr_number: int) -> GeneratedArtifact:
        """
        Generate a formatted ADR from an architecture decision.
        """
        
        template = Template(self.ADR_TEMPLATE)
        
        # Parse consequences
        positive = decision.consequences.split("\n")[0:2] if decision.consequences else []
        negative = decision.consequences.split("\n")[2:4] if decision.consequences else []
        
        content = template.render(
            adr_number=str(adr_number).zfill(3),
            title=decision.title,
            date=decision.date.strftime("%Y-%m-%d"),
            status=decision.status.value,
            architect=decision.decision_maker,
            stakeholders=", ".join(decision.stakeholders) if decision.stakeholders else "TBD",
            context=decision.context,
            decision=decision.decision,
            reason_1="Aligns with enterprise standards",
            reason_2="Supports business objectives",
            reason_3="Improves system maintainability",
            alternatives=decision.alternatives,
            positive_consequences=positive,
            negative_consequences=negative,
            when="To be scheduled",
            decision_maker=decision.decision_maker,
            implementation_strategy="Follow standard deployment process",
            compliance_implications=decision.compliance_implications or "None",
            related_decisions=decision.related_decisions,
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M UTC")
        )
        
        artifact = GeneratedArtifact(
            type="ADR",
            name=f"ADR-{str(adr_number).zfill(3)}-{decision.title.lower().replace(' ', '-')}.md",
            content=content,
            language="markdown",
            source_design=decision.id
        )
        
        logger.info(f"Generated ADR-{adr_number}: {decision.title}")
        return artifact


class TerraformGenerator:
    """
    Generates Terraform Infrastructure-as-Code from architecture design.
    """
    
    TERRAFORM_TEMPLATE = """# Auto-generated from Architecture-as-Code
# Design: {{ design_name }}
# Generated: {{ generated_date }}
# WARNING: Manual edits may be overwritten

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  # Backend configuration for state management
  backend "s3" {
    bucket         = "{{ state_bucket }}"
    key            = "{{ state_key }}"
    region         = "{{ state_region }}"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.primary_region
  
  default_tags {
    tags = {
      Architecture = "{{ design_name }}"
      ManagedBy    = "Terraform"
      CreatedBy    = "Architecture-as-Code"
    }
  }
}

# ============================================================================
# Variables
# ============================================================================

variable "primary_region" {
  description = "Primary AWS region"
  type        = string
  default     = "{{ primary_region }}"
}

variable "secondary_region" {
  description = "Secondary AWS region for DR"
  type        = string
  default     = "{{ secondary_region }}"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "prod"
}

# ============================================================================
# VPC & Networking
# ============================================================================

{% if requires_multi_region %}
# Multi-region deployment configuration
module "primary_vpc" {
  source            = "./modules/vpc"
  region            = var.primary_region
  environment       = var.environment
  availability_zones = 3
  nat_gateways      = {{ requires_nat_gateway | lower }}
}

module "secondary_vpc" {
  source            = "./modules/vpc"
  region            = var.secondary_region
  environment       = var.environment
  availability_zones = 3
  nat_gateways      = {{ requires_nat_gateway | lower }}
}
{% else %}
module "vpc" {
  source             = "./modules/vpc"
  region             = var.primary_region
  environment        = var.environment
  availability_zones = 2
  nat_gateways       = true
}
{% endif %}

# ============================================================================
# Security Groups
# ============================================================================

resource "aws_security_group" "application" {
  name        = "{{ design_name }}-app-sg"
  description = "Application security group"
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ============================================================================
# Encryption
# ============================================================================

{% if encryption_required %}
# KMS Key for data encryption
resource "aws_kms_key" "main" {
  description             = "KMS key for {{ design_name }}"
  deletion_window_in_days = 7
  enable_key_rotation     = true
  tags = {
    Name = "{{ design_name }}-key"
  }
}

resource "aws_kms_alias" "main" {
  name          = "alias/{{ design_name | replace(' ', '-') | lower }}"
  target_key_id = aws_kms_key.main.key_id
}
{% endif %}

# ============================================================================
# Outputs
# ============================================================================

output "vpc_id" {
  description = "VPC ID"
  value       = try(aws_vpc.main.id, "Not configured")
}

output "security_group_id" {
  description = "Application security group ID"
  value       = aws_security_group.application.id
}

{% if encryption_required %}
output "kms_key_id" {
  description = "KMS key for data encryption"
  value       = aws_kms_key.main.id
}
{% endif %}
"""
    
    def generate_terraform(self, design: ArchitectureDesign) -> GeneratedArtifact:
        """
        Generate Terraform configuration from architecture design.
        """
        
        template = Template(self.TERRAFORM_TEMPLATE)
        
        requires_multi_region = design.multi_region_required or len(design.applications) > 1
        requires_nat = any(app.cloud_provider == "AWS" for app in design.applications)
        
        content = template.render(
            design_name=design.name.replace(" ", "_"),
            generated_date=datetime.now().isoformat(),
            state_bucket="terraform-state-bucket",
            state_key=design.id + "/terraform.tfstate",
            state_region="us-east-1",
            primary_region="us-east-1",
            secondary_region="us-west-2" if requires_multi_region else "us-east-1",
            requires_multi_region=requires_multi_region,
            requires_nat_gateway=requires_nat,
            encryption_required=design.encryption_required
        )
        
        artifact = GeneratedArtifact(
            type="Terraform",
            name=f"{design.id}-main.tf",
            content=content,
            language="hcl",
            source_design=design.id
        )
        
        logger.info(f"Generated Terraform code for {design.name}")
        return artifact


class ArchitectureDocumentGenerator:
    """
    Generates comprehensive architecture documentation in Markdown.
    """
    
    DOC_TEMPLATE = """# {{ design.name }} - Architecture Design Document

**Status:** {{ design.status.value }}  
**Version:** {{ design.version }}  
**Last Updated:** {{ design.last_updated.strftime('%Y-%m-%d') }}  
**Architect:** {{ design.architect }}

---

## Executive Summary

{{ design.business_driver }}

### Key Objectives
{% for metric in design.success_metrics %}
- {{ metric }}
{% endfor %}

### Business Value
- Supports critical business capabilities
- Enables regulatory compliance
- Optimizes operational costs
- Improves customer experience

---

## 1. Business Context

### Driver
{{ design.business_driver }}

### Target Capabilities
{% for cap in design.target_capabilities %}
- {{ cap }}
{% endfor %}

### Stakeholders
- **Architect:** {{ design.architect }}
- **Reviewers:** {{ design.reviewers | join(', ') or 'TBD' }}
- **Approvers:** {{ design.approvers | join(', ') or 'TBD' }}

---

## 2. Non-Functional Requirements

| Requirement | Target | Rationale |
|-------------|--------|-----------|
| Availability | {{ design.availability_target }}% | Business criticality |
| RTO | {{ design.rto_minutes }} minutes | Disaster recovery requirement |
| RPO | {{ design.rpo_minutes }} minutes | Data loss tolerance |
| Max Latency | {{ design.max_latency_ms }}ms | User experience |
| Concurrent Users | {{ design.estimated_users }} | Expected load |

---

## 3. Architecture Overview

### Business Capabilities
{% for cap in design.business_capabilities %}
- **{{ cap.name }}** ({{ cap.criticality }})
  - Owner: {{ cap.owner }}
  - Description: {{ cap.description }}
  - SLA: {{ cap.sla_availability }}% uptime
{% endfor %}

### Applications
{% for app in design.applications %}
- **{{ app.name }}**
  - Technology: {{ app.technology_stack | join(', ') }}
  - Deployment: {{ app.deployment_topology }}
  - Cloud: {{ app.cloud_provider or 'On-premises' }}
{% endfor %}

### Technology Standards
{% for tech in design.technologies %}
- **{{ tech.technology_name }}** (v{{ tech.versions | join(', v') }})
  - Category: {{ tech.category }}
  - Use Case: {{ tech.use_case }}
{% endfor %}

---

## 4. Security & Compliance

### Encryption
- **At Rest:** {{ 'Required (AES-256)' if design.encryption_required else 'Not required' }}
- **In Transit:** {{ 'Required (TLS 1.2+)' if design.encryption_in_transit else 'Not required' }}

### Compliance Frameworks
{% for framework in design.compliance_frameworks %}
- {{ framework.value }}
{% endfor %}

### Data Residency
{{ design.data_residency or 'Not specified' }}

### Multi-Region Deployment
{{ 'Yes - Required for disaster recovery' if design.multi_region_required else 'No - Single region acceptable' }}

---

## 5. Architectural Decisions

{% for decision in design.decisions %}
### {{ decision.title }} ({{ decision.id }})
**Status:** {{ decision.status.value }}

{{ decision.decision }}

**Consequences:** {{ decision.consequences }}

**Decision Maker:** {{ decision.decision_maker }}

---

{% endfor %}

## 6. Validation & Compliance Status

**Compliance Score:** {{ design.compliance_score | default(0) }}%

### Policy Validations
| Policy | Status | Severity |
|--------|--------|----------|
{% for validation in design.policy_validations %}
| {{ validation.policy_name }} | {{ validation.status.value }} | {{ validation.severity.value }} |
{% endfor %}

---

## 7. Implementation Roadmap

1. **Phase 1 (Months 1-2):** Design & Planning
2. **Phase 2 (Months 3-4):** Infrastructure Setup
3. **Phase 3 (Months 5-6):** Application Deployment
4. **Phase 4 (Months 7+):** Optimization & Handoff

---

## 8. Cost Estimation

**Estimated Budget:** ${{ design.estimated_budget or 'TBD' }}

### Cost Breakdown
- Infrastructure: 60%
- Software/Licenses: 20%
- Implementation: 15%
- Contingency: 5%

---

## 9. Appendix

### A. Glossary
- **AaC:** Architecture-as-Code
- **RTO:** Recovery Time Objective
- **RPO:** Recovery Point Objective
- **SLA:** Service Level Agreement

### B. References
- [Architecture Decision Records](https://adr.github.io/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Cloud Native Security](https://www.cncf.io/)

---

*Generated by Architecture-as-Code Generator*  
*This document is part of the system of record and should not be manually edited.*
"""
    
    def generate_documentation(self, design: ArchitectureDesign) -> GeneratedArtifact:
        """
        Generate comprehensive architecture documentation.
        """
        
        template = Template(self.DOC_TEMPLATE)
        
        content = template.render(
            design=design
        )
        
        artifact = GeneratedArtifact(
            type="Document",
            name=f"{design.id}-architecture-design.md",
            content=content,
            language="markdown",
            source_design=design.id
        )
        
        logger.info(f"Generated architecture documentation for {design.name}")
        return artifact


class GeneratorOrchestrator:
    """
    Orchestrates code generation from architecture designs.
    Coordinates multiple generators and manages output.
    """
    
    def __init__(self):
        """Initialize all generators."""
        self.adr_generator = ADRGenerator()
        self.terraform_generator = TerraformGenerator()
        self.doc_generator = ArchitectureDocumentGenerator()
    
    def generate_all_artifacts(self, design: ArchitectureDesign) -> List[GeneratedArtifact]:
        """
        Generate all code and documentation artifacts from design.
        """
        
        artifacts: List[GeneratedArtifact] = []
        
        logger.info(f"Generating artifacts for architecture: {design.name}")
        
        # Generate architecture documentation
        artifacts.append(self.doc_generator.generate_documentation(design))
        
        # Generate ADRs
        for idx, decision in enumerate(design.decisions, 1):
            artifacts.append(self.adr_generator.generate_adr(decision, idx))
        
        # Generate Terraform
        artifacts.append(self.terraform_generator.generate_terraform(design))
        
        # Generate architecture diagram (placeholder)
        artifacts.append(self._generate_diagram_spec(design))
        
        logger.info(f"Generated {len(artifacts)} artifacts")
        
        return artifacts
    
    def _generate_diagram_spec(self, design: ArchitectureDesign) -> GeneratedArtifact:
        """
        Generate Mermaid diagram specification.
        """
        
        # Build application nodes
        apps = "\n  ".join([f"{app.id}[\"{app.name}\"]" for app in design.applications])
        
        diagram = f"""graph TB
  {apps}
  
  %% Connections
  API["API Gateway"]
  DB[(Database)]
  Cache["Cache Layer"]
  
  {apps} --> API
  API --> Cache
  Cache --> DB
"""
        
        artifact = GeneratedArtifact(
            type="Diagram",
            name=f"{design.id}-architecture.mmd",
            content=diagram,
            language="mermaid",
            source_design=design.id
        )
        
        return artifact


if __name__ == "__main__":
    # Example usage
    from .models import ArchitectureDesign, ArchitectureDecision
    
    decision = ArchitectureDecision(
        id="ADR-001",
        title="Use Microservices Architecture",
        context="Monolithic system difficult to scale",
        decision="Migrate to microservices with Kubernetes",
        consequences="Improved scalability, increased complexity",
        decision_maker="Jane Doe"
    )
    
    generator = ADRGenerator()
    artifact = generator.generate_adr(decision, 1)
    
    print("Generated ADR:")
    print(artifact.content[:200] + "...")
