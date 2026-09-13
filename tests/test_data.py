"""
Synthetic Test Data Generator

Provides realistic example architectures and test cases for local testing
and demonstrations. All examples are based on real BFSI use cases.
"""

from core.models import (
    ArchitectureDesign, BusinessCapability, ApplicationNode,
    ArchitectureDecision, TechnologyStandard, CloudPattern,
    ComplianceFramework, DecisionStatus
)
from datetime import datetime, timedelta


def create_loan_origination_architecture() -> ArchitectureDesign:
    """
    Example: Loan Origination Platform for a bank
    Real-world scenario: Modernizing legacy loan system
    """
    
    # Business Capabilities
    capabilities = [
        BusinessCapability(
            id="BC-001",
            name="Loan Application Intake",
            description="End-to-end loan application submission and validation",
            owner="Digital Banking Team",
            criticality="Critical",
            sla_availability=99.99,
            sla_rto_minutes=15,
            sla_rpo_minutes=60
        ),
        BusinessCapability(
            id="BC-002",
            name="Credit Risk Assessment",
            description="Real-time credit scoring and risk evaluation",
            owner="Risk Management Team",
            criticality="Critical",
            sla_availability=99.95,
            sla_rto_minutes=30,
            sla_rpo_minutes=120
        ),
        BusinessCapability(
            id="BC-003",
            name="Document Management",
            description="Secure storage and audit trail for loan documents",
            owner="Compliance Team",
            criticality="Critical",
            sla_availability=99.9,
            sla_rto_minutes=60,
            sla_rpo_minutes=180
        ),
        BusinessCapability(
            id="BC-004",
            name="Loan Decisioning",
            description="Automated and manual approval workflow",
            owner="Lending Operations",
            criticality="High",
            sla_availability=99.9,
            sla_rto_minutes=120,
            sla_rpo_minutes=240
        ),
    ]
    
    # Applications
    applications = [
        ApplicationNode(
            id="APP-001",
            name="Loan Application Portal",
            description="Customer-facing web portal for loan applications",
            owner="Digital Banking Team",
            technology_stack=["React", "Node.js", "PostgreSQL"],
            deployment_topology="microservices",
            data_classification="confidential",
            criticality="Critical",
            cloud_provider="AWS",
            containers=True,
            managed_by="Platform Team"
        ),
        ApplicationNode(
            id="APP-002",
            name="Credit Risk Engine",
            description="ML-based credit scoring and risk assessment",
            owner="Risk Management",
            technology_stack=["Python", "TensorFlow", "PostgreSQL", "Redis"],
            deployment_topology="microservices",
            data_classification="restricted",
            criticality="Critical",
            cloud_provider="AWS",
            containers=True,
            managed_by="Data Science Platform"
        ),
        ApplicationNode(
            id="APP-003",
            name="Document Processing Service",
            description="OCR and document validation for loan documents",
            owner="Compliance Team",
            technology_stack=["Python", "Tesseract OCR", "ElasticSearch"],
            deployment_topology="microservices",
            data_classification="confidential",
            criticality="High",
            cloud_provider="AWS",
            containers=True,
            managed_by="Platform Team"
        ),
        ApplicationNode(
            id="APP-004",
            name="Decisioning Engine",
            description="Loan approval and conditional approval workflow",
            owner="Lending Operations",
            technology_stack=["Java", "Drools", "PostgreSQL"],
            deployment_topology="microservices",
            data_classification="confidential",
            criticality="Critical",
            cloud_provider="AWS",
            containers=True,
            managed_by="Platform Team"
        ),
        ApplicationNode(
            id="APP-005",
            name="Analytics & Reporting",
            description="Business intelligence and regulatory reporting",
            owner="Finance & Risk",
            technology_stack=["Python", "Tableau", "Snowflake"],
            deployment_topology="batch-processing",
            data_classification="internal",
            criticality="High",
            cloud_provider="AWS",
            containers=False,
            managed_by="Analytics Team"
        ),
    ]
    
    # Technology Standards
    technologies = [
        TechnologyStandard(
            id="TECH-001",
            category="Language",
            technology_name="Java",
            versions=["11", "17", "21"],
            use_case="Backend services, high-throughput systems",
            adoption_status="Approved",
            owner="Architecture Board",
            compliance_implications=[ComplianceFramework.DORA]
        ),
        TechnologyStandard(
            id="TECH-002",
            category="Language",
            technology_name="Python",
            versions=["3.9", "3.10", "3.11"],
            use_case="Data processing, ML/AI workloads",
            adoption_status="Approved",
            owner="Data Science Platform",
            compliance_implications=[ComplianceFramework.DORA]
        ),
        TechnologyStandard(
            id="TECH-003",
            category="Database",
            technology_name="PostgreSQL",
            versions=["13", "14", "15"],
            use_case="Transactional data, ACID compliance required",
            adoption_status="Approved",
            owner="Data Platform Team",
            compliance_implications=[ComplianceFramework.GDPR, ComplianceFramework.MIFID_II]
        ),
        TechnologyStandard(
            id="TECH-004",
            category="Cache",
            technology_name="Redis",
            versions=["6.2", "7.0"],
            use_case="Session cache, high-frequency data access",
            adoption_status="Approved",
            owner="Platform Team",
            compliance_implications=[ComplianceFramework.DORA]
        ),
        TechnologyStandard(
            id="TECH-005",
            category="Container Orchestration",
            technology_name="Kubernetes",
            versions=["1.26", "1.27", "1.28"],
            use_case="Container orchestration and auto-scaling",
            adoption_status="Approved",
            owner="Platform Engineering",
            compliance_implications=[ComplianceFramework.DORA, ComplianceFramework.SOX]
        ),
    ]
    
    # Architecture Decisions
    decisions = [
        ArchitectureDecision(
            id="ADR-001",
            title="Adopt Microservices Architecture",
            status=DecisionStatus.APPROVED,
            date=datetime.now() - timedelta(days=30),
            context="Monolithic loan system limits scalability and release velocity",
            decision="Migrate to microservices with Kubernetes orchestration",
            consequences="Improved scalability and independent service deployment; increased operational complexity",
            alternatives=["Modular monolith", "Service-oriented architecture"],
            compliance_implications="Enables independent service compliance validation",
            cost_impact="$2-3M migration cost, but $500K annual savings in operations",
            decision_maker="CTO",
            stakeholders=["Chief Architect", "VP Engineering", "VP Operations"],
            related_decisions=["ADR-002", "ADR-003"],
            tags=["architecture", "scalability", "microservices"]
        ),
        ArchitectureDecision(
            id="ADR-002",
            title="Use PostgreSQL for Primary Data Store",
            status=DecisionStatus.APPROVED,
            date=datetime.now() - timedelta(days=25),
            context="Need reliable, ACID-compliant transactional database for financial data",
            decision="Standardize on PostgreSQL 14+ for all transactional data",
            consequences="Strong consistency guarantees; mature ecosystem; proven in BFSI",
            alternatives=["Oracle", "MySQL", "SQL Server"],
            compliance_implications="Meets MiFID II record-keeping requirements",
            cost_impact="Open source license, lower TCO than Oracle",
            decision_maker="VP Architecture",
            stakeholders=["Database Team", "Compliance Officer"],
            tags=["database", "data-storage"]
        ),
        ArchitectureDecision(
            id="ADR-003",
            title="Implement Multi-Region Active-Active Deployment",
            status=DecisionStatus.APPROVED,
            date=datetime.now() - timedelta(days=20),
            context="DORA requires RTO ≤15 min and RPO ≤1 hour for critical systems",
            decision="Deploy to AWS us-east-1 and us-west-2 with active-active setup",
            consequences="Near-zero RTO/RPO; higher infrastructure costs; increased operational complexity",
            alternatives=["Active-passive failover", "Single region with backup"],
            compliance_implications="Meets DORA operational resilience requirements",
            cost_impact="$150K additional annual infrastructure cost",
            decision_maker="CTO",
            stakeholders=["Chief Risk Officer", "VP Operations"],
            tags=["disaster-recovery", "compliance", "dora"]
        ),
    ]
    
    # Create the architecture design
    design = ArchitectureDesign(
        id="ARCH-LOAN-2024-001",
        name="Loan Origination Platform v2.0",
        version="2.0.0",
        created_date=datetime.now() - timedelta(days=45),
        last_updated=datetime.now() - timedelta(days=2),
        status=DecisionStatus.APPROVED,
        architect="Sarah Johnson",
        stakeholders=["Chief Architect", "VP Engineering", "Chief Risk Officer", "Compliance Officer"],
        reviewers=["Enterprise Architecture Review Board"],
        approvers=["CTO", "Chief Risk Officer"],
        business_driver="Modernize loan origination system to support 10x growth, reduce time-to-approval from 2 days to 2 hours, achieve DORA compliance",
        target_capabilities=[
            "Loan Application Intake",
            "Credit Risk Assessment",
            "Document Management",
            "Loan Decisioning"
        ],
        success_metrics=[
            "Loan approval time < 2 hours for 80% of applications",
            "System availability 99.99%",
            "Zero compliance violations in audit",
            "50% reduction in loan processing costs",
            "10x increase in throughput"
        ],
        estimated_budget=2_500_000,
        target_go_live=datetime.now() + timedelta(days=180),
        business_capabilities=capabilities,
        applications=applications,
        technologies=technologies,
        decisions=decisions,
        availability_target=99.99,
        rto_minutes=15,
        rpo_minutes=60,
        max_latency_ms=200,
        estimated_users=100000,
        compliance_frameworks=[
            ComplianceFramework.DORA,
            ComplianceFramework.MIFID_II,
            ComplianceFramework.GDPR,
            ComplianceFramework.SOX
        ],
        data_residency="US (us-east-1 primary, us-west-2 secondary)",
        encryption_required=True,
        encryption_in_transit=True,
        multi_region_required=True,
    )
    
    return design


