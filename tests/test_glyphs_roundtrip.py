from babelfont import Babelfont
import plistlib
import subprocess
from io import BytesIO


def test_roundtrip():
    font = Babelfont.open("tests/data/Test1.glyphs")
    Babelfont.save(font, "tests/data/Test1.roundtrip.glyphs")
    pl1_json = subprocess.run(
        ["plutil", "-convert", "xml1", "-o", "-", "tests/data/Test1.glyphs"],
        capture_output=True,
    )
    pl2_json = subprocess.run(
        ["plutil", "-convert", "xml1", "-o", "-",
            "tests/data/Test1.roundtrip.glyphs"],
        capture_output=True,
    )
    pl1 = plistlib.load(BytesIO(pl1_json.stdout))
    pl2 = plistlib.load(BytesIO(pl2_json.stdout))
    assert pl1 == pl2
