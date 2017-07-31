#MenuTitle: Append Emoty Layers
# -*- coding: utf-8 -*-

__doc__ = """
Move outlines to background layers.
"""

target_cids = range(842, 924+1)

def main():
    glyphs = Glyphs.font.glyphs
    for cid in target_cids:
        gname = "cid{0:05d}".format(cid)
        g = glyphs[gname]
        newLayer = g.layers[0].copy()
        newLayer.name = "{}_background".format(g.name)
        g.layers.append(newLayer)
        for i in reversed(range(len(g.layers[0].paths))):
            del g.layers[0].paths[i]

if __name__ == "__main__":
    main()
