#MenuTitle: Find the terminal stroke and mark it in current glyph
# -*- coding: utf-8 -*-

__doc__ = """
Find the terminal strokes in specified glyphs and mark them.
"""

import sys, math

TARGET_CIDS = range(842, 924+1)

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
        path.applyTransform([1.*a/b, 0, 0, 1, 0, 0])
    else:
        path = draw_circle(a)
        path.applyTransform([1, 0, 0, 1.*b/a, 0, 0])
    path.applyTransform([xscale, xskew, yskew, yscale, x, y])
    return path

def highest_left_edge(path):
    """
    return the left right edge
    """

    # detect node whose y coord is larger than this threshold
    Y_THRESHOLD = 400

    corner = NSPoint(path.bounds.origin.x, path.bounds.origin.y + path.bounds.size.height)
    mindist2 = sys.maxint
    edge = None
    for node in path.points:
        if node.type != "line":
            continue
        if node.y <= Y_THRESHOLD:
            continue
        dist2 = (node.x - corner.x)**2 + (node.y - corner.y)**2
        if dist2 < mindist2:
            mindist2 = dist2
            edge = node
    return edge

def lowest_right_edge(path):
    """
    return the lowest right edge
    """

    corner = NSPoint(path.bounds.origin.x + path.bounds.size.width, path.bounds.origin.y)
    mindist2 = sys.maxint
    edge = None
    for node in path.points:
        if node.type != "line":
            continue
        dist2 = (node.x - corner.x)**2 + (node.y - corner.y)**2
        if dist2 < mindist2:
            mindist2 = dist2
            edge = node
    return edge

def approx_segment_length2(segment):
    """
    calculate approximate squared segment length
    """

    pt1 = segment.points[0]
    pt2 = segment.points[-1]
    return (pt1.x - pt2.x)**2 + (pt1.y - pt2.y)**2

def approx_segment_direction(segment, pt):
    """
    calculate approximate segment direction
    """

    if len(segment.points) == 2:
        x = segment.points[0].x - segment.points[1].x
        y = segment.points[0].y - segment.points[1].y
    else:
        for i in range(4):
            node = segment.points[i]
            if node.x == pt.x and node.y == pt.y:
                if i == 0:
                    x = segment.points[0].x - segment.points[1].x
                    y = segment.points[0].y - segment.points[1].y
                else:
                    x = segment.points[2].x - segment.points[3].x
                    y = segment.points[2].y - segment.points[3].y
    if x < 0:
        x *= -1
        y *= -1
    return NSPoint(x, y)

def approx_segment_center(segment):
    """
    calculate approximate segment center
    """

    pt1 = segment.points[0]
    pt2 = segment.points[-1]
    return NSPoint((pt1.x + pt2.x)*.5, (pt1.y + pt2.y)*.5)

def find_stroke_including_edge(path, edge):
    """
    find stroke including specified edge and calculate its center, its stem width and its direction, then return them
    """

    terminal_segments = []
    for segment in path.segments:
        for node in segment.points:
            if node.x == edge.x and node.y == edge.y:
                terminal_segments.append(segment)
                break
    ts0 = terminal_segments[0]
    ts1 = terminal_segments[1]
    if approx_segment_length2(ts0) >= approx_segment_length2(ts1):
        return approx_segment_center(ts1), math.sqrt(approx_segment_length2(ts1)), approx_segment_direction(ts0, edge)
    else:
        return approx_segment_center(ts0), math.sqrt(approx_segment_length2(ts0)), approx_segment_direction(ts1, edge)

def is_path_including_edge(path, edge):
    for node in path.points:
        if node.x == edge.x and node.y == edge.y:
            return True
    return False

def initial_stroke_in_layer(layer):
    edges = []
    for path in layer.paths:
        edge = highest_left_edge(path)
        if edge:
            edges.append(edge)
    edges = sorted(edges, key=lambda edge: edge.x)
    if len(edges) <= 0:
        return None, None, None
    initial_edge = edges[0]
    for path in layer.paths:
        if is_path_including_edge(path, initial_edge):
            center, stem_width, direction = find_stroke_including_edge(path, initial_edge)
            return center, stem_width, direction
    return None, None, None

def terminal_stroke_in_layer(layer):
    edges = []
    for path in layer.paths:
        edge = lowest_right_edge(path)
        if edge:
            edges.append(edge)
    edges = sorted(edges, key=lambda edge: edge.y)
    if len(edges) <= 0:
        return None, None, None
    terminal_edge = edges[0]
    if terminal_edge is None:
        return None, None, None
    for path in layer.paths:
        if is_path_including_edge(path, terminal_edge):
            center, stem_width, direction = find_stroke_including_edge(path, terminal_edge)
            return center, stem_width, direction
    return None, None, None

def main():
    ANGLE_THRESHOLD = math.pi*30/180

    glyphs = Glyphs.font.glyphs

    for cid in TARGET_CIDS:
        gname = "cid{0:05d}".format(cid)
        layer = glyphs[gname].layers[0]

        center, stem_width, direction = initial_stroke_in_layer(layer)
        if center is not None:
            r = stem_width * .5
            circle_path = draw_oval(r, r, center.x, center.y, 1, 0, 0, 1)
            layer.paths.append(circle_path)

        center, stem_width, direction = terminal_stroke_in_layer(layer)
        if center is not None:
            a = stem_width
            b = stem_width * .5
            angle = math.atan2(direction.y, direction.x)
            if angle < ANGLE_THRESHOLD:
                angle = ANGLE_THRESHOLD

            sin = math.sin(angle)
            cos = math.cos(angle)
            oval_path = draw_oval(a, b, center.x, center.y, cos, sin, -sin, cos)
            layer.paths.append(oval_path)

if __name__ == "__main__":
    main()
