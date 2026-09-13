"""
Architecture-as-Code Generator - Main Streamlit Application

A comprehensive web UI for generating, validating, and governing enterprise architecture
in banking and financial services environments.

This application implements the full Architecture-as-Code lifecycle:
Model → Validate → Govern → Generate → Deploy → Observe → Reconcile
"""

import streamlit as st
from datetime import datetime
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.models import (
    ArchitectureDesign, BusinessCapability, ApplicationNode, ArchitectureDecision,
    TechnologyStandard, CloudPattern, ComplianceFramework, DecisionStatus
)
from core.validators import PolicyValidator, ComplianceAssessment
from core.generators import GeneratorOrchestrator


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="ArchiCode",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UX
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)


# ============================================================================
# SESSION STATE & INITIALIZATION
# ============================================================================

def initialize_session_state():
    """Initialize session state variables."""
    if 'current_design' not in st.session_state:
        st.session_state.current_design = None
    
    if 'validator' not in st.session_state:
        st.session_state.validator = PolicyValidator()
    
    if 'generator' not in st.session_state:
        st.session_state.generator = GeneratorOrchestrator()
    
    if 'validations' not in st.session_state:
        st.session_state.validations = []
    
    if 'artifacts' not in st.session_state:
        st.session_state.artifacts = []


initialize_session_state()


# ============================================================================
# DEMO MODE
# ============================================================================

def load_demo_architecture():
    """Load a demo architecture for testing"""
    from tests.test_data import create_loan_origination_architecture
    st.session_state.current_design = create_loan_origination_architecture()
    st.success("✅ Demo architecture loaded! Check the Model tab.")


# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    st.title("🏗️ ArchiCode V1.0")
    st.markdown("---")
    
    # Demo Mode Quick Access
    st.subheader("🚀 Quick Demo")
    if st.button("📥 Load Demo Architecture"):
        load_demo_architecture()
        st.rerun()
    
    st.markdown("---")
    
    st.subheader("📋 Navigation")
    
    page = st.radio(
        "Select Phase:",
        options=[
            "🏠 Home",
            "🎯 Model",
            "✅ Validate",
            "🛡️ Govern",
            "⚙️ Generate",
            "🚀 Deploy",
            "👁️ Observe",
            "🔄 Reconcile"
        ]
    )
    
    st.markdown("---")
    st.subheader("📊 Current Design")
    
    if st.session_state.current_design:
        st.info(f"**{st.session_state.current_design.name}**\n\n"
                f"Status: {st.session_state.current_design.status.value}\n\n"
                f"Compliance Score: {st.session_state.current_design.compliance_score:.1f}%")
        
        if st.button("🗑️ Clear Design"):
            st.session_state.current_design = None
            st.rerun()
    else:
        st.warning("No active design. Create one in the Model phase.")
    
    st.markdown("---")
    st.subheader("ℹ️ Help & Documentation")
    
    with st.expander("About AaC"):
        st.markdown("""
        **Architecture-as-Code** represents enterprise architecture decisions
        in machine-readable, policy-validated form.
        
        **Key Benefits:**
        - ✅ Automated governance and compliance checking
        - 🔄 Continuous alignment with business outcomes
        - 📊 Real-time architecture drift detection
        - 🤖 AI-assisted architecture review
        - 📈 Improved decision quality and speed
        """)
    
    with st.expander("Maturity Levels"):
        st.markdown("""
        1. **DOCUMENTED** - PowerPoint/Visio
        2. **VERSIONED** - Git + ADRs
        3. **STRUCTURED** - YAML/JSON models
        4. **POLICY-DRIVEN** - Automated validation
        5. **AUTOMATED** - IaC + CI/CD
        6. **AGENTIC** - AI agents
        7. **AUTONOMOUS** - Continuous reconciliation
        """)


# ============================================================================
# HOME PAGE
# ============================================================================

