#MenuTitle: Access to segments
# -*- coding: utf-8 -*-

from GlyphsApp.plugins import *

g = Glyphs.font.selectedLayers[0].parent
paths = Glyphs.font.selectedLayers[0].paths
for path in paths:
    segments = path.segments
    for segment in segments:
        print type(segment.points[0]), dir(segment.points[0])
