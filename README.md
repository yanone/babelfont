# Babelfont: Load, examine and save fonts in Babelfont format

*This describes Babelfont >3.0, which is a complete rewrite from the previous version.*

Babelfont is a utility for loading and examining fonts in the Babelfont format.

The Babelfont format is a JSON-based font format that provides a simple and
consistent way to work with font data. It supports single master and variable fonts.

The object hierarchy can be seen [here](docs/Font.md).

For example:

```python
from babelfont import load

font = load("Myfont.babelfont")
default_a = font.default_master.get_glyph_layer("A")
top_anchor = default_a.anchors_dict["top"]
print("Top anchor = (%i,%i)" % (top_anchor.x, top_anchor.y))
print("LSB, RSB = (%i,%i)" % (default_a.lsb, default_a.rsb))
font.save("Myfont-modified.babelfont")
```

## AI-Friendly Documentation

Babelfont includes an AI documentation generator for creating concise, natural language
documentation suitable for LLM/AI prompts:

```python
from babelfont import generate_minimal_docs, generate_class_docs, generate_all_docs

# Generate minimal documentation for common use cases
minimal_docs = generate_minimal_docs()

# Generate documentation for a specific class
from babelfont import Font
font_docs = generate_class_docs(Font)

# Generate full documentation for all classes
all_docs = generate_all_docs()
```

This is useful when you need to provide context about Babelfont's structure to an AI assistant.

