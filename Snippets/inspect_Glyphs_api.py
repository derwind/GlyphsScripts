#MenuTitle: Inspect Glyphs api
# -*- coding: utf-8 -*-

import inspect

font = Glyphs.currentDocument.font
print type(font)
ufoExporter = Glyphs.objectWithClassName_("GlyphsFileFormatUFO")
print type(ufoExporter)
print dir(ufoExporter)
#for x in inspect.getmembers(ufoExporter, inspect.ismethod):
#    print x[0]
ufoExporter.setConvertNames_(True)
ufoExporter.setFontMaster_(font.masters[0])
url = NSURL.fileURLWithPath_("~/test.ufo")
#ufoExporter.writeUfo_toURL_error_(font, url, None)
help(ufoExporter.writeUfo_toURL_error_)
# Oops... TypeError: <native-selector writeUfo:toURL:error: of <GlyphsFileFormatUFO: 0x6040002f0080>> is not a Python function
#inspect.getargspec(ufoExporter.writeUfo_toURL_error_)
