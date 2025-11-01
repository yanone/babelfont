import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Tuple

from .BaseObject import BaseObject

if TYPE_CHECKING:
    from context.Font import Font

PREFIX_MARKER = "# Prefix: "
PREFIX_RE = re.compile(r"# Prefix: (.*)")


@dataclass
class Features(BaseObject):
    """A representation of the OpenType feature code."""

    classes: Dict[str, List[str]] = field(
        default_factory=dict,
        metadata={
            "separate_items": True,
            "description": "A dictionary of classes. Each group is a list of glyph names or class names. The key should not start with @.",
        },
    )
    prefixes: Dict[str, str] = field(
        default_factory=dict,
        metadata={
            "separate_items": True,
            "description": "A dictionary of OpenType lookups and other feature code to be placed before features are defined. The keys are user-defined names, the values are AFDKO feature code.",
        },
    )
    features: List[Tuple[str, str]] = field(
        default_factory=list,
        metadata={
            "separate_items": True,
            "description": "A list of OpenType feature code, expressed as a tuple (feature tag, code).",
        },
    )

    @classmethod
    def from_fea(cls, fea: str, glyphNames=()) -> "Features":
        """Load features from a .fea file."""
        features = Features()
        currentPrefix = "anonymous"

        lines = fea.split("\n")
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            # Handle glyph class definitions
            if line.startswith("@") and "=" in line:
                match = re.match(r"@(\w+)\s*=\s*\[(.*?)\];?", line)
                if match:
                    class_name = match.group(1)
                    class_content = match.group(2).strip()
                    features.classes[class_name] = class_content.split()
                i += 1
                continue

            # Handle prefix markers
            if line.startswith("# Prefix:"):
                match = re.match(PREFIX_RE, line)
                if match:
                    currentPrefix = match.group(1)
                i += 1
                continue

            # Handle feature blocks
            if line.startswith("feature "):
                match = re.match(r"feature\s+(\w+)\s*\{", line)
                if match:
                    feature_name = match.group(1)
                    feature_code = ""
                    i += 1

                    # Collect lines until we find the closing brace
                    brace_count = 1
                    while i < len(lines) and brace_count > 0:
                        curr_line = lines[i]
                        brace_count += curr_line.count("{") - curr_line.count("}")

                        if brace_count > 0:
                            feature_code += curr_line + "\n"
                        i += 1

                    features.features.append((feature_name, feature_code.rstrip()))
                    continue

            # Everything else goes into prefixes
            if line:  # Skip empty lines
                if currentPrefix not in features.prefixes:
                    features.prefixes[currentPrefix] = ""
                features.prefixes[currentPrefix] += lines[i] + "\n"

            i += 1

        # Clean up trailing newlines in prefixes
        for prefix in features.prefixes:
            features.prefixes[prefix] = features.prefixes[prefix].rstrip("\n")

        return features

    def to_fea(self) -> str:
        """Dump features to a .fea file."""
        fea = ""
        for name, glyphs in self.classes.items():
            fea += f"@{name} = [{' '.join(glyphs)}];\n"
        for prefix, code in self.prefixes.items():
            if prefix != "anonymous":
                fea += f"# Prefix: {prefix}\n"
            fea += code + "\n"
        for name, code in self.features:
            fea += f"feature {name} {{\n{code}\n}} {name};\n"
        return fea

    def as_ast(self, font: "Font") -> Dict[str, Any]:
        from io import StringIO
        from fontTools.feaLib import ast
        from fontTools.feaLib.parser import Parser, SymbolTable

        rv = {
            "prefixes": {},
            "features": [],
        }
        glyphnames = font.glyphs.keys()
        lookups = SymbolTable()
        glyphclasses = SymbolTable()
        for name, glyphs in self.classes.items():
            glyphcls = ast.GlyphClass(glyphs=[ast.GlyphName(g) for g in glyphs])
            glyphclass = ast.GlyphClassDefinition(name, glyphcls)
            glyphclasses.define(name, glyphclass)

        for prefix, code in self.prefixes.items():
            parser = Parser(StringIO(code), followIncludes=False, glyphNames=glyphnames)
            parser.lookups_ = lookups
            parser.glyphclasses_ = glyphclasses
            try:
                file = parser.parse()
            except Exception as e:
                raise ValueError(f"Error parsing feature code: {e}\n\nCode was: {code}")
            rv["prefixes"][prefix] = file

        for name, code in self.features:
            if name is not None and not code.startswith("feature " + name):
                code = f"feature {name} {{\n{code}\n}} {name};"
            parser = Parser(StringIO(code), followIncludes=False, glyphNames=glyphnames)
            parser.lookups_ = lookups
            parser.glyphclasses_ = glyphclasses
            try:
                file = parser.parse()
            except Exception as e:
                raise ValueError(f"Error parsing feature code: {e}\n\nCode was: {code}")
            rv["features"].append((name, file))

        return rv
