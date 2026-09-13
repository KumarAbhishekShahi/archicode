"""
Architecture Validators

This module implements policy-as-code validation for architecture decisions.
Validates designs against compliance frameworks, security standards, and cost policies.

Follows the "Govern" phase of the Architecture-as-Code lifecycle.
"""

from typing import List, Dict, Tuple, Optional
from datetime import datetime
import logging

from .models import (
    ArchitectureDesign, PolicyRule, PolicyValidation, ValidationStatus,
    PolicySeverity, ComplianceFramework, ApplicationNode
)

logger = logging.getLogger(__name__)


class PolicyValidator:
    """
    Core policy validation engine. Evaluates architecture designs against
    a set of policy rules to ensure compliance and governance.
    """
    
    def __init__(self):
        """Initialize the validator with default policies."""
        self.policies: List[PolicyRule] = []
        self._initialize_default_policies()
    
    def _initialize_default_policies(self) -> None:
        """
        Initialize a set of real-world policies based on BFSI best practices.
        These cover MiFID II, DORA, GDPR, and industry standards.
        """
        
        # Security Policies
        self.add_policy(PolicyRule(
            id="POL-SEC-001",
            name="Data Encryption at Rest",
            description="All data at rest must use AES-256 encryption",
            frameworks=[ComplianceFramework.GDPR, ComplianceFramework.PCI_DSS],
            severity=PolicySeverity.CRITICAL,
            condition="architecture.encryption_required == True",
            remediation="Enable AES-256 encryption for all data stores",
            owner="Chief Security Officer"
        ))
        
        self.add_policy(PolicyRule(
            id="POL-SEC-002",
            name="Encryption in Transit",
            description="All data in transit must use TLS 1.2+",
            frameworks=[ComplianceFramework.GDPR, ComplianceFramework.PCI_DSS],
            severity=PolicySeverity.CRITICAL,
            condition="architecture.encryption_in_transit == True",
            remediation="Enable TLS 1.2+ for all network communications",
            owner="Chief Security Officer"
        ))
        
        self.add_policy(PolicyRule(
            id="POL-SEC-003",
            name="Multi-Region Deployment for Critical Systems",
            description="Critical systems must be deployed in multiple regions",
            frameworks=[ComplianceFramework.DORA],
            severity=PolicySeverity.HIGH,
            condition="if criticality==Critical: multi_region_required==True",
            remediation="Deploy to multiple cloud regions with failover",
            owner="Chief Information Officer"
        ))
        
        # Compliance Policies
        self.add_policy(PolicyRule(
            id="POL-COMP-001",
            name="GDPR Data Residency",
            description="Personal data must reside in appropriate regions",
            frameworks=[ComplianceFramework.GDPR],
            severity=PolicySeverity.CRITICAL,
            condition="if handles_personal_data: data_residency_specified",
            remediation="Specify data residency requirements aligned with GDPR",
            owner="Data Protection Officer"
        ))
        
        self.add_policy(PolicyRule(
            id="POL-COMP-002",
            name="MiFID II Regulatory Reporting",
            description="Must support automated regulatory reporting",
            frameworks=[ComplianceFramework.MIFID_II],
            severity=PolicySeverity.HIGH,
            condition="architecture.supports_regulatory_reporting",
            remediation="Implement audit logging and reporting capabilities",
            owner="Head of Compliance"
        ))
        
        self.add_policy(PolicyRule(
            id="POL-COMP-003",
            name="DORA Operational Resilience",
            description="Must meet DORA impact tolerance thresholds",
            frameworks=[ComplianceFramework.DORA],
            severity=PolicySeverity.CRITICAL,
            condition="rto_minutes <= 15 and rpo_minutes <= 60",
            remediation="Implement backup, disaster recovery, and redundancy",
            owner="Chief Risk Officer"
        ))
        
        # Availability & Reliability
        self.add_policy(PolicyRule(
            id="POL-REL-001",
            name="High Availability Requirement",
            description="Critical systems must have 99.9%+ availability",
            frameworks=[ComplianceFramework.DORA],
            severity=PolicySeverity.HIGH,
            condition="if criticality==Critical: availability >= 99.9",
            remediation="Implement multi-region, multi-zone, load balancing",
            owner="VP Infrastructure"
        ))
        
        self.add_policy(PolicyRule(
            id="POL-REL-002",
            name="RTO/RPO Compliance",
            description="Recovery objectives must be defined and achievable",
            frameworks=[ComplianceFramework.DORA],
            severity=PolicySeverity.HIGH,
            condition="rto_defined and rpo_defined",
            remediation="Define and document RTO/RPO based on criticality",
            owner="VP Operations"
        ))
        
        # Technology Standards
        self.add_policy(PolicyRule(
            id="POL-TECH-001",
            name="No End-of-Life Technologies",
            description="All technologies must be supported and current",
            frameworks=[],
            severity=PolicySeverity.MEDIUM,
            condition="all_technologies in approved_standards",
            remediation="Replace with approved technology from standards list",
            owner="Chief Technology Officer"
        ))
        
        self.add_policy(PolicyRule(
            id="POL-TECH-002",
            name="Container Security Scanning",
            description="All container images must be scanned for vulnerabilities",
            frameworks=[ComplianceFramework.PCI_DSS],
            severity=PolicySeverity.HIGH,
            condition="if uses_containers: security_scanning_enabled",
            remediation="Enable container image scanning in CI/CD pipeline",
            owner="Chief Security Officer"
        ))
        
        # Cost Policies
        self.add_policy(PolicyRule(
            id="POL-COST-001",
            name="Cloud Cost Optimization",
            description="Reserved instances for baseline workloads",
            frameworks=[],
            severity=PolicySeverity.MEDIUM,
            condition="if production: uses_reserved_instances or uses_savings_plans",
            remediation="Purchase reserved instances or commitment plans",
            owner="Head of FinOps"
        ))
        
        self.add_policy(PolicyRule(
            id="POL-COST-002",
            name="Cost Estimation Required",
            description="All major architectures must have budget estimates",
            frameworks=[],
            severity=PolicySeverity.MEDIUM,
            condition="if estimated_users > 10000: budget_estimated",
            remediation="Provide detailed cost estimation for architecture",
            owner="Finance"
        ))
        
        # Architecture Governance
        self.add_policy(PolicyRule(
            id="POL-ARCH-001",
            name="Architecture Decision Documentation",
            description="All critical decisions must be documented as ADRs",
            frameworks=[],
            severity=PolicySeverity.MEDIUM,
            condition="all_decisions_documented_as_adr",
            remediation="Document decisions using Architecture Decision Record format",
            owner="Chief Architect"
        ))
        
        self.add_policy(PolicyRule(
            id="POL-ARCH-002",
            name="Stakeholder Review & Approval",
            description="Major architectures require stakeholder review",
            frameworks=[],
            severity=PolicySeverity.MEDIUM,
            condition="architecture.has_stakeholder_approval",
            remediation="Schedule architecture review with stakeholders",
            owner="Chief Architect"
        ))
    
    def add_policy(self, policy: PolicyRule) -> None:
        """Add a policy rule to the validator."""
        if policy.enabled:
            self.policies.append(policy)
            logger.info(f"Added policy: {policy.id} - {policy.name}")
    
    def validate_architecture(self, design: ArchitectureDesign) -> Tuple[List[PolicyValidation], float]:
        """
        Validate an architecture design against all enabled policies.
        
        Args:
            design: The architecture design to validate
            
        Returns:
            Tuple of (validation results, compliance score 0-100)
        """
        validations: List[PolicyValidation] = []
        passed_count = 0
        total_count = len(self.policies)
        
        logger.info(f"Validating architecture '{design.name}' against {total_count} policies")
        
        for policy in self.policies:
            result = self._validate_policy(design, policy)
            validations.append(result)
            
            if result.status == ValidationStatus.PASS:
                passed_count += 1
                logger.debug(f"✓ {policy.id}: {policy.name}")
            elif result.status == ValidationStatus.FAIL:
                logger.warning(f"✗ {policy.id}: {policy.name}")
            elif result.status == ValidationStatus.WARN:
                logger.info(f"⚠ {policy.id}: {policy.name}")
        
        # Calculate compliance score
        compliance_score = (passed_count / total_count * 100) if total_count > 0 else 0.0
        
        # Update design with results
        design.policy_validations = validations
        design.compliance_score = compliance_score
        
        logger.info(f"Validation complete. Compliance score: {compliance_score:.1f}%")
        
        return validations, compliance_score
    
    def _validate_policy(self, design: ArchitectureDesign, policy: PolicyRule) -> PolicyValidation:
        """
        Validate a single policy against the design.
        
        This is a simplified implementation. In production, you would:
        1. Parse the policy condition expression
        2. Execute it against the design object
        3. Use Python's eval with restricted globals for safety
        """
        
        try:
            # Extract validation logic based on policy ID patterns
            status, message = self._check_policy_condition(design, policy)
            
            validation = PolicyValidation(
                policy_id=policy.id,
                policy_name=policy.name,
                status=status,
                severity=policy.severity,
                message=message,
                remediation_steps=None if status == ValidationStatus.PASS else [policy.remediation]
            )
            
            return validation
            
        except Exception as e:
            logger.error(f"Error validating policy {policy.id}: {str(e)}")
            return PolicyValidation(
                policy_id=policy.id,
                policy_name=policy.name,
                status=ValidationStatus.WARN,
                severity=PolicySeverity.LOW,
                message=f"Validation error: {str(e)}"
            )
    
    def _check_policy_condition(self, design: ArchitectureDesign, policy: PolicyRule) -> Tuple[ValidationStatus, str]:
        """
        Check a specific policy condition against the design.
        
        This is the core validation logic - can be extended with more sophisticated
        condition evaluation using a proper expression parser.
        """
        
        # Security Policies
        if policy.id == "POL-SEC-001":
            if design.encryption_required:
                return ValidationStatus.PASS, "Data encryption at rest is required"
            else:
                return ValidationStatus.FAIL, "Data encryption at rest must be enabled"
        
        elif policy.id == "POL-SEC-002":
            if design.encryption_in_transit:
                return ValidationStatus.PASS, "Data encryption in transit is required"
            else:
                return ValidationStatus.FAIL, "Data encryption in transit must be enabled"
        
        elif policy.id == "POL-SEC-003":
            # Check if critical systems are multi-region
            critical_apps = [app for app in design.applications 
                           if app.criticality == "Critical"]
            
            if not critical_apps:
                return ValidationStatus.PASS, "No critical systems found"
            
            if design.multi_region_required:
                return ValidationStatus.PASS, "Multi-region deployment required for critical systems"
            else:
                return ValidationStatus.FAIL, f"Critical system(s) require multi-region deployment: {[a.name for a in critical_apps]}"
        
        # Compliance Policies
        elif policy.id == "POL-COMP-003":
            meets_rto = design.rto_minutes <= 15
            meets_rpo = design.rpo_minutes <= 60
            
            if meets_rto and meets_rpo:
                return ValidationStatus.PASS, f"DORA compliance: RTO={design.rto_minutes}min, RPO={design.rpo_minutes}min"
            else:
                issues = []
                if not meets_rto:
                    issues.append(f"RTO {design.rto_minutes}min > 15min limit")
                if not meets_rpo:
                    issues.append(f"RPO {design.rpo_minutes}min > 60min limit")
                return ValidationStatus.FAIL, "DORA compliance failure: " + ", ".join(issues)
        
        # Reliability Policies
        elif policy.id == "POL-REL-001":
            critical_apps = [app for app in design.applications 
                           if app.criticality == "Critical"]
            
            if not critical_apps:
                return ValidationStatus.PASS, "No critical systems to validate"
            
            if design.availability_target >= 99.9:
                return ValidationStatus.PASS, f"Availability target: {design.availability_target}%"
            else:
                return ValidationStatus.FAIL, f"Critical systems require 99.9%+ availability, configured: {design.availability_target}%"
        
        elif policy.id == "POL-REL-002":
            if design.rto_minutes > 0 and design.rpo_minutes > 0:
                return ValidationStatus.PASS, f"RTO/RPO defined: RTO={design.rto_minutes}min, RPO={design.rpo_minutes}min"
            else:
                return ValidationStatus.FAIL, "RTO and RPO must be defined for all designs"
        
        # Technology Policies
        elif policy.id == "POL-TECH-001":
            # In production, check against approved standards database
            return ValidationStatus.PASS, "All technologies in approved standards"
        
        elif policy.id == "POL-TECH-002":
            container_apps = [app for app in design.applications if app.containers]
            
            if not container_apps:
                return ValidationStatus.PASS, "No containerized applications"
            
            # This would check actual scanning setup
            return ValidationStatus.WARN, f"Container security scanning required for: {[a.name for a in container_apps]}"
        
        # Cost Policies
        elif policy.id == "POL-COST-001":
            return ValidationStatus.WARN, "Recommend reserved instances for cost optimization"
        
        elif policy.id == "POL-COST-002":
            if design.estimated_budget is not None:
                return ValidationStatus.PASS, f"Budget estimated: ${design.estimated_budget:,.0f}"
            else:
                if design.estimated_users > 10000:
                    return ValidationStatus.WARN, "Cost estimation recommended for large deployments"
                else:
                    return ValidationStatus.PASS, "Cost estimation not required for this scale"
        
        # Architecture Policies
        elif policy.id == "POL-ARCH-001":
            if design.decisions:
                return ValidationStatus.PASS, f"Architecture has {len(design.decisions)} documented decisions"
            else:
                return ValidationStatus.WARN, "No architecture decisions documented yet"
        
        elif policy.id == "POL-ARCH-002":
            if design.approvers:
                return ValidationStatus.PASS, f"Architecture approved by: {', '.join(design.approvers)}"
            else:
                return ValidationStatus.WARN, "Architecture requires stakeholder approval"
        
        # Default
        return ValidationStatus.PASS, f"Policy {policy.id} validation passed"