if "🏠" in page:
    st.title("🏗️ ArchiCode")
    st.markdown("*From Architectural Intent to Real-World Impact*")
    
    st.markdown("---")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Policies", 15, "Enforcement rules")
    
    with col2:
        st.metric("Frameworks", 6, "Compliance standards")
    
    with col3:
        st.metric("Maturity Levels", 7, "Assessment model")
    
    with col4:
        st.metric("Generators", 5, "Artifact types")
    
    st.markdown("---")
    
    # Overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 What is ArchiCode?")
        st.markdown("""
        AaC is the practice of representing enterprise architecture decisions,
        design patterns, and policies in machine-readable, validatable form.
        
        This enables:
        - **Faster decisions** through automation
        - **Better compliance** through policy validation
        - **Continuous governance** of architecture
        - **AI-assisted review** and improvement
        """)
    
    with col2:
        st.subheader("📊 The AaC Lifecycle")
        st.markdown("""
        ```
        1. MODEL → Define architecture
        2. VALIDATE → Check policies
        3. GOVERN → Apply controls
        4. GENERATE → Create code
        5. DEPLOY → Release IaC
        6. OBSERVE → Monitor drift
        7. RECONCILE → Improve continuously
        ```
        """)
    
    st.markdown("---")
    
    # Quick start
    st.subheader("🚀 Quick Start")
    
    tabs = st.tabs(["Create Design", "Load Template", "View Examples"])
    
    with tabs[0]:
        col1, col2 = st.columns(2)
        
        with col1:
            design_name = st.text_input("Architecture Name", 
                                       value="Loan Origination Platform")
            architect = st.text_input("Architect Name", value="Jane Doe")
            business_driver = st.text_area("Business Driver",
                                          value="Modernize loan origination to support rapid growth")
        
        with col2:
            criticality = st.selectbox("Criticality", ["Critical", "High", "Medium", "Low"])
            compliance = st.multiselect("Compliance Frameworks",
                                       options=[f.value for f in ComplianceFramework],
                                       default=["MiFID II", "DORA"])
            budget = st.number_input("Estimated Budget ($M)", min_value=0.1, max_value=100.0, step=0.5)
        
        if st.button("✨ Create Design", key="create_design"):
            design = ArchitectureDesign(
                id=f"ARCH-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                name=design_name,
                architect=architect,
                business_driver=business_driver,
                estimated_budget=budget * 1_000_000,
                compliance_frameworks=[ComplianceFramework(c) for c in compliance],
                status=DecisionStatus.DRAFT
            )
            st.session_state.current_design = design
            st.success("✅ Architecture created! Now go to **Model** phase to add details.")
            st.balloons()
    
    with tabs[1]:
        st.info("Template library coming soon...")
    
    with tabs[2]:
        st.markdown("""
        ### Example: Financial Services Platform
        
        **Scenario:** A bank needs to modernize its core banking system
        
        - **Business Driver:** Enable digital transformation
        - **Technology Stack:** Microservices, Kubernetes, PostgreSQL
        - **Compliance:** MiFID II, DORA, GDPR
        - **Availability Target:** 99.99%
        
        This example demonstrates how AaC handles complex BFSI requirements.
        """)


# ============================================================================
# MODEL PHASE
# ============================================================================