def create_payment_processing_architecture() -> ArchitectureDesign:
    """
    Example: Payment Processing Platform
    Real-world scenario: High-throughput payment processor
    """
    
    capabilities = [
        BusinessCapability(
            id="BC-101",
            name="Payment Acquisition",
            description="Receive and validate payment transactions",
            owner="Payments Team",
            criticality="Critical",
            sla_availability=99.99,
            sla_rto_minutes=5,
            sla_rpo_minutes=15
        ),
        BusinessCapability(
            id="BC-102",
            name="Transaction Routing",
            description="Route payments to appropriate processors",
            owner="Payments Platform",
            criticality="Critical",
            sla_availability=99.99,
            sla_rto_minutes=5,
            sla_rpo_minutes=15
        ),
        BusinessCapability(
            id="BC-103",
            name="Fraud Detection",
            description="Real-time fraud detection and prevention",
            owner="Risk Team",
            criticality="Critical",
            sla_availability=99.95,
            sla_rto_minutes=10,
            sla_rpo_minutes=30
        ),
    ]
    
    applications = [
        ApplicationNode(
            id="APP-P-001",
            name="Payment API Gateway",
            description="REST API for payment submission",
            owner="Payments Team",
            technology_stack=["Go", "gRPC", "Redis"],
            deployment_topology="microservices",
            data_classification="restricted",
            criticality="Critical",
            cloud_provider="AWS",
            containers=True
        ),
        ApplicationNode(
            id="APP-P-002",
            name="Fraud Detection Engine",
            description="ML-based real-time fraud detection",
            owner="Risk Team",
            technology_stack=["Python", "Kafka", "DynamoDB"],
            deployment_topology="event-driven",
            data_classification="confidential",
            criticality="Critical",
            cloud_provider="AWS",
            containers=True
        ),
        ApplicationNode(
            id="APP-P-003",
            name="Settlement Service",
            description="End-of-day settlement and reconciliation",
            owner="Finance Team",
            technology_stack=["Java", "PostgreSQL", "Kafka"],
            deployment_topology="batch-processing",
            data_classification="restricted",
            criticality="High",
            cloud_provider="AWS",
            containers=True
        ),
    ]
    
    design = ArchitectureDesign(
        id="ARCH-PAYMENT-2024-001",
        name="Payment Processing Platform",
        version="3.0.0",
        status=DecisionStatus.ACTIVE,
        architect="Michael Chen",
        business_driver="Handle 10,000 transactions per second with sub-100ms latency, PCI DSS compliance, real-time fraud detection",
        availability_target=99.99,
        rto_minutes=5,
        rpo_minutes=15,
        max_latency_ms=100,
        estimated_users=50000,
        compliance_frameworks=[
            ComplianceFramework.PCI_DSS,
            ComplianceFramework.GDPR,
            ComplianceFramework.SOX
        ],
        encryption_required=True,
        encryption_in_transit=True,
        multi_region_required=True,
        business_capabilities=capabilities,
        applications=applications,
    )
    
    return design


