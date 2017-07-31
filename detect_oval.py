#MenuTitle: Detect ovals in current glyph
# -*- coding: utf-8 -*-

__doc__ = """
Detect ovals in current glyph.
"""

import math

def cross_product(pt1, pt2):
    return pt1.x * pt2.y - pt1.y * pt2.x

def twenty_times_segment_area(segment):
    pt0 = segment.points[0]
    pt1 = segment.points[1]
    pt2 = segment.points[2]
    pt3 = segment.points[3]

    return 6 * cross_product(pt0, pt1) + 3 * cross_product(pt0, pt2) + cross_product(pt0, pt3) + 3 * cross_product(pt1, pt2) + 3 * cross_product(pt1, pt3) + 6 * cross_product(pt2, pt3)

def all_curve_segments(segments):
    for i in range(4):
        if segments[i].type != "curve":
            return False
    return True

def elliptic_area(pt1, pt2, pt3, pt4):
    return math.pi * math.sqrt((pt1.x - pt3.x)**2 + (pt1.y - pt3.y)**2) * math.sqrt((pt2.x - pt4.x)**2 + (pt2.y - pt4.y)**2) / 4

def is_oval(path):
    if len(path.nodes) != 12 or len(path.segments) != 4 or not all_curve_segments(path.segments):
        return False

    # we judge a closed path is an oval if its bezier area and elliptic area are approximately same.

    APPROX_THRESHOLD = 1.35

    area1 = 0.
    for segment in path.segments:
        area1 += twenty_times_segment_area(segment)
    area1 /= 20

    pt1 = path.nodes[2]
    pt2 = path.nodes[2+3]
    pt3 = path.nodes[2+6]
    pt4 = path.nodes[2+9]
    area2 = elliptic_area(pt1, pt2, pt3, pt4)

    return 1/APPROX_THRESHOLD < area1 / area2 < APPROX_THRESHOLD

def main():
    for path in Glyphs.font.selectedLayers[0].paths:
        print is_oval(path)

if __name__ == "__main__":
    main()