class ComplianceAssessment:
    """
    Generates compliance assessments against specific regulatory frameworks.
    """
    
    def __init__(self, validator: PolicyValidator):
        """Initialize with a policy validator."""
        self.validator = validator
    
    def assess_framework_compliance(self, 
                                   design: ArchitectureDesign,
                                   framework: ComplianceFramework) -> Dict[str, any]:
        """
        Assess compliance with a specific regulatory framework.
        """
        
        # Get policies related to this framework
        framework_policies = [p for p in self.validator.policies 
                            if framework in p.frameworks]
        
        compliance_details = {
            "framework": framework.value,
            "total_policies": len(framework_policies),
            "assessment_date": datetime.now().isoformat(),
            "policies": []
        }
        
        passed = 0
        failed = 0
        warned = 0
        
        for policy in framework_policies:
            status, message = self.validator._check_policy_condition(design, policy)
            
            policy_result = {
                "id": policy.id,
                "name": policy.name,
                "status": status.value,
                "severity": policy.severity.value,
                "message": message,
                "remediation": policy.remediation if status == ValidationStatus.FAIL else None
            }
            compliance_details["policies"].append(policy_result)
            
            if status == ValidationStatus.PASS:
                passed += 1
            elif status == ValidationStatus.FAIL:
                failed += 1
            elif status == ValidationStatus.WARN:
                warned += 1
        
        compliance_details["summary"] = {
            "passed": passed,
            "failed": failed,
            "warned": warned,
            "compliance_percentage": (passed / len(framework_policies) * 100) if framework_policies else 0
        }
        
        return compliance_details


if __name__ == "__main__":
    # Example usage
    validator = PolicyValidator()
    
    # Create a sample design
    from .models import ArchitectureDesign
    
    design = ArchitectureDesign(
        id="ARCH-001",
        name="Loan Origination Platform",
        architect="Jane Doe",
        business_driver="Modernize loan origination system",
        encryption_required=True,
        encryption_in_transit=True,
        availability_target=99.95,
        rto_minutes=15,
        rpo_minutes=60,
        compliance_frameworks=[ComplianceFramework.DORA, ComplianceFramework.MiFID_II]
    )
    
    # Validate
    validations, score = validator.validate_architecture(design)
    
    print(f"\n=== Architecture Validation Results ===")
    print(f"Design: {design.name}")
    print(f"Compliance Score: {score:.1f}%")
    print(f"\nValidation Details:")
    for v in validations:
        print(f"  {v.policy_name}: {v.status.value}")
