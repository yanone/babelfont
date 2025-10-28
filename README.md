# Babelfont: Load, examine and save fonts in Babelfont format

*This describes Babelfont >3.0, which is a complete rewrite from the previous version.*

Babelfont is a utility for loading and examining fonts in the Babelfont format.

The Babelfont format is a JSON-based font format that provides a simple and
consistent way to work with font data. It supports single master and variable fonts.

The object hierarchy can be seen [here](https://simoncozens.github.io/babelfont).

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

## Documentation

For detailed documentation of the Babelfont Python API, see [Font.md](docs/Font.md).
