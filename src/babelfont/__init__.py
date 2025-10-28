from babelfont.Anchor import Anchor
from babelfont.Axis import Axis
from babelfont.BaseObject import Color, I18NDictionary, Position
from babelfont.Features import Features
from babelfont.Font import Font
from babelfont.Glyph import Glyph
from babelfont.Guide import Guide
from babelfont.Instance import Instance
from babelfont.Layer import Layer
from babelfont.Master import Master
from babelfont.Names import Names
from babelfont.Node import Node
from babelfont.Shape import Shape, Transform
from babelfont.ai_docs import (
    generate_all_docs,
    generate_class_docs,
    generate_minimal_docs,
)

__all__ = [
    "Font",
    "Axis",
    "Glyph",
    "Master",
    "Instance",
    "Guide",
    "Anchor",
    "Layer",
    "Shape",
    "Transform",
    "Node",
    "Names",
    "Color",
    "Position",
    "I18NDictionary",
    "Features",
    "load",
    "generate_all_docs",
    "generate_class_docs",
    "generate_minimal_docs",
]


def load(filename):
    """Load a Babelfont format font file."""
    from babelfont.convertors.nfsf import Babelfont
    from babelfont.convertors import Convert

    convertor = Convert(filename)
    return Babelfont.load(convertor)
