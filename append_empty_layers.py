#MenuTitle: Append Empty Layers
# -*- coding: utf-8 -*-

__doc__ = """
Create empty layers to specified glyphs.
"""

target_cids = range(842, 924+1)

def empty_layer(g):
    newLayer = g.layers[0].copy()
    for i in reversed(range(len(newLayer.paths))):
        del newLayer.paths[i]
    return newLayer

def main():
    glyphs = Glyphs.font.glyphs
    for cid in target_cids:
        gname = "cid{0:05d}".format(cid)
        g = glyphs[gname]
        newLayer = empty_layer(g)
        newLayer.name = "{}_stroke".format(g.name)
        g.layers.append(newLayer)

if __name__ == "__main__":
    main()
