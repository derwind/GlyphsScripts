#MenuTitle: Split all segments at its half point
# -*- coding: utf-8 -*-

from GlyphsApp.plugins import *

paths = Glyphs.font.selectedLayers[0].paths
for path in paths:
    for i in reversed(range(len(path.points))):
        if path.points[i].type != OFFCURVE:
            path.insertNodeWithPathTime_(i+.5)
