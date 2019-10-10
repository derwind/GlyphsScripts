#MenuTitle: Divide Path At Node
# encoding: utf-8

layer = Glyphs.font.selectedLayers[0]
for path in layer.paths:
    for node in path.nodes:
        if node.selected:
            layer.dividePathAtNode_(node)
