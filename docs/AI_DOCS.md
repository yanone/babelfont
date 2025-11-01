# AI Documentation Generator

The `context.ai_docs` module provides utilities for generating AI-friendly documentation
that can be embedded in LLM/AI assistant prompts.

## Why?

When working with AI coding assistants, providing concise, natural-language documentation
about Context's structure helps the AI understand how to work with the library. This
module generates documentation that:

- Uses natural language descriptions from docstrings
- Expresses types in human-readable format (e.g., "list of Glyph" instead of "List[Glyph]")
- Indicates required vs optional fields clearly
- Is compact enough to fit in AI context windows

## Usage

### Minimal Documentation (Recommended for AI Prompts)

```python
from context import generate_minimal_docs

# Generate a quick reference focused on the most commonly used classes
docs = generate_minimal_docs()
print(docs)
```

This generates documentation for Font, Master, Glyph, and Layer - the core classes
you'll use most often.

### Single Class Documentation

```python
from context import generate_class_docs, Font

# Generate documentation for a specific class
font_docs = generate_class_docs(Font, include_private=False)
print(font_docs)
```

### Full Documentation

```python
from context import generate_all_docs

# Generate documentation for all Context classes
all_docs = generate_all_docs(include_private=False)
print(all_docs)
```

### Custom Class Selection

```python
from context import generate_all_docs, Font, Glyph, Layer

# Generate documentation for specific classes
custom_docs = generate_all_docs(classes=[Font, Glyph, Layer])
print(custom_docs)
```

## Example Output

Here's what the minimal documentation looks like:

```
# Context Quick Reference

Context is a font manipulation library. Key concepts:

- **Font**: Top-level object representing a font family with one or more masters
- **Master**: A single master/style in a font (e.g., Regular, Bold)
- **Glyph**: A glyph in the font (character/shape)
- **Layer**: The actual outline data for a glyph in a specific master

# Font

Represents a font, with one or more masters.

## Fields:

- **upm** (int) - defaults to `1000`
  The font's units per em.

- **version** (tuple of (int, int)) - defaults to `(1, 0)`
  Font version number as a tuple of integers (major, minor).

- **axes** (list of Axis) - optional
  A list of axes, in the case of variable/multiple master font. May be empty.

...
```

## Integration with AI Assistants

To use this with an AI assistant, include the documentation in your prompt:

```python
from context import generate_minimal_docs

docs = generate_minimal_docs()

prompt = f"""
I'm working with the Context library. Here's the documentation:

{docs}

Now help me write code to...
"""
```

## API Reference

### `generate_minimal_docs() -> str`

Generates concise documentation for the most commonly used classes (Font, Master, Glyph, Layer).

**Returns:** Documentation string suitable for AI prompts

### `generate_class_docs(cls, include_private=False) -> str`

Generates documentation for a single dataclass.

**Args:**
- `cls`: The dataclass to document
- `include_private`: If True, include fields starting with underscore

**Returns:** Formatted documentation string

### `generate_all_docs(classes=None, include_private=False) -> str`

Generates documentation for multiple classes.

**Args:**
- `classes`: List of classes to document. If None, documents all main Context classes
- `include_private`: If True, include private fields

**Returns:** Combined documentation string
