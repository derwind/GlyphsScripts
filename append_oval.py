#MenuTitle: Append oval in current glyph
# -*- coding: utf-8 -*-

__doc__ = """
Append oval in current glyph.
"""

import math

def mk_node(x, y, type="offcurve"):
    pt = NSPoint(x, y)
    return GSNode(pt, type=type)

def draw_circle(r):
    K = 4.0 * (math.sqrt(2) - 1) / 3

    path = GSPath()
    path.nodes.append(mk_node(-K*r, r))
    path.nodes.append(mk_node(-r, K*r))
    path.nodes.append(mk_node(-r, 0, "curve"))
    path.nodes.append(mk_node(-r, -K*r))
    path.nodes.append(mk_node(-K*r, -r))
    path.nodes.append(mk_node(0, -r, "curve"))
    path.nodes.append(mk_node(K*r, -r))
    path.nodes.append(mk_node(r, -K*r))
    path.nodes.append(mk_node(r, 0, "curve"))
    path.nodes.append(mk_node(r, K*r))
    path.nodes.append(mk_node(K*r, r))
    path.nodes.append(mk_node(0, r, "curve"))
    path.closed = True
    return path

def draw_oval(a, b, x=0, y=0, xscale=1, xskew=0, yskew=0, yscale=1):
    if a >= b:
        path = draw_circle(b)
        path.applyTransform(1.*a/b, 0, 0, 1, 0, 0)
    else:
        path = draw_circle(a)
        path.applyTransform(1, 0, 0, 1.*b/a, 0, 0)
    path.applyTransform(xscale, xskew, yskew, yscale, x, y)
    return path

def main():
    cur_layer = Glyphs.font.selectedLayers[0]
    path = draw_oval(200, 100, 500, 100, 1/math.sqrt(2), 1/math.sqrt(2), -1/math.sqrt(2), 1/math.sqrt(2))
    cur_layer.paths.append(path)

if __name__ == "__main__":
    main()
