---
title: Features
---
A representation of the OpenType feature code.
## Features._formatspecific

* Python type: `dict`


Each object in Babelfont has an optional attached dictionary to allow the storage
of format-specific information. Font creation software may store any additional
information that they wish to have preserved on import and export under a
namespaced (reverse-domain) key in this dictionary. For example, information
specific to the Glyphs software should be stored under the key `com.glyphsapp`.
The value stored under this key may be any data serializable in JSON; typically
it will be a `dict`.

Note that there is an important distinction between the Python object format
of this field and the Babelfont-JSON representation. When stored to JSON, this key
is exported not as `_formatspecific` but as a simple underscore (`_`).



## Features.classes

* Python type: `Dict`

* When writing to Babelfont-JSON, each item in the list must be placed on a separate line.

A dictionary of classes. Each group is a list of glyph names or class names. The key should not start with @.


## Features.prefixes

* Python type: `Dict`

* When writing to Babelfont-JSON, each item in the list must be placed on a separate line.

A dictionary of OpenType lookups and other feature code to be placed before features are defined. The keys are user-defined names, the values are AFDKO feature code.


## Features.features

* Python type: `[Tuple]`

* When writing to Babelfont-JSON, each item in the list must be placed on a separate line.

A list of OpenType feature code, expressed as a tuple (feature tag, code).


