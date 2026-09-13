"""
Setup configuration for Architecture-as-Code Generator package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aac-generator",
    version="1.0.0",
    author="Architecture-as-Code Team",
    author_email="team@aac-generator.example.com",
    description="Architecture-as-Code generator for enterprise architecture governance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/aac-generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.9",
    install_requires=[
        "streamlit>=1.28.0",
        "pydantic>=2.5.0",
        "pydantic-yaml>=1.2.0",
        "jsonschema>=4.20.0",
        "anthropic>=0.21.0",
        "openai>=1.6.0",
        "pandas>=2.1.0",
        "PyYAML>=6.0.0",
        "jinja2>=3.1.0",
        "plotly>=5.18.0",
        "python-dateutil>=2.8.0",
        "requests>=2.31.0",
        "click>=8.1.0",
        "loguru>=0.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.12.0",
            "pylint>=3.0.0",
            "sphinx>=7.2.0",
        ],
        "aws": [
            "boto3>=1.28.0",
            "botocore>=1.31.0",
        ],
        "kubernetes": [
            "kubernetes>=28.1.0",
        ],
        "database": [
            "sqlalchemy>=2.0.0",
            "psycopg2-binary>=2.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "aac=core.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/aac-generator/issues",
        "Documentation": "https://aac-generator.example.com/docs",
        "Source Code": "https://github.com/yourusername/aac-generator",
    },
)
