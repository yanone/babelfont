"""Generate AI-friendly documentation for Babelfont classes.

This module provides utilities to generate concise, natural language documentation
suitable for inclusion in AI/LLM prompts.
"""

import dataclasses
import typing
from io import StringIO

from .BaseObject import I18NDictionary


def _type_to_string(t) -> str:
    """Convert a type annotation to a human-readable string."""
    # Handle string type annotations
    if isinstance(t, str):
        return t

    # Handle ForwardRef objects
    if hasattr(t, "__forward_arg__"):
        return t.__forward_arg__

    # Handle None type
    if t is type(None):
        return "None"

    # Handle generic types
    if isinstance(t, typing._GenericAlias):
        origin = typing.get_origin(t)
        args = typing.get_args(t)

        if origin is typing.Union:
            # Optional is Union[X, None]
            if len(args) == 2 and type(None) in args:
                inner = args[0] if args[1] is type(None) else args[1]
                return f"Optional[{_type_to_string(inner)}]"
            else:
                return f"Union[{', '.join(_type_to_string(a) for a in args)}]"
        elif origin is list:
            if args:
                return f"list of {_type_to_string(args[0])}"
            return "list"
        elif origin is dict:
            if len(args) == 2:
                return f"dict mapping {_type_to_string(args[0])} to {_type_to_string(args[1])}"
            return "dict"
        elif origin is tuple:
            if args:
                return f"tuple of ({', '.join(_type_to_string(a) for a in args)})"
            return "tuple"

    # Handle list/tuple as literal types
    if isinstance(t, list):
        return f"list of {', '.join(_type_to_string(item) for item in t)}"
    if isinstance(t, tuple):
        return f"tuple of ({', '.join(_type_to_string(item) for item in t)})"

    # Handle classes with __name__
    if hasattr(t, "__name__"):
        return t.__name__

    return str(t)


def generate_class_docs(cls, include_private: bool = False) -> str:
    """Generate AI-friendly documentation for a dataclass.

    Args:
        cls: The dataclass to document
        include_private: If True, include fields starting with underscore

    Returns:
        A formatted documentation string suitable for LLM prompts
    """
    if not dataclasses.is_dataclass(cls):
        return f"{cls.__name__}: Not a dataclass"

    out = StringIO()

    # Class name and description
    out.write(f"# {cls.__name__}\n\n")
    if cls.__doc__:
        out.write(f"{cls.__doc__.strip()}\n\n")

    # Fields
    out.write("## Fields:\n\n")

    for field in dataclasses.fields(cls):
        # Skip private fields unless requested
        if not include_private and field.name.startswith("_"):
            continue

        # Field name and type
        type_str = _type_to_string(field.type)
        out.write(f"- **{field.name}** ({type_str})")

        # Required vs optional
        if (
            field.default is dataclasses.MISSING
            and field.default_factory is dataclasses.MISSING
        ):
            out.write(" - REQUIRED")
        elif field.default is not dataclasses.MISSING:
            out.write(f" - defaults to `{field.default}`")
        else:
            out.write(" - optional")

        # Localizable
        if field.type == I18NDictionary:
            out.write(" (localizable)")

        out.write("\n")

        # Description from metadata
        if "description" in field.metadata:
            desc = field.metadata["description"].strip()
            # Clean up multi-line descriptions
            desc = " ".join(desc.split())
            out.write(f"  {desc}\n")

        out.write("\n")

    return out.getvalue()


def generate_all_docs(classes: list = None, include_private: bool = False) -> str:
    """Generate documentation for multiple classes.

    Args:
        classes: List of classes to document. If None, documents all main Babelfont classes
        include_private: If True, include private fields

    Returns:
        Combined documentation string
    """
    if classes is None:
        # Import here to avoid circular imports
        from . import (
            Font,
            Axis,
            Instance,
            Master,
            Names,
            Features,
            Glyph,
            Layer,
            Guide,
            Shape,
            Anchor,
        )

        classes = [
            Font,
            Axis,
            Instance,
            Master,
            Names,
            Features,
            Glyph,
            Layer,
            Guide,
            Shape,
            Anchor,
        ]

    out = StringIO()
    out.write("# Babelfont Format Documentation\n\n")
    out.write(
        "Babelfont is a JSON-based font format for working with single master and variable fonts.\n\n"
    )

    for cls in classes:
        out.write(generate_class_docs(cls, include_private=include_private))
        out.write("\n---\n\n")

    return out.getvalue()


def generate_minimal_docs() -> str:
    """Generate a minimal documentation string focused on the most commonly used classes.

    Returns:
        A concise documentation string suitable for AI prompts
    """
    from . import Font, Glyph, Layer, Master

    out = StringIO()
    out.write("# Babelfont Quick Reference\n\n")
    out.write("Babelfont is a font manipulation library. Key concepts:\n\n")
    out.write(
        "- **Font**: Top-level object representing a font family with one or more masters\n"
    )
    out.write("- **Master**: A single master/style in a font (e.g., Regular, Bold)\n")
    out.write("- **Glyph**: A glyph in the font (character/shape)\n")
    out.write(
        "- **Layer**: The actual outline data for a glyph in a specific master\n\n"
    )

    for cls in [Font, Master, Glyph, Layer]:
        out.write(generate_class_docs(cls, include_private=False))
        out.write("\n")

    return out.getvalue()


if __name__ == "__main__":
    # Example usage
    print(generate_minimal_docs())
