"""
Configuration module for Architecture-as-Code Generator
"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Application Settings
APP_NAME = "Architecture-as-Code Generator"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
APP_ENV = os.getenv("APP_ENV", "development")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "text")  # text or json

# Database (SQLite for local, PostgreSQL for production)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///aac.db")
DATABASE_ECHO = DEBUG

# Directories
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
CONFIG_DIR = PROJECT_ROOT / "config"
DEMO_OUTPUT_DIR = PROJECT_ROOT / "demo_outputs"

# Create directories if they don't exist
for directory in [DATA_DIR, LOGS_DIR, CONFIG_DIR, DEMO_OUTPUT_DIR]:
    directory.mkdir(exist_ok=True)

# Compliance Frameworks
SUPPORTED_FRAMEWORKS = [
    "DORA",      # Digital Operational Resilience Act (EU)
    "MIFID_II",  # Markets in Financial Instruments Directive (EU)
    "GDPR",      # General Data Protection Regulation (Global)
    "SOX",       # Sarbanes-Oxley (US)
    "PCI_DSS",   # Payment Card Industry Data Security Standard (Global)
    "HIPAA",     # Health Insurance Portability and Accountability Act (US)
]

# Policy Configuration
NUM_POLICIES = 15  # Total number of built-in policies
POLICY_CATEGORIES = {
    "Security": 3,
    "Compliance": 3,
    "Reliability": 2,
    "Technology": 2,
    "Cost": 2,
    "Architecture": 3,
}

# Maturity Levels
MATURITY_LEVELS = {
    1: "DOCUMENTED",
    2: "VERSIONED",
    3: "STRUCTURED",
    4: "POLICY-DRIVEN",
    5: "AUTOMATED",
    6: "AGENTIC",
    7: "AUTONOMOUS",
}

# Cloud Providers
CLOUD_PROVIDERS = ["AWS", "Azure", "GCP", "On-Premises"]

# Technology Categories
TECH_CATEGORIES = [
    "Language",
    "Framework",
    "Database",
    "Cache",
    "Message Queue",
    "Container Orchestration",
    "Observability",
    "Security",
]

# Deployment Topologies
DEPLOYMENT_TOPOLOGIES = [
    "Monolith",
    "Microservices",
    "Serverless",
    "Event-Driven",
    "Batch Processing",
]

# Data Classifications
DATA_CLASSIFICATIONS = [
    "Public",
    "Internal",
    "Confidential",
    "Restricted",
]

# Criticality Levels
CRITICALITY_LEVELS = ["Critical", "High", "Medium", "Low"]

# Default SLA Values
DEFAULT_AVAILABILITY = 99.9
DEFAULT_RTO_MINUTES = 60
DEFAULT_RPO_MINUTES = 240
DEFAULT_MAX_LATENCY_MS = 500

if __name__ == "__main__":
    print("Architecture-as-Code Configuration")
    print(f"App Version: {APP_VERSION}")
    print(f"Environment: {APP_ENV}")
    print(f"Debug Mode: {DEBUG}")
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Supported Frameworks: {', '.join(SUPPORTED_FRAMEWORKS)}")
