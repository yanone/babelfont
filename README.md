# Context: Load, examine and save fonts in Context format

*This describes Context >3.0, which is a complete rewrite from the previous version.*

Context is a utility for loading and examining fonts in the Context format.

The Context format is a JSON-based font format that provides a simple and
consistent way to work with font data. It supports single master and variable fonts.

The object hierarchy can be seen [here](docs/Font.md).

For example:

```python
from context import load

font = load("Myfont.context")
default_a = font.default_master.get_glyph_layer("A")
top_anchor = default_a.anchors_dict["top"]
print("Top anchor = (%i,%i)" % (top_anchor.x, top_anchor.y))
print("LSB, RSB = (%i,%i)" % (default_a.lsb, default_a.rsb))
font.save("Myfont-modified.context")
```

## AI-Friendly Documentation

Context includes an AI documentation generator for creating concise, natural language
documentation suitable for LLM/AI prompts:

```python
from context import generate_minimal_docs, generate_class_docs, generate_all_docs

# Generate minimal documentation for common use cases
minimal_docs = generate_minimal_docs()

# Generate documentation for a specific class
from context import Font
font_docs = generate_class_docs(Font)

# Generate full documentation for all classes
all_docs = generate_all_docs()
```

This is useful when you need to provide context about Context's structure to an AI assistant.

