#MenuTitle: split and join glyphs
# -*- coding: utf-8 -*-

__doc__ = """
split and join glyphs
"""

import os, sys, re
from GlyphsApp.plugins import *

CONTOURS_THRESHOLD = 2
Y_THRESHOLD = 380

class UfoSplitter(object):
    def __init__(self, join=False):
        self.join = join

    def run(self):
        glyphs = Glyphs.font.glyphs
        if self.join:
            self.join_glyphs(glyphs)
        else:
            self.split_glyphs(glyphs)

    def split_glyphs(self, glyphs):
        new_pgo = []
        for gname in Glyphs.font.customParameters["glyphOrder"]:
            g = Glyphs.font.glyphs[gname]
            layer = g.layers[0]
            if len(layer.paths) > CONTOURS_THRESHOLD:
                upper = g.copy()
                upper.layers[0].clear()
                upper.name = "{}.upper".format(g.name)
                lower = g.copy()
                lower.layers[0].clear()
                lower.name = "{}.lower".format(g.name)
                for path in layer.paths:
                    if path.bounds.origin.y >= Y_THRESHOLD:
                        upper.layers[0].paths.append(path)
                    else:
                        lower.layers[0].paths.append(path)
                Glyphs.font.glyphs.append(upper)
                Glyphs.font.glyphs.append(lower)
                new_pgo.append(upper.name)
                new_pgo.append(lower.name)
                del Glyphs.font.glyphs[g.name]
            else:
                new_pgo.append(g.name)
        Glyphs.font.customParameters["glyphOrder"] = sorted(new_pgo)

    def join_glyphs(self, glyphs):
        new_pgo = []
        for gname in Glyphs.font.customParameters["glyphOrder"]:
            g = Glyphs.font.glyphs[gname]
            suffix = g.name.split(".")[-1]
            if suffix == "lower":
                continue
            elif suffix == "upper":
                parent_name = g.name.split(".")[0]
                g.name = parent_name
                lower_g = Glyphs.font.glyphs["{}.lower".format(parent_name)]
                for path in lower_g.layers[0].paths:
                    g.layers[0].paths.append(path)
                new_pgo.append(parent_name)
                del Glyphs.font.glyphs[lower_g.name]
            else:
                new_pgo.append(g.name)
        Glyphs.font.customParameters["glyphOrder"] = sorted(new_pgo)

def main():
    join = False

    ufo_splitter = UfoSplitter(join)
    ufo_splitter.run()

if __name__ == "__main__":
    main()
