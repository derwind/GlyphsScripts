#MenuTitle: Dump T1 Charstring
# -*- coding: utf-8 -*-

__doc__ = """
dump T1 Charstring
"""

from fontTools.t1Lib import T1Font

def dump(font_path, gname):
    t1_font = T1Font(font_path)
    gs = t1_font.getGlyphSet()
    charstrings = t1_font["CharStrings"]
    g = charstrings[gname]
    g.decompile()
    operands = []
    for b in g.program:
        if isinstance(b, int):
            operands.append(b)
        else:
            print("[{}] << {} >>".format(", ".join(map(lambda v: str(v), operands)), b))
            operands = []

font = Glyphs.font
dump(font.filepath, font.selectedLayers[0].parent.name)
