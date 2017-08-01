#MenuTitle: Detect ovals in current glyph
# -*- coding: utf-8 -*-

__doc__ = """
Detect remmen connections in specified glyphs.
"""

from GlyphsApp.plugins import *
import math

TARGET_CIDS = [843, 866, 879, 880, 887]

UPM = 1000

def dist(pt1, pt2):
    return math.sqrt((pt1.x - pt2.x)**2 + (pt1.y - pt2.y)**2)

def dist_pt_and_line(pt, a, b, c):
    """
    distance between pt and ax+by+c=0
    """

    return abs(a*pt.x+b*pt.y+c) / abs(a**2+b**2)

def cross_product(pt1, pt2):
    return pt1.x * pt2.y - pt1.y * pt2.x

def twenty_times_segment_area(segment):
    pt0 = segment.points[0]
    pt1 = segment.points[1]
    pt2 = segment.points[2]
    pt3 = segment.points[3]

    return 6*cross_product(pt0, pt1) + 3*cross_product(pt0, pt2) + cross_product(pt0, pt3) + 3*cross_product(pt1, pt2) + 3*cross_product(pt1, pt3) + 6*cross_product(pt2, pt3)

def all_curve_segments(segments):
    for i in range(4):
        if segments[i].type != "curve":
            return False
    return True

def elliptic_area(pt1, pt2, pt3, pt4):
    return math.pi * dist(pt1, pt3) * dist(pt2, pt4) / 4

def is_oval(path):
    """
    Is path an oval?
    """

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

def oval_center(oval_path):
    """
    calculate the coordinate of the center of given oval
    """

    pt1 = oval_path.nodes[2]
    pt3 = oval_path.nodes[2+6]
    return NSPoint((pt1.x+pt3.x)*.5, (pt1.y+pt3.y)*.5)

def detect_initial_final_stroke(layer):
    """
    detect initial stroke and final stroke among ovals
    """

    oval_paths = []
    for path in layer.paths:
        if is_oval(path):
            oval_paths.append(path)

    oval_paths = sorted(oval_paths, key=lambda oval_path: oval_center(oval_path).y)
    # init, fina
    return oval_paths[-1], oval_paths[0]

def center_vector_oval(oval_path):
    """
    calculate the center coordinate and the direction vector of given oval
    """

    pt1 = oval_path.nodes[2]
    pt2 = oval_path.nodes[2+3]
    pt3 = oval_path.nodes[2+6]
    pt4 = oval_path.nodes[2+9]

    d13 = dist(pt1, pt3)
    d24 = dist(pt2, pt4)
    if d13 > d24:
        direction = NSPoint(round((pt1.x-pt3.x)/d13, 2), round((pt1.y-pt3.y)/d13, 2))
    else:
        direction = NSPoint(round((pt2.x-pt4.x)/d24, 2), round((pt2.y-pt4.y)/d24, 2))

    return oval_center(oval_path), direction

def can_connect_as_remmen(fina_oval_path, init_oval_path, vertical_shift = UPM):
    """
    Can paths connect as remmen?
    """

    DISTANCE_THRESHOLD = 70 # 70units

    fina_center, fina_dir = center_vector_oval(fina_oval_path)
    init_center, init_dir = center_vector_oval(init_oval_path)
    init_center.y -= vertical_shift

    d2 = dist_pt_and_line(init_center, fina_dir.y, -fina_dir.x, -fina_dir.y*fina_center.x + fina_dir.x*fina_center.y)

    if d2 > DISTANCE_THRESHOLD:
        return False

    return True

def main():
    glyphs = Glyphs.font.glyphs

    for cid1 in TARGET_CIDS:
        gname1 = "cid{0:05d}".format(cid1)
        uni1 = int(glyphs[gname1].unicode, 16)
        layer1 = glyphs[gname1].layers[0]
        _, fina = detect_initial_final_stroke(layer1)
        for cid2 in TARGET_CIDS:
            gname2 = "cid{0:05d}".format(cid2)
            uni2 = int(glyphs[gname2].unicode, 16)
            layer2 = glyphs[gname2].layers[0]
            init, _ = detect_initial_final_stroke(layer2)

            if can_connect_as_remmen(fina, init):
                print "{0}(U+{1:04X}) and {2}(U+{3:04X}) can connect as remmen".format(gname1, uni1, gname2, uni2)
            else:
                print "{0}(U+{1:04X}) and {2}(U+{3:04X}) can not connect as remmen".format(gname1, uni1, gname2, uni2)

if __name__ == "__main__":
    main()
