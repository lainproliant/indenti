#
# A test script for the XmlWriter
#

from indent.XmlWriter import *
from indent.IndentWriter import *

xf = XmlFactory ()

outFile = open ("test.html", 'w')
outCSS = open ("test.css", 'w')

html = xf.html (
      xf.head (
         xf.meta ({'http-equiv': 'Content-Type',
                   'content': 'text/html;charset=utf-8'}),
         xf.link (rel='stylesheet', type='text/css', href='test.css'),
         xf.title ("Indent Tools")
      ),
      xf.body (
         xf.h1 ("Indent Tools", {'class': 'red'}),
         xf.a ("Indent Tools on Github", href="http://github.com/lainproliant/indent"),
         xf.table ([xf.tr ([xf.td (x * y) for x in range (1,11)]) for y in range (1,11)]),
         ))

outFile.write (str (html))
outFile.close ()

iw = IndentWriter (outCSS)

iw ('h1.red {')
with iw:
   iw ('color: red;')
iw ('}')
iw ()

iw ('table tr, table td {')
with iw:
   iw ('border: 2px solid black')
iw ('}')

