"""
Test module for Architecture-as-Code Generator

Contains test data, fixtures, and example scenarios for development and demonstration.
"""

from .test_data import (
    create_loan_origination_architecture,
    create_payment_processing_architecture,
    create_data_mesh_architecture,
    get_all_test_architectures,
)

__all__ = [
    "create_loan_origination_architecture",
    "create_payment_processing_architecture",
    "create_data_mesh_architecture",
    "get_all_test_architectures",
]
