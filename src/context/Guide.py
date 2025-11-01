from dataclasses import dataclass
from .BaseObject import BaseObject, Color, Position


@dataclass
class _GuideFields:
    pos: Position
    name: str = None
    color: Color = None


@dataclass
class Guide(BaseObject, _GuideFields):
    def __post_init__(self):
        # Convert dict or list to Position if needed
        if isinstance(self.pos, dict):
            self.pos = Position(**self.pos)
        elif isinstance(self.pos, (list, tuple)):
            self.pos = Position(*self.pos)
        super().__post_init__()
