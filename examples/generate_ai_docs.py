#!/usr/bin/env python3
"""Example: Generate AI-friendly documentation for Babelfont.

This script demonstrates how to generate documentation suitable for
including in LLM/AI prompts.
"""

import sys
import os

# Add parent src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from babelfont.ai_docs import (
    generate_minimal_docs,
    generate_class_docs,
    generate_all_docs,
)
from babelfont import Font, Glyph


def example_minimal():
    """Generate minimal documentation for common use cases."""
    print("=== MINIMAL DOCUMENTATION ===")
    print(generate_minimal_docs())
    print()


def example_single_class():
    """Generate documentation for a single class."""
    print("=== SINGLE CLASS DOCUMENTATION (Font) ===")
    print(generate_class_docs(Font))
    print()


def example_all_docs():
    """Generate full documentation for all classes."""
    print("=== FULL DOCUMENTATION ===")
    docs = generate_all_docs()
    # Just show first 2000 characters as example
    print(docs[:2000])
    print(f"\n... (total length: {len(docs)} characters)")
    print()


def example_custom_classes():
    """Generate documentation for specific classes."""
    print("=== CUSTOM CLASS SELECTION ===")
    print(generate_all_docs(classes=[Font, Glyph]))
    print()


if __name__ == "__main__":
    # Generate minimal docs (most useful for AI prompts)
    example_minimal()

    # Uncomment to see other examples:
    # example_single_class()
    # example_all_docs()
    # example_custom_classes()