def create_data_mesh_architecture() -> ArchitectureDesign:
    """
    Example: Data Mesh Platform
    Real-world scenario: Decentralized data architecture
    """
    
    design = ArchitectureDesign(
        id="ARCH-DATAMESH-2024-001",
        name="Enterprise Data Mesh",
        version="1.0.0",
        status=DecisionStatus.PROPOSED,
        architect="Emma Williams",
        business_driver="Enable self-serve analytics with federated data domains, reduce time-to-insight",
        availability_target=99.9,
        rto_minutes=120,
        rpo_minutes=240,
        max_latency_ms=500,
        estimated_users=200,
        compliance_frameworks=[
            ComplianceFramework.GDPR,
            ComplianceFramework.MIFID_II
        ],
        encryption_required=True,
        encryption_in_transit=True,
        multi_region_required=False,
        success_metrics=[
            "100+ data products available",
            "50% faster time-to-insight",
            "Self-serve analytics adoption >80%"
        ],
    )
    
    return design


def get_all_test_architectures():
    """Get all test architectures for demonstration"""
    return [
        create_loan_origination_architecture(),
        create_payment_processing_architecture(),
        create_data_mesh_architecture(),
    ]


if __name__ == "__main__":
    print("\n=== Test Architecture Examples ===\n")
    
    architectures = get_all_test_architectures()
    
    for arch in architectures:
        print(f"📋 {arch.name}")
        print(f"   Status: {arch.status.value}")
        print(f"   Architect: {arch.architect}")
        print(f"   Applications: {len(arch.applications)}")
        print(f"   Compliance Frameworks: {len(arch.compliance_frameworks)}")
        print(f"   Availability Target: {arch.availability_target}%")
        print()
