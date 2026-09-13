#!/usr/bin/env python3
"""
Architecture-as-Code Generator - Local Demo Script

Run this to see the complete workflow with synthetic test data.
No Docker required - runs on your laptop!

Usage:
    python demo.py
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from tests.test_data import get_all_test_architectures
from core.validators import PolicyValidator, ComplianceAssessment
from core.generators import GeneratorOrchestrator
from core.models import ComplianceFramework


def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")


def print_section(text):
    """Print formatted section"""
    print(f"\n{text}")
    print(f"{'-'*len(text)}\n")


def demo_validation(architect):
    """Demonstrate policy validation"""
    print_section(f"2. VALIDATE - Checking {architect.name} against policies")
    
    validator = PolicyValidator()
    validations, compliance_score = validator.validate_architecture(architect)
    
    print(f"✅ Validation Complete!")
    print(f"   Compliance Score: {compliance_score:.1f}%")
    print(f"   Total Policies: {len(validations)}")
    
    passed = sum(1 for v in validations if v.status.value == "Pass")
    failed = sum(1 for v in validations if v.status.value == "Fail")
    warned = sum(1 for v in validations if v.status.value == "Warn")
    
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   ⚠️  Warned: {warned}")
    
    # Show details of failures and warnings
    if failed > 0 or warned > 0:
        print(f"\n📋 Policy Details:")
        for v in validations:
            if v.status.value in ["Fail", "Warn"]:
                status_icon = "❌" if v.status.value == "Fail" else "⚠️"
                print(f"   {status_icon} {v.policy_name}")
                print(f"      Message: {v.message}")
                if v.remediation_steps:
                    for step in v.remediation_steps:
                        print(f"      → {step}")
    
    return validations, compliance_score


def demo_compliance_frameworks(architect, validator):
    """Demonstrate compliance framework assessment"""
    print_section("3. GOVERN - Framework-Specific Compliance")
    
    assessment = ComplianceAssessment(validator)
    
    for framework in architect.compliance_frameworks:
        result = assessment.assess_framework_compliance(architect, framework)
        
        compliance_pct = result['summary']['compliance_percentage']
        passed = result['summary']['passed']
        failed = result['summary']['failed']
        warned = result['summary']['warned']
        
        status_icon = "✅" if compliance_pct >= 90 else "⚠️" if compliance_pct >= 70 else "❌"
        
        print(f"{status_icon} {framework.value}: {compliance_pct:.0f}%")
        print(f"   Passed: {passed}, Failed: {failed}, Warned: {warned}")


def demo_code_generation(architect):
    """Demonstrate code generation"""
    print_section("4. GENERATE - Creating Artifacts")
    
    generator = GeneratorOrchestrator()
    artifacts = generator.generate_all_artifacts(architect)
    
    print(f"✅ Generated {len(artifacts)} artifacts:\n")
    
    for artifact in artifacts:
        lines = len(artifact.content.split('\n'))
        print(f"   📄 {artifact.name}")
        print(f"      Type: {artifact.type}")
        print(f"      Format: {artifact.language}")
        print(f"      Lines: {lines}")
        
        # Show first few lines of ADRs
        if artifact.type == "ADR":
            first_lines = artifact.content.split('\n')[:3]
            for line in first_lines:
                if line.strip():
                    print(f"      → {line[:60]}")
    
    return artifacts


def demo_architecture_summary(architect):
    """Print architecture summary"""
    print_section("1. MODEL - Architecture Overview")
    
    print(f"📋 {architect.name}")
    print(f"   ID: {architect.id}")
    print(f"   Status: {architect.status.value}")
    print(f"   Architect: {architect.architect}")
    print(f"   Driver: {architect.business_driver}")
    
    print(f"\n📊 Non-Functional Requirements:")
    print(f"   Availability: {architect.availability_target}%")
    print(f"   RTO: {architect.rto_minutes} minutes")
    print(f"   RPO: {architect.rpo_minutes} minutes")
    print(f"   Max Latency: {architect.max_latency_ms}ms")
    print(f"   Est. Users: {architect.estimated_users:,}")
    
    print(f"\n🏢 Components:")
    print(f"   Business Capabilities: {len(architect.business_capabilities)}")
    for cap in architect.business_capabilities:
        print(f"      • {cap.name} ({cap.criticality})")
    
    print(f"\n   Applications: {len(architect.applications)}")
    for app in architect.applications:
        print(f"      • {app.name}")
        print(f"        - Technology: {', '.join(app.technology_stack)}")
        print(f"        - Cloud: {app.cloud_provider}")
        print(f"        - Containers: {'Yes' if app.containers else 'No'}")
    
    print(f"\n   Technology Standards: {len(architect.technologies)}")
    for tech in architect.technologies:
        print(f"      • {tech.technology_name} (v{', v'.join(tech.versions)})")
    
    print(f"\n⚖️  Compliance Frameworks:")
    for framework in architect.compliance_frameworks:
        print(f"      • {framework.value}")


def save_example_outputs(architect, artifacts, compliance_score):
    """Save example outputs to files for review"""
    output_dir = Path("demo_outputs")
    output_dir.mkdir(exist_ok=True)
    
    print_section("5. SAVE - Exporting Results")
    
    # Save architecture design as JSON
    design_file = output_dir / f"{architect.id}_design.json"
    with open(design_file, 'w') as f:
        json.dump(json.loads(architect.model_dump_json()), f, indent=2, default=str)
    print(f"✅ Saved architecture design: {design_file}")
    
    # Save artifacts
    for artifact in artifacts:
        artifact_file = output_dir / artifact.name
        with open(artifact_file, 'w') as f:
            f.write(artifact.content)
        print(f"✅ Saved artifact: {artifact_file}")
    
    # Save summary report
    summary_file = output_dir / f"{architect.id}_summary.md"
    with open(summary_file, 'w') as f:
        f.write(f"# {architect.name} - Architecture Summary\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n")
        f.write(f"## Status\n")
        f.write(f"- Status: {architect.status.value}\n")
        f.write(f"- Architect: {architect.architect}\n")
        f.write(f"- Compliance Score: {compliance_score:.1f}%\n\n")
        f.write(f"## Requirements\n")
        f.write(f"- Availability: {architect.availability_target}%\n")
        f.write(f"- RTO: {architect.rto_minutes} min\n")
        f.write(f"- RPO: {architect.rpo_minutes} min\n\n")
        f.write(f"## Artifacts Generated\n")
        for artifact in artifacts:
            f.write(f"- {artifact.name} ({artifact.type})\n")
    print(f"✅ Saved summary report: {summary_file}")
    
    print(f"\n📁 All outputs saved to: {output_dir.absolute()}")


def run_complete_demo():
    """Run complete Architecture-as-Code demonstration"""
    
    print_header("🏗️  Architecture-as-Code Generator - Local Demo")
    print("This demo shows the complete 7-phase workflow using synthetic BFSI data.\n")
    print("No Docker required - everything runs on your laptop!")
    
    # Get test architectures
    architectures = get_all_test_architectures()
    
    print(f"\n📚 {len(architectures)} example architectures available:\n")
    for idx, arch in enumerate(architectures, 1):
        print(f"{idx}. {arch.name}")
        print(f"   Status: {arch.status.value} | Applications: {len(arch.applications)}")
    
    # Run workflow for each architecture
    for architect in architectures:
        print_header(f"Processing: {architect.name}")
        
        # Phase 1: Model
        demo_architecture_summary(architect)
        
        # Phase 2: Validate
        validations, compliance_score = demo_validation(architect)
        
        # Phase 3: Govern
        demo_compliance_frameworks(architect, PolicyValidator())
        
        # Phase 4: Generate
        artifacts = demo_code_generation(architect)
        
        # Phase 5: Save outputs
        save_example_outputs(architect, artifacts, compliance_score)
    
    # Summary
    print_header("✅ Demo Complete!")
    print(f"Generated outputs are in the 'demo_outputs/' directory")
    print(f"Review the generated ADRs, Terraform configs, and documentation")
    print(f"\nNext steps:")
    print(f"1. Review the generated files in demo_outputs/")
    print(f"2. Read QUICKSTART.md for next steps")
    print(f"3. Run 'streamlit run ui/app.py' to use the interactive UI")
    print(f"4. Check BEST_PRACTICES.md for enterprise patterns")


def run_single_architecture_demo():
    """Run demo for a single architecture with detailed output"""
    
    print_header("🏗️  Architecture-as-Code Generator - Detailed Demo")
    
    # Use loan origination as main example
    architect = get_all_test_architectures()[0]
    
    print(f"Detailed demonstration of: {architect.name}\n")
    
    # Phase 1: Model
    print("\n" + "="*70)
    print("PHASE 1: MODEL - Define Architecture")
    print("="*70)
    demo_architecture_summary(architect)
    
    # Phase 2: Validate
    print("\n" + "="*70)
    print("PHASE 2: VALIDATE - Policy Compliance Checking")
    print("="*70)
    validations, compliance_score = demo_validation(architect)
    
    # Phase 3: Govern
    print("\n" + "="*70)
    print("PHASE 3: GOVERN - Framework Assessment")
    print("="*70)
    demo_compliance_frameworks(architect, PolicyValidator())
    
    # Phase 4: Generate
    print("\n" + "="*70)
    print("PHASE 4: GENERATE - Create Artifacts")
    print("="*70)
    artifacts = demo_code_generation(architect)
    
    # Show sample artifact content
    print("\n📄 Sample Generated Artifact (ADR):")
    print("-" * 70)
    adr = next((a for a in artifacts if a.type == "ADR"), None)
    if adr:
        lines = adr.content.split('\n')[:20]
        for line in lines:
            print(line)
        print("   ... (truncated for display)")
    
    # Save results
    print("\n" + "="*70)
    print("PHASE 5: SAVE - Export Results")
    print("="*70)
    save_example_outputs(architect, artifacts, compliance_score)
    
    # Summary
    print("\n" + "="*70)
    print("✅ DEMO COMPLETE - Next Steps")
    print("="*70)
    print(f"""
📁 Generated files are in: demo_outputs/
   • {architect.id}_design.json - Full architecture definition
   • {architect.id}_summary.md - Executive summary
   • Generated artifacts (ADRs, Terraform, etc.)

🚀 Try the interactive UI:
   $ streamlit run ui/app.py
   
📚 Learn more:
   • QUICKSTART.md - 5-minute guide
   • BEST_PRACTICES.md - Enterprise patterns
   • BUSINESS_PITCH.md - Business case

💡 What you're seeing:
   ✅ Model Phase - Defined business capabilities and apps
   ✅ Validate Phase - Ran 15+ compliance policies
   ✅ Govern Phase - Assessed 4 regulatory frameworks
   ✅ Generate Phase - Created 5+ production artifacts
   ✅ Save Phase - Exported for team review

🎯 This entire workflow took seconds - try 6 weeks of manual review!
""")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Architecture-as-Code Generator - Local Demo"
    )
    parser.add_argument(
        "--detailed",
        action="store_true",
        help="Run detailed single-architecture demo (default)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run demo for all test architectures"
    )
    
    args = parser.parse_args()
    
    if args.all:
        run_complete_demo()
    else:
        run_single_architecture_demo()