elif "🎯 Model" in page:
    st.title("🎯 Model - Architecture Definition")
    st.markdown("Define business capabilities, applications, and technology decisions")
    
    if not st.session_state.current_design:
        st.warning("⚠️ No design selected. Please create one on the Home page first.")
        st.stop()
    
    design = st.session_state.current_design
    
    tabs = st.tabs(["Design Metadata", "Business Capabilities", "Applications", "Technologies", "Decisions"])
    
    # TAB 1: Design Metadata
    with tabs[0]:
        st.subheader("Design Metadata")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            design.name = st.text_input("Architecture Name", value=design.name)
            design.architect = st.text_input("Lead Architect", value=design.architect)
        
        with col2:
            design.business_driver = st.text_area("Business Driver", value=design.business_driver)
            design.estimated_budget = st.number_input("Budget ($)", value=design.estimated_budget, step=100000.0)
        
        with col3:
            design.availability_target = st.slider("Target Availability (%)", 99.0, 99.99, value=design.availability_target)
            design.rto_minutes = st.number_input("RTO (minutes)", value=design.rto_minutes, min_value=1)
            design.rpo_minutes = st.number_input("RPO (minutes)", value=design.rpo_minutes, min_value=1)
    
    # TAB 2: Business Capabilities
    with tabs[1]:
        st.subheader("Business Capabilities")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cap_name = st.text_input("Capability Name", value="Loan Origination")
            cap_owner = st.text_input("Owner", value="John Doe")
            cap_description = st.text_area("Description", value="End-to-end loan origination process")
        
        with col2:
            cap_criticality = st.selectbox("Criticality", ["Critical", "High", "Medium", "Low"], key="cap_crit")
            cap_sla = st.number_input("SLA (%)", min_value=90.0, max_value=99.99, value=99.9)
        
        if st.button("➕ Add Capability"):
            capability = BusinessCapability(
                id=f"BC-{len(design.business_capabilities) + 1:03d}",
                name=cap_name,
                description=cap_description,
                owner=cap_owner,
                criticality=cap_criticality,
                sla_availability=cap_sla
            )
            design.business_capabilities.append(capability)
            st.success(f"✅ Added capability: {cap_name}")
        
        if design.business_capabilities:
            st.markdown("### Current Capabilities")
            for cap in design.business_capabilities:
                with st.expander(f"📌 {cap.name}"):
                    st.write(f"**Owner:** {cap.owner}")
                    st.write(f"**Criticality:** {cap.criticality}")
                    st.write(f"**SLA:** {cap.sla_availability}%")
                    st.write(f"**Description:** {cap.description}")
    
    # TAB 3: Applications
    with tabs[2]:
        st.subheader("Applications")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            app_name = st.text_input("Application Name", value="Core Banking System")
            app_owner = st.text_input("Owner", value="Platform Team")
            app_criticality = st.selectbox("Criticality", ["Critical", "High", "Medium", "Low"], key="app_crit")
        
        with col2:
            app_topology = st.selectbox("Deployment", ["Monolith", "Microservices", "Serverless"])
            app_cloud = st.selectbox("Cloud Provider", ["AWS", "Azure", "GCP", "On-Premises"])
            app_containers = st.checkbox("Uses Containers/Kubernetes")
        
        with col3:
            app_classification = st.selectbox("Data Classification", 
                                             ["Public", "Internal", "Confidential", "Restricted"])
            tech_stack = st.multiselect("Technology Stack",
                                       ["Java", "Python", "Node.js", "Go", "Rust", ".NET"],
                                       default=["Java"])
        
        if st.button("➕ Add Application"):
            app = ApplicationNode(
                id=f"APP-{len(design.applications) + 1:03d}",
                name=app_name,
                description=f"{app_name} application",
                owner=app_owner,
                criticality=app_criticality,
                deployment_topology=app_topology,
                cloud_provider=app_cloud,
                containers=app_containers,
                data_classification=app_classification,
                technology_stack=tech_stack
            )
            design.applications.append(app)
            st.success(f"✅ Added application: {app_name}")
        
        if design.applications:
            st.markdown("### Current Applications")
            for app in design.applications:
                with st.expander(f"🔧 {app.name}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Owner:** {app.owner}")
                        st.write(f"**Criticality:** {app.criticality}")
                        st.write(f"**Cloud:** {app.cloud_provider}")
                    with col2:
                        st.write(f"**Topology:** {app.deployment_topology}")
                        st.write(f"**Containers:** {'✅ Yes' if app.containers else '❌ No'}")
                        st.write(f"**Tech Stack:** {', '.join(app.technology_stack)}")
    
    # TAB 4: Technologies
    with tabs[3]:
        st.subheader("Technology Standards")
        st.info("Define approved technologies and versions for this architecture")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tech_category = st.selectbox("Category", ["Database", "Language", "Framework", "Platform"])
            tech_name = st.text_input("Technology Name", value="PostgreSQL")
            versions = st.text_input("Approved Versions (comma-separated)", value="14, 15, 16")
        
        with col2:
            use_case = st.text_input("Use Case", value="Primary relational database")
            adoption_status = st.selectbox("Adoption Status", ["Approved", "Trial", "Deprecated", "Prohibited"])
        
        with col3:
            owner = st.text_input("Technology Owner", value="Data Platform Team")
            compliance_frameworks = st.multiselect("Compliance Frameworks",
                                                   options=[f.value for f in ComplianceFramework])
        
        if st.button("➕ Add Technology"):
            tech = TechnologyStandard(
                id=f"TECH-{len(design.technologies) + 1:03d}",
                category=tech_category,
                technology_name=tech_name,
                versions=versions.split(","),
                use_case=use_case,
                adoption_status=adoption_status,
                owner=owner,
                compliance_implications=[ComplianceFramework(c) for c in compliance_frameworks] if compliance_frameworks else []
            )
            design.technologies.append(tech)
            st.success(f"✅ Added technology: {tech_name}")
        
        if design.technologies:
            st.markdown("### Current Technologies")
            for tech in design.technologies:
                st.write(f"**{tech.technology_name}** - {tech.adoption_status}")
                st.write(f"Versions: {', '.join(tech.versions)}")
    
    # TAB 5: Decisions
    with tabs[4]:
        st.subheader("Architecture Decisions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            decision_title = st.text_input("Decision Title", value="Use Microservices")
            decision_context = st.text_area("Context/Problem", value="Monolith limits scalability")
        
        with col2:
            decision_desc = st.text_area("Decision & Rationale", value="Adopt microservices with Kubernetes")
            decision_consequences = st.text_area("Consequences", value="Better scalability, increased complexity")
        
        decision_maker = st.text_input("Decision Maker", value=design.architect)
        
        if st.button("➕ Add Decision"):
            decision = ArchitectureDecision(
                id=f"ADR-{len(design.decisions) + 1:03d}",
                title=decision_title,
                context=decision_context,
                decision=decision_desc,
                consequences=decision_consequences,
                decision_maker=decision_maker,
                status=DecisionStatus.PROPOSED
            )
            design.decisions.append(decision)
            st.success(f"✅ Added decision: {decision_title}")
        
        if design.decisions:
            st.markdown("### Current Decisions")
            for decision in design.decisions:
                with st.expander(f"📋 {decision.title} ({decision.id})"):
                    st.write(f"**Status:** {decision.status.value}")
                    st.write(f"**Maker:** {decision.decision_maker}")
                    st.write(f"**Context:** {decision.context}")
                    st.write(f"**Decision:** {decision.decision}")
    
    # Save design
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Design", key="save_design"):
            st.session_state.current_design = design
            st.success("✅ Design saved to session")
    
    with col2:
        if st.button("📥 Export Design", key="export_design"):
            design_json = design.model_dump_json(indent=2)
            st.download_button(
                label="Download JSON",
                data=design_json,
                file_name=f"{design.id}.json",
                mime="application/json"
            )
    
    with col3:
        if st.button("➡️ Go to Validate", key="goto_validate"):
            st.switch_page("pages/2_Validate.py")


# ============================================================================
# VALIDATE PHASE
# ============================================================================

elif "✅ Validate" in page:
    st.title("✅ Validate - Policy Compliance")
    st.markdown("Check architecture against compliance frameworks and policies")
    
    if not st.session_state.current_design:
        st.warning("⚠️ No design selected.")
        st.stop()
    
    design = st.session_state.current_design
    
    # Run validation
    if st.button("🔍 Run Validation", key="run_validation"):
        with st.spinner("Validating architecture against policies..."):
            validations, compliance_score = st.session_state.validator.validate_architecture(design)
            st.session_state.validations = validations
            st.success("✅ Validation complete!")
    
    # Display results
    if st.session_state.validations:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Compliance Score", f"{design.compliance_score:.1f}%", delta="Validated")
        
        with col2:
            passed = sum(1 for v in st.session_state.validations if v.status.value == "Pass")
            st.metric("Policies Passed", f"{passed}/{len(st.session_state.validations)}")
        
        with col3:
            failed = sum(1 for v in st.session_state.validations if v.status.value == "Fail")
            st.metric("Critical Issues", failed, delta="-" if failed == 0 else f"-{failed}" )
        
        st.markdown("---")
        
        # Framework breakdown
        st.subheader("📋 Compliance Frameworks")
        
        framework_tabs = st.tabs([f.value for f in design.compliance_frameworks] + ["All Policies"])
        
        for idx, framework in enumerate(design.compliance_frameworks):
            with framework_tabs[idx]:
                assessment = ComplianceAssessment(st.session_state.validator)
                result = assessment.assess_framework_compliance(design, framework)
                
                st.metric(f"{framework.value} Compliance", 
                         f"{result['summary']['compliance_percentage']:.0f}%")
                
                st.markdown("### Policy Results")
                for policy in result['policies']:
                    color = "🟢" if policy['status'] == "Pass" else "🔴" if policy['status'] == "Fail" else "🟡"
                    st.write(f"{color} **{policy['name']}** - {policy['status']}")
                    st.caption(policy['message'])
                    if policy['remediation']:
                        st.warning(f"**Fix:** {policy['remediation']}")
        
        with framework_tabs[-1]:
            st.markdown("### All Policies")
            for validation in st.session_state.validations:
                color = "🟢" if validation.status.value == "Pass" else "🔴" if validation.status.value == "Fail" else "🟡"
                with st.expander(f"{color} {validation.policy_name} ({validation.severity.value})"):
                    st.write(f"**ID:** {validation.policy_id}")
                    st.write(f"**Status:** {validation.status.value}")
                    st.write(f"**Message:** {validation.message}")
                    if validation.remediation_steps:
                        st.info("**Remediation Steps:**\n\n" + 
                               "\n".join([f"- {step}" for step in validation.remediation_steps]))


# ============================================================================
# GOVERN PHASE
# ============================================================================

elif "🛡️ Govern" in page:
    st.title("🛡️ Govern - Architecture Control Plane")
    st.markdown("Configure governance policies and enterprise controls")
    
    if not st.session_state.current_design:
        st.warning("⚠️ No design selected.")
        st.stop()
    
    design = st.session_state.current_design
    
    tabs = st.tabs(["Policies", "Control Plane", "Approvals"])
    
    with tabs[0]:
        st.subheader("Active Policies")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            security_policies = sum(1 for p in st.session_state.validator.policies if "SEC" in p.id)
            st.metric("Security Policies", security_policies)
        
        with col2:
            compliance_policies = sum(1 for p in st.session_state.validator.policies if "COMP" in p.id)
            st.metric("Compliance Policies", compliance_policies)
        
        with col3:
            governance_policies = sum(1 for p in st.session_state.validator.policies if "ARCH" in p.id)
            st.metric("Governance Policies", governance_policies)
        
        st.markdown("### Policy Catalog")
        
        policy_categories = {
            "Security": [p for p in st.session_state.validator.policies if "SEC" in p.id],
            "Compliance": [p for p in st.session_state.validator.policies if "COMP" in p.id],
            "Reliability": [p for p in st.session_state.validator.policies if "REL" in p.id],
            "Technology": [p for p in st.session_state.validator.policies if "TECH" in p.id],
            "Cost": [p for p in st.session_state.validator.policies if "COST" in p.id],
            "Architecture": [p for p in st.session_state.validator.policies if "ARCH" in p.id],
        }
        
        for category, policies in policy_categories.items():
            if policies:
                with st.expander(f"📌 {category} ({len(policies)})"):
                    for policy in policies:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{policy.name}** ({policy.id})")
                            st.caption(policy.description)
                        with col2:
                            severity_colors = {
                                "Critical": "🔴",
                                "High": "🟠",
                                "Medium": "🟡",
                                "Low": "🟢"
                            }
                            st.write(severity_colors.get(policy.severity.value, "⚪"))
    
    with tabs[1]:
        st.subheader("Enterprise Architecture Control Plane")
        
        st.markdown("""
        The control plane enforces architecture governance across the organization.
        
        **Components:**
        """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Architecture Models")
            st.write("Enterprise capabilities and landscape")
        
        with col2:
            st.markdown("### Standards")
            st.write("Approved technologies and patterns")
        
        with col3:
            st.markdown("### Policies")
            st.write("Security, compliance, cost controls")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Architecture Agents")
            st.write("Review and validation automation")
        
        with col2:
            st.markdown("### IaC & GitOps")
            st.write("Terraform/Helm + GitHub Actions")
        
        with col3:
            st.markdown("### Observability")
            st.write("Runtime monitoring & alerting")
    
    with tabs[2]:
        st.subheader("Design Approvals")
        
        col1, col2 = st.columns(2)
        
        with col1:
            design.approvers = st.multiselect(
                "Approvers",
                options=["CTO", "CISO", "Chief Architect", "Compliance Officer"],
                default=design.approvers or ["Chief Architect"]
            )
        
        with col2:
            design.reviewers = st.multiselect(
                "Reviewers",
                options=["Security Team", "Platform Team", "Database Team", "Finance"],
                default=design.reviewers or ["Security Team"]
            )
        
        st.markdown("### Approval Status")
        
        for approver in design.approvers:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{approver}**")
            with col2:
                status = st.selectbox("Status", ["⏳ Pending", "✅ Approved", "❌ Rejected"], key=approver)


# ============================================================================
# GENERATE PHASE
# ============================================================================

elif "⚙️ Generate" in page:
    st.title("⚙️ Generate - Code & Documentation")
    st.markdown("Generate IaC, ADRs, and documentation from architecture")
    
    if not st.session_state.current_design:
        st.warning("⚠️ No design selected.")
        st.stop()
    
    design = st.session_state.current_design
    
    st.subheader("Artifact Generation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        generate_adr = st.checkbox("📋 ADRs", value=True)
    with col2:
        generate_terraform = st.checkbox("🌍 Terraform", value=True)
    with col3:
        generate_docs = st.checkbox("📚 Documentation", value=True)
    
    if st.button("🚀 Generate All Artifacts", key="generate_artifacts"):
        with st.spinner("Generating artifacts..."):
            artifacts = st.session_state.generator.generate_all_artifacts(design)
            st.session_state.artifacts = artifacts
            st.success(f"✅ Generated {len(artifacts)} artifacts!")
    
    if st.session_state.artifacts:
        st.markdown("---")
        st.subheader("Generated Artifacts")
        
        for artifact in st.session_state.artifacts:
            with st.expander(f"📄 {artifact.name} ({artifact.type})"):
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.code(artifact.content, language=artifact.language)
                
                with col2:
                    st.download_button(
                        label="⬇️ Download",
                        data=artifact.content,
                        file_name=artifact.name,
                        mime="text/plain"
                    )
        
        # Download all as ZIP
        st.markdown("---")
        if st.button("📦 Download All as ZIP", key="download_zip"):
            st.info("ZIP export functionality coming soon")


# ============================================================================
# DEPLOY PHASE
# ============================================================================

elif "🚀 Deploy" in page:
    st.title("🚀 Deploy - Release Management")
    st.markdown("Deploy infrastructure and track deployment status")
    
    if not st.session_state.current_design:
        st.warning("⚠️ No design selected.")
        st.stop()
    
    design = st.session_state.current_design
    
    st.subheader("Deployment Pipeline")
    
    # Deployment phases
    phases = ["Plan", "Validate", "Review", "Approve", "Apply", "Monitor"]
    
    col = st.columns(len(phases))
    for idx, phase in enumerate(phases):
        with col[idx]:
            status = "✅" if idx < 3 else "⏳" if idx == 3 else "⏹️"
            st.metric(f"{status} {phase}", "Complete" if idx < 3 else "Pending")
    
    st.markdown("---")
    
    st.subheader("CI/CD Pipeline Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Repository Configuration**")
        repo_type = st.selectbox("Repository Type", ["GitHub", "GitLab", "Azure DevOps"])
        repo_name = st.text_input("Repository Name", value=f"arch-{design.id.lower()}")
        branch = st.text_input("Deployment Branch", value="main")
    
    with col2:
        st.write("**Deployment Configuration**")
        provider = st.selectbox("Cloud Provider", ["AWS", "Azure", "GCP"])
        region = st.text_input("Primary Region", value="us-east-1")
        environment = st.selectbox("Environment", ["Dev", "Staging", "Production"])
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 View Deployment Plan", key="view_plan"):
            st.info("Terraform plan output will display here")
    
    with col2:
        if st.button("▶️ Apply Deployment", key="apply_deploy"):
            st.success("✅ Deployment initiated! Check CI/CD pipeline for status.")
    
    with col3:
        if st.button("⏸️ Cancel Deployment", key="cancel_deploy"):
            st.warning("Deployment cancellation initiated")


# ============================================================================
# OBSERVE PHASE
# ============================================================================

elif "👁️ Observe" in page:
    st.title("👁️ Observe - Runtime Monitoring")
    st.markdown("Monitor architecture drift and system health")
    
    if not st.session_state.current_design:
        st.warning("⚠️ No design selected.")
        st.stop()
    
    design = st.session_state.current_design
    
    tabs = st.tabs(["Drift Detection", "Metrics", "Logs"])
    
    with tabs[0]:
        st.subheader("Architecture Drift Detection")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Drifts", 3, delta="-1")
        with col2:
            st.metric("Critical Issues", 1, delta=None)
        with col3:
            st.metric("Last Sync", "2 minutes ago")
        
        st.markdown("### Detected Drifts")
        
        drifts = [
            {"component": "RDS Database", "expected": "Encrypted", "actual": "Not Encrypted", "severity": "🔴 Critical"},
            {"component": "Security Group", "expected": "Restricted", "actual": "Wide Open", "severity": "🟠 High"},
            {"component": "Backup Schedule", "expected": "Daily", "actual": "Weekly", "severity": "🟡 Medium"},
        ]
        
        for drift in drifts:
            with st.expander(f"{drift['severity']} - {drift['component']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Expected:** {drift['expected']}")
                with col2:
                    st.write(f"**Actual:** {drift['actual']}")
                
                if st.button("Fix Drift", key=f"fix_{drift['component']}"):
                    st.success("✅ Remediation initiated")
    
    with tabs[1]:
        st.subheader("System Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Availability", "99.95%", delta="+0.05%")
        with col2:
            st.metric("Response Time", "145ms", delta="-15ms")
        with col3:
            st.metric("Error Rate", "0.02%", delta="-0.01%")
        
        st.info("Metric visualizations coming soon")
    
    with tabs[2]:
        st.subheader("System Logs")
        st.info("Log streaming coming soon")


# ============================================================================
# RECONCILE PHASE
# ============================================================================

elif "🔄 Reconcile" in page:
    st.title("🔄 Reconcile - Continuous Improvement")
    st.markdown("Drive continuous improvement through feedback loops")
    
    if not st.session_state.current_design:
        st.warning("⚠️ No design selected.")
        st.stop()
    
    design = st.session_state.current_design
    
    tabs = st.tabs(["Feedback", "Improvements", "Lessons Learned"])
    
    with tabs[0]:
        st.subheader("Feedback Collection")
        
        feedback_source = st.selectbox(
            "Feedback Source",
            ["Operations Team", "Security Team", "Development Team", "Users", "Compliance", "Finance"]
        )
        
        feedback_category = st.selectbox(
            "Category",
            ["Performance", "Reliability", "Security", "Cost", "Usability", "Compliance"]
        )
        
        feedback_text = st.text_area("Feedback", placeholder="Enter feedback here...")
        
        priority = st.select_slider("Priority", options=["Low", "Medium", "High", "Critical"])
        
        if st.button("📤 Submit Feedback"):
            st.success("✅ Feedback recorded")
    
    with tabs[1]:
        st.subheader("Improvement Opportunities")
        
        improvements = [
            {"title": "Add caching layer", "impact": "High", "effort": "Medium", "estimated_savings": "$50K/year"},
            {"title": "Optimize database queries", "impact": "High", "effort": "High", "estimated_savings": "$75K/year"},
            {"title": "Implement auto-scaling", "impact": "Medium", "effort": "Medium", "estimated_savings": "$30K/year"},
        ]
        
        for imp in improvements:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(imp["title"])
            with col2:
                st.write(f"Impact: {imp['impact']}")
            with col3:
                st.write(f"Effort: {imp['effort']}")
            with col4:
                st.write(imp["estimated_savings"])
    
    with tabs[2]:
        st.subheader("Lessons Learned")
        
        lesson = st.text_area("Document lesson learned:", placeholder="What did we learn from this architecture?")
        
        if st.button("💾 Save Lesson"):
            st.success("✅ Lesson documented")


st.markdown("---")
st.markdown("*ArchiCode Generator • People + Policy + Automation + AI + Real Business Outcomes*")
